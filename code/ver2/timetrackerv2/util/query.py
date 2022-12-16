from database.db import Database as db
import re


class QueryEntry():
    def __init__(self, queryObj, conn):
        self.queryObj = queryObj[0]
        self.conn = conn

    def read(self):
        if (re.search('^:', self.queryObj) != None):
            self.searchTag()
        elif (not "/" in self.queryObj and not ":" in self.queryObj):
            self.searchTask()
        else:
            self.searchDate()

    def searchTag(self):
        db.select_entries(db, self.conn, "tag", self.queryObj)

    def searchTask(self):
        db.select_entries(db, self.conn, "task", self.queryObj)

    def searchDate(self):
        db.select_entries(db, self.conn, "date", self.queryObj)
