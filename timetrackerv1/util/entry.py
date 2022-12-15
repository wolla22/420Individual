from .create import CreateEntry
from .query import QueryEntry


class Entry:
    def __init__(self, entryString, parms, conn):
        self.entryString = entryString
        self.parms = parms
        self.conn = conn

    def create_entry(self):
        if (self.entryString == "record"):
            entry = CreateEntry(self.parms, self.conn)
            entry.write()

    def query_entry(self):
        if (self.entryString == "query"):
            entry = QueryEntry(self.parms, self.conn)
            entry.read()

    def entryDetect(self):
        self.create_entry()
        self.query_entry()
