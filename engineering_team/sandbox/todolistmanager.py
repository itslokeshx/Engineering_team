class TodoListManager:
    def __init__(self):
        self.tasks = []
        self.next_id = 1

    def add_task(self, title, priority):
        task = Task(title, priority)
        task.id = self.next_id
        self.tasks.append(task)
        self.next_id += 1
        return task

    def remove_task(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                return
        raise ValueError('Task not found')

    def mark_task_as_completed(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.mark_as_completed()
                return
        raise ValueError('Task not found')

    def get_tasks(self, status=None, priority=None):
        tasks = self.tasks
        if status is not None:
            tasks = [task for task in tasks if task.completed == status]
        if priority is not None:
            tasks = [task for task in tasks if task.priority == priority]
        return tasks

    def get_task_count(self):
        pending = len([task for task in self.tasks if not task.completed])
        completed = len([task for task in self.tasks if task.completed])
        return pending, completed

    def __getitem__(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError('Task not found')
