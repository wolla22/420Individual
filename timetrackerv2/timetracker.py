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

    """
    @startuml

class Entry {
  +entryString: String
  +parms: List
  +conn: Connection
  +__init__(entryString: String, parms: List, conn: Connection)
  +entryDetect()
}

class CreateEntry {
  +createObj: List
  +filename: String
  +conn: Connection
  +__init__(createObj: List, conn: Connection)
  +write()
}

class QueryEntry {
  +queryObj: String
  +filename: String
  +conn: Connection
  +__init__(queryObj: String, conn: Connection)
  +read()
  +searchTag()
  +searchTask()
  +searchDate()
}

class Report {
  +fromdate: List
  +todate: List
  +report_arr: List
  +conn: Connection
  +__init__(fromdate: List, todate: List, conn: Connection)
  +searchFromTo()
}

class Rank {
  +conn: Connection
  +__init__(conn: Connection)
  +reportRank()
}


@startuml

class Database {
  -filename: string
  +__init__()
  +create_connection(): Connection
  +create_table(conn: Connection, create_table_sql: string): void
  +create_database(conn: Connection): void
  +create_entry(conn: Connection, entry: tuple): int
  +select_entries(conn: Connection, query: string, search: any): list
}

@enduml


    """
