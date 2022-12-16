from util.entry import Entry

import unittest


class TestSuite(unittest.TestCase):
    def test_record(self):
        conn = ""
        entry = Entry("record", [], conn)
        self.assertTrue(entry.entryDetect() == "record")

    def test_query(self):
        conn = ""
        entry = Entry("query", [], conn)
        self.assertTrue(entry.entryDetect() == "query")

    def test_record(self):
        conn = ""
        entry = Entry("report", [], conn)
        self.assertTrue(entry.entryDetect() == "report")

    def test_record(self):
        conn = ""
        entry = Entry("priority", [], conn)
        self.assertTrue(entry.entryDetect() == "priority")


if __name__ == '__main__':
    unittest.main()
