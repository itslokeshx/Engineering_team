# System Design
The system will consist of two main modules: `backend.py` and `frontend.py`. The `backend.py` module will contain the backend logic, and the `frontend.py` module will contain the Gradio UI.

## Backend Module
The backend module will be responsible for managing the todo list. It will contain a `TodoList` class with the following methods:
### TodoList Class
* `__init__`: Initialize the todo list
* `add_task(title: str, priority: str) -> int`: Add a new task to the list
* `mark_task_complete(task_id: int) -> None`: Mark a task as complete
* `remove_task(task_id: int) -> None`: Remove a task from the list
* `list_tasks(status: str = None, priority: str = None) -> list`: List all tasks, optionally filtered by status or priority
* `get_task_count() -> dict`: Get a count of pending and completed tasks

## Frontend Module
The frontend module will be responsible for creating the Gradio UI. It will contain a `TodoListUI` class with the following methods:
### TodoListUI Class
* `__init__(todo_list: TodoList)`: Initialize the UI with a TodoList instance
* `create_app() -> gradio.App`: Create the Gradio app

## Test Module
The test module will be responsible for writing unit tests for the backend module. It will contain a `TestTodoList` class with the following methods:
### TestTodoList Class
* `test_add_task`: Test the `add_task` method
* `test_mark_task_complete`: Test the `mark_task_complete` method
* `test_remove_task`: Test the `remove_task` method
* `test_list_tasks`: Test the `list_tasks` method
* `test_get_task_count`: Test the `get_task_count` method

## Assignments
* `backend_engineer`: Write the `backend.py` module, including the `TodoList` class
* `frontend_engineer`: Write the `frontend.py` module, including the `TodoListUI` class, and create the Gradio app using the latest Gradio 6 APIs
* `test_engineer`: Write the `test_module.py` module, including the `TestTodoList` class, and write unit tests for the backend module

## Gradio 6 API Guidance
The `frontend_engineer` should use the latest Gradio 6 APIs to create the UI. Specifically, they should use the `gradio.App` class to create the app, and the `gradio.Interface` class to create the UI components. They should also use the `gradio.State` class to manage the state of the app.

The `frontend_engineer` should be aware of the changes in the Gradio 6 APIs, including the new `kwargs` and method signatures. They should consult the Context7 mcp tools to get the latest information on the Gradio 6 APIs.

## Sandbox Environment
All engineers will work in the same sandbox directory, with no directory structure. They will have access to a uv project with Gradio installed, and will be able to execute and test their code in this environment.

## Success Criteria
The system is successfully built and works when the following conditions are met:
* The `backend_engineer` has written the `backend.py` module, including the `TodoList` class, and it passes all unit tests written by the `test_engineer`.
* The `frontend_engineer` has written the `frontend.py` module, including the `TodoListUI` class, and has created a Gradio app that works as expected.
* The `test_engineer` has written unit tests for the backend module, and all tests pass.
* The system allows users to add, mark as complete, remove, list, and get task counts, and raises clear errors when trying to complete or remove a non-existent task ID.