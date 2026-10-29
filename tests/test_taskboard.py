import unittest
import tempfile
import os
import json
from taskboard import domain
from taskboard import storage

class TestValidation(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.sqlite3')
    def tearDown(self):
        os.close(self.db_fd)
        os.remove(self.db_path)
    def test_blank_title_rejected(self):
        with self.assertRaises(domain.TaskboardError):
            domain.add_task('   ', self.db_path)
    def test_unicode_and_sql_like_title(self):
        title = "שלום '; DROP TABLE tasks; --"
        task = domain.add_task(title, self.db_path)
        self.assertEqual(task['title'], title.strip())
        self.assertFalse(task['completed'])

class TestStateTransitions(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix='.sqlite3')
    def tearDown(self):
        os.close(self.db_fd)
        os.remove(self.db_path)
    def test_add_and_complete(self):
        t1 = domain.add_task('buy milk', self.db_path)
        self.assertEqual(t1['id'], 1)
        self.assertFalse(t1['completed'])
        listed = domain.list_tasks(self.db_path)
        self.assertEqual(len(listed), 1)
        self.assertEqual(listed[0]['title'], 'buy milk')
        completed = domain.complete_task('1', self.db_path)
        self.assertTrue(completed['completed'])
        # Idempotent complete
        completed2 = domain.complete_task('1', self.db_path)
        self.assertTrue(completed2['completed'])
    def test_invalid_id(self):
        domain.add_task('foo', self.db_path)
        with self.assertRaises(domain.TaskboardError):
            domain.complete_task('0', self.db_path)
        with self.assertRaises(domain.TaskboardError):
            domain.complete_task('-1', self.db_path)
        with self.assertRaises(domain.TaskboardError):
            domain.complete_task('999', self.db_path)
        with self.assertRaises(domain.TaskboardError):
            domain.complete_task('notanumber', self.db_path)

class TestPersistence(unittest.TestCase):
    def test_persistence_across_runs(self):
        db_fd, db_path = tempfile.mkstemp(suffix='.sqlite3')
        try:
            t1 = domain.add_task('task1', db_path)
            t2 = domain.add_task('task2', db_path)
            listed1 = domain.list_tasks(db_path)
            self.assertEqual(len(listed1), 2)
            # Simulate new process by re-importing domain
            listed2 = domain.list_tasks(db_path)
            self.assertEqual(listed2[0]['title'], 'task1')
            self.assertEqual(listed2[1]['title'], 'task2')
            domain.complete_task(str(t1['id']), db_path)
            listed3 = domain.list_tasks(db_path)
            self.assertTrue(listed3[0]['completed'])
            self.assertFalse(listed3[1]['completed'])
        finally:
            os.close(db_fd)
            os.remove(db_path)
