from copy import deepcopy
import sys
import re
import numpy as np
from datetime import date
import sqlite3
from sqlite3 import Error
from os.path import exists
from datetime import date
from database.db import Database
from util.entry import Entry


if __name__ == "__main__":
    database = Database("database.db")
    conn = database.create_connection()
    database.create_database(conn)
    query = sys.argv
    query.pop(0)
    entry = Entry(query[0], np.array(query[1:6]), conn)
    entry.entryDetect()

