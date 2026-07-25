```python
# Test Module
import unittest
from backend import TodoList

class TestTodoList(unittest.TestCase):
    def test_add_task(self):
        todo_list = TodoList()
        task_id = todo_list.add_task('New Task', 'low')
        self.assertIn(task_id, todo_list.tasks)
        self.assertEqual(todo_list.tasks[task_id]['title'], 'New Task')
        self.assertEqual(todo_list.tasks[task_id]['priority'], 'low')
        self.assertFalse(todo_list.tasks[task_id]['completed'])

    def test_mark_task_complete(self):
        todo_list = TodoList()
        task_id = todo_list.add_task('New Task', 'low')
        todo_list.mark_task_complete(task_id)
        self.assertTrue(todo_list.tasks[task_id]['completed'])

    def test_remove_task(self):
        todo_list = TodoList()
        task_id = todo_list.add_task('New Task', 'low')
        todo_list.remove_task(task_id)
        self.assertNotIn(task_id, todo_list.tasks)

    def test_list_tasks(self):
        todo_list = TodoList()
        task1_id = todo_list.add_task('Task 1', 'low')
        task2_id = todo_list.add_task('Task 2', 'high')
        task3_id = todo_list.add_task('Task 3', 'low')
        todo_list.mark_task_complete(task2_id)
        tasks = todo_list.list_tasks()
        self.assertEqual(len(tasks), 3)
        tasks = todo_list.list_tasks(status='completed')
        self.assertEqual(len(tasks), 1)
        tasks = todo_list.list_tasks(priority='low')
        self.assertEqual(len(tasks), 2)

    def test_get_task_count(self):
        todo_list = TodoList()
        task1_id = todo_list.add_task('Task 1', 'low')
        task2_id = todo_list.add_task('Task 2', 'high')
        task3_id = todo_list.add_task('Task 3', 'low')
        todo_list.mark_task_complete(task2_id)
        count = todo_list.get_task_count()
        self.assertEqual(count['pending'], 2)
        self.assertEqual(count['completed'], 1)

if __name__ == '__main__':
    unittest.main()
```