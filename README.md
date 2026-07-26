# Multi-Agent AI Engineering and Debate Systems

This repository contains multi-agent AI systems built using the CrewAI framework. The codebase is organized into two primary projects: an autonomous software engineering crew (`engineering_team`) and a structured debate simulation crew (`debate`).

---

## Workspace Directory Structure

```
.
├── debate/
│   ├── src/debate/
│   │   ├── config/
│   │   │   ├── agents.yaml
│   │   │   └── tasks.yaml
│   │   ├── crew.py
│   │   └── main.py
│   ├── pyproject.toml
│   └── report.md
└── engineering_team/
    ├── sandbox/
    │   ├── app.py
    │   ├── backend.py
    │   ├── design.md
    │   ├── main.py
    │   ├── task.py
    │   ├── test_backend.py
    │   ├── test_summary.md
    │   └── todolistmanager.py
    ├── src/engineering_team/
    │   ├── config/
    │   │   ├── agents.yaml
    │   │   └── tasks.yaml
    │   ├── tools/
    │   │   └── sandbox_tools.py
    │   ├── crew.py
    │   ├── main.py
    │   └── patch.py
    └── pyproject.toml
```

---

## Project 1: Engineering Team (`engineering_team`)

### Overview
The `engineering_team` project is an autonomous software development framework where specialized AI agents collaborate sequentially to design, build, test, and validate full-stack Python software based on high-level natural language requirements.

Instead of writing code directly into the main repository, agents operate within an isolated `sandbox/` directory using custom execution tools. This ensures safe execution, isolated dependencies, and runtime verification.

---

### Agent Architecture and Roles

The crew consists of four distinct agents defined in `src/engineering_team/config/agents.yaml`:

1. **Engineering Lead**
   - **Model**: `groq/llama-3.3-70b-versatile`
   - **Role**: Analyzes the high-level prompt and produces a technical specification document (`sandbox/design.md`).
   - **Responsibilities**: Defines module architectures, class hierarchies, and method signatures without writing full implementation code. Assigns technical sub-tasks to the backend, frontend, and QA engineers.

2. **Backend Engineer**
   - **Model**: `groq/llama-3.3-70b-versatile`
   - **Role**: Implements object-oriented Python modules satisfying the design specification.
   - **Responsibilities**: Writes pure Python standard library modules (`task.py`, `todolistmanager.py`). Executes sandbox tools to verify syntax and functionality.

3. **Frontend Engineer**
   - **Model**: `groq/llama-3.3-70b-versatile`
   - **Role**: Builds an interactive web user interface using Gradio (`app.py`).
   - **Responsibilities**: Creates user-facing components matching backend APIs, implements custom color palettes and responsive layouts, and writes verification scripts (`_validate.py`) to confirm AST constructability without blocking process execution.

4. **Test Engineer**
   - **Model**: `groq/llama-3.3-70b-versatile`
   - **Role**: Performs quality assurance and unit testing (`test_backend.py`).
   - **Responsibilities**: Writes standard `unittest` test suites covering standard usage and edge cases (e.g., non-existent ID lookups). Runs tests inside the sandbox, identifies defects, fixes backend logic if needed, and produces a test summary report (`sandbox/test_summary.md`).

---

### Task Execution Workflow

The development lifecycle follows a strict sequence of dependent tasks defined in `src/engineering_team/config/tasks.yaml`:

```
[ Requirements Prompt ]
          │
          ▼
   1. design_task       ──> Generates sandbox/design.md
          │
          ▼
   2. code_task         ──> Implements backend logic in sandbox/
          │
          ▼
   3. frontend_task     ──> Implements Gradio UI (app.py) & validates setup
          │
          ▼
   4. test_task         ──> Runs unit tests (test_backend.py) & writes test_summary.md
```

---

### Sandbox Tooling and Infrastructure

Agents interact with the environment using specialized tools defined in `src/engineering_team/tools/sandbox_tools.py`:

- `write_file_tool`: Writes code files safely into the `sandbox/` directory.
- `read_file_tool`: Inspects file contents within `sandbox/`.
- `run_command_tool`: Executes Python scripts inside `sandbox/` under the project environment (`uv run`).
- `reset_sandbox`: Clears old sandbox artifacts before starting a new crew run.

In addition, `src/engineering_team/patch.py` applies custom runtime monkey-patches to integrate Model Context Protocol (MCP) tool bindings seamlessly within CrewAI.

---

### Sandbox Artifacts Example

When executed with the default Todo List Manager prompt, the crew generates:

- `task.py`: Data class representation for task entities (`id`, `title`, `priority`, `completed`).
- `todolistmanager.py`: In-memory state manager supporting task creation, status updates, deletion, filtering, and counts.
- `backend.py`: Unified entry point exporting core backend classes.
- `app.py`: Gradio web user interface with multi-tab controls.
- `test_backend.py`: Complete unit test suite verifying backend contracts.

---

### How to Run the Engineering Team

#### Running the Generated Application (`sandbox/`)
To execute the generated application directly:

```bash
cd engineering_team/sandbox

# 1. Run the CLI demonstration script
uv run --active python main.py

# 2. Run the full unit test suite
uv run --active python test_backend.py

# 3. Launch the Gradio web interface (available at http://127.0.0.1:7860)
uv run --active python app.py
```

#### Triggering a New Autonomous Crew Execution
To run the CrewAI agents with a custom or updated requirements prompt:

```bash
cd engineering_team
uv run run_crew
```

---

## Project 2: Debate Crew (`debate`)

### Overview
The `debate` project is a multi-agent framework designed to simulate structured multi-perspective debates on technical or philosophical topics.

### Agent Architecture and Roles
Defined in `src/debate/config/agents.yaml`:

1. **Debater Agents**: Construct structured, evidence-backed arguments for or against a target motion (e.g., topic evaluation, architectural trade-offs).
2. **Judge Agent**: Evaluates opposing arguments based on logical consistency, clarity, and evidence strength, declaring a winner and generating a final summary report (`debate/report.md`).

### How to Run the Debate Crew

```bash
cd debate
uv run crewai run
```

---

## Prerequisites and Installation

- **Python**: Version `>=3.10` and `<3.14`
- **Package Manager**: `uv`

To install dependencies across the workspace:

```bash
# Install UV package manager if not already installed
pip install uv

# Install crewAI CLI tool
pip install crewai
```

---

## License and Maintenance

Internal project repository maintained for multi-agent software engineering research and development.
