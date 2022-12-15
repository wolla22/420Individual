from database.db import Database as db
from datetime import date


class CreateEntry():
    def __init__(self, createObj, conn):
        self.createObj = createObj
        self.conn = conn

    def checkDateString(self):
        objCopy = [0]*5
        if (self.createObj[0] == "today"):
            today = str(date.today())
            dateFormat = today.replace("-", "/")
            for i in range(len(self.createObj)):
                if (i == 0):
                    objCopy[0] = dateFormat
                    continue
                else:
                    objCopy[i] = self.createObj[i]
        return objCopy

    def write(self):
        objCopy = self.checkDateString()
        db.create_entry(self.conn, objCopy)
