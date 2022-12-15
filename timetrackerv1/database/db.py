import sqlite3
from sqlite3 import Error


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
        conn = sqlite3.connect(self.filename)
        return conn

        return conn

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """

        c = conn.cursor()
        c.execute(create_table_sql)


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
        print(entry)
        return cur.lastrowid

    def checkTag(rows, search):
        entries = []
        for row in rows:
            if (row[5] == search):
                entries.append(row)
        return entries

    def checkTask(rows, search):
        entries = []
        for row in rows:
            if (row[4] == search):
                entries.append(row)
        return entries

    def checkDate(rows, search):
        entries = []
        for row in rows:
            if (row[1] == search):
                entries.append(row)
        return entries

    def select_entries(self, conn, query, search):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = conn.cursor()
        cur.execute("SELECT * FROM entries")

        rows = cur.fetchall()
        entries = []

        if (query == "tag"):
            entries = self.checkTag(rows, search)
        elif (query == "task"):
            entries = self.checkTask(rows, search)
        elif (query == "date"):
            entries = self.checkDate(rows, search)
        for entry in entries:
            print(entry)
