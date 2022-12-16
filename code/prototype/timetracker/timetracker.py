import sys
import re
import numpy as np
from datetime import date
import sqlite3
from sqlite3 import Error
from os.path import exists


class Entry:
    def __init__(self, entryString, parms, conn):
        self.entryString = entryString
        self.parms = parms
        self.conn = conn

    def entryDetect(self):
        if (self.entryString == "record"):
            entry = CreateEntry(self.parms, self.conn)
            entry.write()
        elif (self.entryString == "query"):
            entry = QueryEntry(self.parms, self.conn)
            entry.read()


class CreateEntry:
    def __init__(self, createObj, conn):
        self.createObj = createObj
        self.filename = 'database.json'
        self.conn = conn

    def checkDateString(self):
        objCopy = self.createObj
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
        Database.create_entry(self.conn, objCopy)


class QueryEntry(Entry):
    def __init__(self, queryObj, conn):
        self.queryObj = queryObj[0]
        self.filename = 'database.json'
        self.conn = conn

    def read(self):
        print(self.queryObj)
        if (re.search('^:', self.queryObj) != None):
            self.searchTag()
        elif (re.search('^\'', self.queryObj) != None):
            self.searchTask()
        else:
            self.searchDate()

    def searchTag(self):
        Database.select_entries(self.conn, "tag", self.queryObj)

    def searchTask(self):
        Database.select_entries(self.conn, "task", self.queryObj)

    def searchDate(self):
        Database.select_entries(self.conn, "date", self.queryObj)


class Database:
    def __init__(self, filename):
        self.filename = filename
        pass

    def create_connection(self):
        """ create a database connection to the SQLite database specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self.filename)
            return conn
        except Error as e:
            print(e)
        return conn

    def create_table(conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)

    def create_database(self, conn):
        sql_create_entries_table = """CREATE TABLE IF NOT EXISTS entries (
                                        id integer PRIMARY KEY,
                                        date text NOT NULL,
                                        fromtime text NOT NULL,
                                        totime text NOT NULL,
                                        task text NOT NULL,
                                        tag text NOT NULL
                                    );"""
        # create tables
        if conn is not None:
            # create tasks table
            self.create_table(conn, sql_create_entries_table)
        else:
            print("Error! cannot create the database connection.")

    def create_entry(conn, entry):
        """
        Create a new project into the projects table
        :param conn:
        :param project:
        :return: project id
        """
        sql = f''' INSERT INTO entries(date,fromtime,totime,task,tag)
                VALUES(?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, entry)
        conn.commit()
        return cur.lastrowid

    def select_entries(conn, query, search):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM entries")

        rows = cur.fetchall()
        entries = []
        print(rows)
        if (query == "tag"):
            for row in rows:
                if (row[5] == search):
                    entries.append(row)
        elif (query == "task"):
            for row in rows:
                if (row[4] == search):
                    entries.append(row)
        elif (query == "date"):
            for row in rows:
                if (row[1] == search):
                    entries.append(row)
        for entry in entries:
            print(entry)


if __name__ == "__main__":
    database = Database("database.db")
    conn = database.create_connection()
    if (exists("database.db") == False):
        database.create_database(conn)
    query = sys.argv
    query.pop(0)
    entry = Entry(query[0], np.array(query[1:6]), conn)
    entry.entryDetect()
