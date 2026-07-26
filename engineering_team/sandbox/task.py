class Task:
    def __init__(self, title, priority):
        self.id = None
        self.title = title
        self.priority = priority
        self.completed = False

    def mark_as_completed(self):
        self.completed = True

    def __repr__(self):
        return f'Task({self.id}, {self.title}, {self.priority}, {self.completed})'
