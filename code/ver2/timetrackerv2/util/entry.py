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
        entry = CreateEntry(self.parms, self.conn)
        entry.write()
        return "Record"

    def query_entry(self):

        entry = QueryEntry(self.parms, self.conn)
        entry.read()
        return "Query"

    def report_search(self):

        entry = Report(self.parms[0], self.parms[1], self.conn)
        entry.searchFromTo()
        return "Report"

    def rank_priority(self):
        entry = Rank(self.conn)
        entry.reportRank()
        return "Priority"

    def entryDetect(self):
        if (self.entryString == "record"):
            return self.create_entry()
        if (self.entryString == "query"):
            return self.query_entry()
        if (self.entryString == "report"):
            return self.report_search()
        if (self.entryString == "priority"):
            return self.rank_priority()
