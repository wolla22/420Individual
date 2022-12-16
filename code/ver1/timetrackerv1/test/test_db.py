from database.db import Database
import sqlite3

import unittest


class TestSuite(unittest.TestCase):
    def test_connection(self):
        conn = sqlite3.connect("hello.db")
        database = Database("hello.db")
        self.assertTrue(database.create_connection() == conn)


if __name__ == '__main__':
    unittest.main()
