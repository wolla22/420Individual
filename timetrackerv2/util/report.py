from copy import deepcopy
import sys
import re
import numpy as np
from datetime import date
import sqlite3
from sqlite3 import Error
from os.path import exists
from datetime import date
from database.db import Database as db


class Report:
    def __init__(self, fromdate, todate, conn):
        self.fromdate = fromdate.split("/")
        self.todate = todate.split("/")
        self.conn = conn

    def checkDateString(self):
        if (self.fromdate == ['today']):
            today = str(date.today())
            dateFormat = today.split("-")
            self.fromdate = dateFormat
        if (self.todate == ['today']):
            today = str(date.today())
            dateFormat = today.split("-")
            self.todate = dateFormat

    def searchFromTo(self):
        self.checkDateString()
        db.select_entries(db, self.conn, "report", [
                          self.fromdate, self.todate])
