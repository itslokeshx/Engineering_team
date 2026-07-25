# Backend Module

class TodoList:
    def __init__(self):
        self.tasks = {}
        self.next_id = 1

    def add_task(self, title: str, priority: str) -> int:
        task_id = self.next_id
        self.tasks[task_id] = {'title': title, 'priority': priority, 'completed': False}
        self.next_id += 1
        return task_id

    def mark_task_complete(self, task_id: int) -> None:
        if task_id not in self.tasks:
            raise ValueError('Task ID does not exist')
        self.tasks[task_id]['completed'] = True

    def remove_task(self, task_id: int) -> None:
        if task_id not in self.tasks:
            raise ValueError('Task ID does not exist')
        del self.tasks[task_id]

    def list_tasks(self, status: str = None, priority: str = None) -> list:
        tasks = list(self.tasks.values())
        if status:
            tasks = [task for task in tasks if task['completed'] == (status == 'completed')]
        if priority:
            tasks = [task for task in tasks if task['priority'] == priority]
        return tasks

    def get_task_count(self) -> dict:
        pending = sum(1 for task in self.tasks.values() if not task['completed'])
        completed = sum(1 for task in self.tasks.values() if task['completed'])
        return {'pending': pending, 'completed': completed}
