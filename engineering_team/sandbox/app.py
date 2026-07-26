import gradio as gr
from backend import TodoListManager

todo_list_manager = TodoListManager()

with gr.Blocks() as demo:
    gr.Header("Todo List Manager")
    with gr.Tab("Add Task"):
        title = gr.Textbox(label="Title")
        priority = gr.Radio([
            "low",
            "medium",
            "high"
        ], label="Priority")
        add_task_button = gr.Button("Add Task")
        add_task_button.click(
            todo_list_manager.add_task,
            inputs=[title, priority],
            outputs=None
        )
    with gr.Tab("Remove Task"):
        task_id = gr.Number(label="Task ID")
        remove_task_button = gr.Button("Remove Task")
        remove_task_button.click(
            todo_list_manager.remove_task,
            inputs=[task_id],
            outputs=None
        )
    with gr.Tab("Mark Task as Completed"):
        task_id = gr.Number(label="Task ID")
        mark_task_as_completed_button = gr.Button("Mark Task as Completed")
        mark_task_as_completed_button.click(
            todo_list_manager.mark_task_as_completed,
            inputs=[task_id],
            outputs=None
        )
    with gr.Tab("List Tasks"):
        status = gr.Radio([
            "pending",
            "completed"
        ], label="Status")
        priority = gr.Radio([
            "low",
            "medium",
            "high"
        ], label="Priority")
        list_tasks_button = gr.Button("List Tasks")
        tasks = gr.JSON(label="Tasks")
        list_tasks_button.click(
            lambda status, priority: todo_list_manager.get_tasks(
                status=status if status != "pending" else False,
                priority=priority
            ),
            inputs=[status, priority],
            outputs=[tasks]
        )
    with gr.Tab("Task Count"):
        task_count = gr.JSON(label="Task Count")
        task_count_button = gr.Button("Task Count")
        task_count_button.click(
            todo_list_manager.get_task_count,
            inputs=None,
            outputs=[task_count]
        )

demo.launch()