from .create import CreateEntry
from .query import QueryEntry
from .report import Report
from .rank import Rank


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

    def report_search(self):
        if (self.entryString == "report"):
            entry = Report(self.parms[0], self.parms[1], self.conn)
            entry.searchFromTo()

    def rank_priority(self):
        if (self.entryString == "priority"):
            entry = Rank(self.conn)
            entry.reportRank()

    def entryDetect(self):
        self.create_entry()
        self.query_entry()
        self.report_search()
        self.rank_priority()
