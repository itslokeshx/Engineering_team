```python
import unittest
from backend import Task, TodoListManager

todo_list_manager = TodoListManager()

todo_list_manager.tasks = []

todo_list_manager.next_id = 1


class TestTodoListManager(unittest.TestCase):
    def test_add_task(self):
        task = todo_list_manager.add_task('Task 1', 'low')
        self.assertEqual(task.title, 'Task 1')
        self.assertEqual(task.priority, 'low')
        self.assertFalse(task.completed)
        self.assertEqual(len(todo_list_manager.tasks), 1)
        self.assertEqual(task.id, 1)

    def test_remove_task(self):
        task = todo_list_manager.add_task('Task 1', 'low')
        todo_list_manager.remove_task(task.id)
        self.assertEqual(len(todo_list_manager.tasks), 0)

    def test_mark_task_as_completed(self):
        task = todo_list_manager.add_task('Task 1', 'low')
        todo_list_manager.mark_task_as_completed(task.id)
        self.assertTrue(task.completed)

    def test_get_tasks(self):
        task1 = todo_list_manager.add_task('Task 1', 'low')
        task2 = todo_list_manager.add_task('Task 2', 'low')
        tasks = todo_list_manager.get_tasks()
        self.assertEqual(len(tasks), 2)

    def test_get_task_count(self):
        task1 = todo_list_manager.add_task('Task 1', 'low')
        task2 = todo_list_manager.add_task('Task 2', 'low')
        pending, completed = todo_list_manager.get_task_count()
        self.assertEqual(pending, 2)
        self.assertEqual(completed, 0)

    def test_get_tasks_filter_status(self):
        task1 = todo_list_manager.add_task('Task 1', 'low')
        task2 = todo_list_manager.add_task('Task 2', 'low')
        todo_list_manager.mark_task_as_completed(task1.id)
        tasks = todo_list_manager.get_tasks(status=True)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, task1.id)

    def test_get_tasks_filter_priority(self):
        task1 = todo_list_manager.add_task('Task 1', 'low')
        task2 = todo_list_manager.add_task('Task 2', 'medium')
        tasks = todo_list_manager.get_tasks(priority='low')
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, task1.id)

    def test_get_tasks_filter_status_and_priority(self):
        task1 = todo_list_manager.add_task('Task 1', 'low')
        task2 = todo_list_manager.add_task('Task 2', 'low')
        task3 = todo_list_manager.add_task('Task 3', 'medium')
        todo_list_manager.mark_task_as_completed(task1.id)
        tasks = todo_list_manager.get_tasks(status=True, priority='low')
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].id, task1.id)

    def test_remove_non_existent_task(self):
        with self.assertRaises(ValueError):
            todo_list_manager.remove_task(1)

    def test_mark_non_existent_task_as_completed(self):
        with self.assertRaises(ValueError):
            todo_list_manager.mark_task_as_completed(1)

if __name__ == '__main__':
    unittest.main()
```