"""Monkey-patch for a CrewAI 1.14.4 bug where HTTPS MCP tool names are sanitized
on discovery but the sanitized name is then sent back to the server, so any
server tool whose name contains hyphens (e.g. Context7's `resolve-library-id`)
becomes unreachable. Re-verify on crewai upgrade.

Also includes Groq API Key rotation (GROQ_KEY_1..6), invalid key auto-skip,
and rate-limit retry logic.

Importing this module applies the patch as a side effect.
"""
import asyncio
import os
import re
import time
import threading
from typing import Any, cast
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env files
load_dotenv(find_dotenv(usecwd=True))
try:
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".env"))
except Exception:
    pass

from crewai.mcp.tool_resolver import MCPToolResolver
from crewai.tools.base_tool import BaseTool
from crewai.tools.mcp_tool_wrapper import MCPToolWrapper
from crewai.utilities.string_utils import sanitize_tool_name


def _resolve_external(self, mcp_ref: str) -> list[BaseTool]:
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client

    if "#" in mcp_ref:
        server_url, specific_tool = mcp_ref.split("#", 1)
    else:
        server_url, specific_tool = mcp_ref, None

    server_params = {"url": server_url}
    server_name = self._extract_server_name(server_url)
    sanitized_specific = sanitize_tool_name(specific_tool) if specific_tool else None

    async def _list_mcp_tools() -> list[Any]:
        async with streamablehttp_client(server_url) as (read, write, _):
            async with ClientSession(read, write) as session:
                await session.initialize()
                return list((await session.list_tools()).tools)

    try:
        mcp_tools = asyncio.run(_list_mcp_tools())
    except Exception as e:
        self._logger.log("warning", f"Failed to connect to MCP server {server_url}: {e}")
        return []

    tools: list[BaseTool] = []
    for mcp_tool in mcp_tools:
        sanitized = sanitize_tool_name(mcp_tool.name)
        if sanitized_specific and sanitized != sanitized_specific:
            continue
        args_schema = None
        if getattr(mcp_tool, "inputSchema", None):
            args_schema = self._json_schema_to_pydantic(sanitized, mcp_tool.inputSchema)
        schema = {
            "description": getattr(mcp_tool, "description", ""),
            "args_schema": args_schema,
        }
        try:
            wrapper = MCPToolWrapper(
                mcp_server_params=server_params,
                tool_name=sanitized,
                tool_schema=schema,
                server_name=server_name,
            )
            # Preserve the unsanitized server-side name so call_tool reaches the real tool.
            wrapper._original_tool_name = mcp_tool.name
            tools.append(wrapper)
        except Exception as e:
            self._logger.log("warning", f"Failed to create MCP tool wrapper for {sanitized}: {e}")

    return cast(list[BaseTool], tools)


MCPToolResolver._resolve_external = _resolve_external


# --- Groq API Key Rotation, Invalid Key Filtering & Rate Limit Handler ---
_key_lock = threading.Lock()
_key_counter = 0
_invalid_keys: set[str] = set()

def get_groq_keys() -> list[tuple[str, str]]:
    """
    Returns a list of tuples (key_name, key_value) sorted by index.
    Filters out keys marked as invalid.
    """
    keys_with_idx = []
    
    for k, v in os.environ.items():
        if not v or not v.strip():
            continue
        match = re.match(r"^GROQ_(?:API_)?KEY_?(\d+)$", k, re.IGNORECASE)
        if match:
            idx = int(match.group(1))
            val = v.strip()
            if val not in _invalid_keys:
                keys_with_idx.append((idx, k, val))
            
    if keys_with_idx:
        keys_with_idx.sort(key=lambda x: x[0])
        return [(k, v) for _, k, v in keys_with_idx]
        
    fallback = os.environ.get("GROQ_API_KEY") or os.environ.get("GROQ_KEY")
    if fallback and fallback.strip() and fallback.strip() not in _invalid_keys:
        return [("GROQ_API_KEY", fallback.strip())]
        
    return []

def mark_key_invalid(key_name: str, key_val: str):
    """Mark a key as invalid so it's skipped in subsequent rotations."""
    with _key_lock:
        _invalid_keys.add(key_val)
        masked_val = key_val[:7] + "..." + key_val[-4:] if len(key_val) > 11 else "***"
        print(f"\n[KeyRotator] ⚠️ WARNING: {key_name} ({masked_val}) is invalid! Removing it from active key pool.")

def rotate_groq_key() -> tuple[str, str] | None:
    """Gets the next valid (key_name, key_value) in round-robin sequence."""
    global _key_counter
    keys = get_groq_keys()
    if not keys:
        return None
    with _key_lock:
        key_tuple = keys[_key_counter % len(keys)]
        _key_counter += 1
        return key_tuple

import litellm

_original_completion = litellm.completion

def rate_limit_safe_completion(*args, **kwargs):
    groq_keys = get_groq_keys()
    current_key_name = "GROQ_API_KEY"
    
    # Rotate key for each request if Groq keys are present
    if groq_keys:
        key_tuple = rotate_groq_key()
        if key_tuple:
            current_key_name, key_val = key_tuple
            kwargs["api_key"] = key_val
            os.environ["GROQ_API_KEY"] = key_val
            masked_val = key_val[:7] + "..." + key_val[-4:] if len(key_val) > 11 else "***"
            print(f"\n[KeyRotator] Rotating key for request -> {current_key_name} ({masked_val})")

    max_attempts = max(10, len(groq_keys) * 2 if groq_keys else 10)
    for attempt in range(max_attempts):
        try:
            return _original_completion(*args, **kwargs)
        except Exception as e:
            err_str = str(e)
            is_invalid_key = (
                "invalid_api_key" in err_str or
                "Invalid API Key" in err_str or
                "401" in err_str or
                "Unauthorized" in err_str
            )
            is_rate_limit = (
                "Rate limit" in err_str or 
                "rate_limit_exceeded" in err_str or 
                "RateLimitError" in type(e).__name__ or
                "429" in err_str
            )

            if is_invalid_key:
                cur_key_val = kwargs.get("api_key") or os.environ.get("GROQ_API_KEY")
                if cur_key_val:
                    mark_key_invalid(current_key_name, cur_key_val)
                
                remaining_keys = get_groq_keys()
                if remaining_keys:
                    key_tuple = rotate_groq_key()
                    if key_tuple:
                        current_key_name, next_key_val = key_tuple
                        kwargs["api_key"] = next_key_val
                        os.environ["GROQ_API_KEY"] = next_key_val
                        masked_next = next_key_val[:7] + "..." + next_key_val[-4:] if len(next_key_val) > 11 else "***"
                        print(f"[KeyRotator] Retrying immediately with {current_key_name} ({masked_next})...")
                        continue
                raise e

            elif is_rate_limit:
                if attempt == max_attempts - 1:
                    raise e
                
                remaining_keys = get_groq_keys()
                if len(remaining_keys) > 1:
                    key_tuple = rotate_groq_key()
                    if key_tuple:
                        current_key_name, next_key_val = key_tuple
                        kwargs["api_key"] = next_key_val
                        os.environ["GROQ_API_KEY"] = next_key_val
                        masked_next = next_key_val[:7] + "..." + next_key_val[-4:] if len(next_key_val) > 11 else "***"
                        
                        if (attempt + 1) % len(remaining_keys) == 0:
                            wait_time = 5.0
                            match_ms = re.search(r"Please try again in (\d+(?:\.\d+)?)ms", err_str)
                            match_s = re.search(r"Please try again in (\d+(?:\.\d+)?)s", err_str)
                            if match_ms:
                                wait_time = (float(match_ms.group(1)) / 1000.0) + 1.0
                            elif match_s:
                                wait_time = float(match_s.group(1)) + 1.0
                            print(f"\n[RateLimitHandler] All available keys currently rate limited. Sleeping for {wait_time:.2f}s before retrying (attempt {attempt+1}/{max_attempts})...")
                            time.sleep(wait_time)
                        else:
                            print(f"\n[RateLimitHandler] Hit rate limit on attempt {attempt+1}/{max_attempts}. Rotating immediately to {current_key_name} ({masked_next})...")
                        continue

                wait_time = 10.0
                match_ms = re.search(r"Please try again in (\d+(?:\.\d+)?)ms", err_str)
                match_s = re.search(r"Please try again in (\d+(?:\.\d+)?)s", err_str)
                if match_ms:
                    wait_time = (float(match_ms.group(1)) / 1000.0) + 1.0
                elif match_s:
                    wait_time = float(match_s.group(1)) + 1.0
                print(f"\n[RateLimitHandler] Hit Groq TPM limit. Sleeping for {wait_time:.2f}s before retry (attempt {attempt+1}/{max_attempts})...")
                time.sleep(wait_time)
            else:
                raise e

litellm.completion = rate_limit_safe_completion
