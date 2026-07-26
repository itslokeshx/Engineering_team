from task import Task
from todolistmanager import TodoListManager

todo_list_manager = TodoListManager()

todo_list_manager.add_task('Task 1', 'low')
todo_list_manager.add_task('Task 2', 'medium')
todo_list_manager.add_task('Task 3', 'high')

tasks = todo_list_manager.get_tasks()
for task in tasks:
    print(task)

todo_list_manager.mark_task_as_completed(1)

tasks = todo_list_manager.get_tasks(status=True)
for task in tasks:
    print(task)

todo_list_manager.remove_task(2)

tasks = todo_list_manager.get_tasks()
for task in tasks:
    print(task)

pending, completed = todo_list_manager.get_task_count()
print(f'Pending: {pending}, Completed: {completed}')