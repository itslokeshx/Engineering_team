# Design for Todo List Manager
## Overview
The Todo List Manager will consist of a backend module and a Gradio UI. The backend module will manage the tasks in-memory, and the Gradio UI will provide a user interface to interact with the backend.

## Backend Module
The backend module will be implemented by the `backend_engineer`. It will consist of a `Task` class and a `TodoListManager` class.

### Task Class
#### Attributes
* `id`: auto-incrementing integer ID
* `title`: task title
* `priority`: priority level (low, medium, high)
* `completed`: completed status (boolean)

#### Methods
* `__init__(self, title, priority)`: initialize a new task
* `mark_as_completed(self)`: mark the task as completed
* `__repr__(self)`: return a string representation of the task

### TodoListManager Class
#### Attributes
* `tasks`: list of tasks
* `next_id`: next available task ID

#### Methods
* `__init__(self)`: initialize the todo list manager
* `add_task(self, title, priority)`: add a new task to the list
* `remove_task(self, task_id)`: remove a task from the list by its ID
* `mark_task_as_completed(self, task_id)`: mark a task as completed by its ID
* `get_tasks(self, status=None, priority=None)`: return a list of tasks, optionally filtered by status or priority
* `get_task_count(self)`: return a count of pending and completed tasks
* `__getitem__(self, task_id)`: return a task by its ID

## Gradio UI
The Gradio UI will be implemented by the `frontend_engineer`. It will provide a user interface to interact with the backend module.

### Gradio App
The Gradio app will consist of the following components:
* `add_task`: a form to add a new task
* `remove_task`: a form to remove a task by its ID
* `mark_task_as_completed`: a form to mark a task as completed by its ID
* `list_tasks`: a dropdown to select the status and priority filters, and a button to list the tasks
* `task_count`: a display to show the count of pending and completed tasks

The Gradio app will use the following Gradio 6 APIs:
* `gradio.Interface`: to create the Gradio app
* `gradio.form`: to create forms for adding, removing, and marking tasks as completed
* `gradio.drop_down`: to create a dropdown for selecting the status and priority filters
* `gradio.button`: to create a button to list the tasks
* `gradio.display`: to create a display to show the task count

### API Guidance for Frontend Engineer
To use the Gradio 6 APIs, the `frontend_engineer` should follow these guidelines:
* Use `gradio.Interface` to create the Gradio app, and pass the `add_task`, `remove_task`, `mark_task_as_completed`, `list_tasks`, and `task_count` components as arguments.
* Use `gradio.form` to create forms for adding, removing, and marking tasks as completed. Pass the `title` and `priority` fields as arguments to the `add_task` form, and the `task_id` field as an argument to the `remove_task` and `mark_task_as_completed` forms.
* Use `gradio.drop_down` to create a dropdown for selecting the status and priority filters. Pass the `status` and `priority` fields as arguments to the `list_tasks` component.
* Use `gradio.button` to create a button to list the tasks. Pass the `list_tasks` component as an argument to the button.
* Use `gradio.display` to create a display to show the task count. Pass the `task_count` component as an argument to the display.

## Unit Tests
The unit tests will be implemented by the `test_engineer`. They will test the backend module to ensure it is working correctly.

### Test Cases
The following test cases will be implemented:
* Test adding a new task
* Test removing a task by its ID
* Test marking a task as completed by its ID
* Test getting tasks, optionally filtered by status or priority
* Test getting the task count
* Test error handling when trying to complete or remove a non-existent task ID

### Test Functions
The test functions will be implemented using the `unittest` framework. They will use the `assertEqual` method to assert that the expected and actual values are equal.

## Assignments to Engineers
* `backend_engineer`: implement the backend module, including the `Task` and `TodoListManager` classes
* `frontend_engineer`: implement the Gradio UI, including the Gradio app and its components
* `test_engineer`: implement the unit tests for the backend module