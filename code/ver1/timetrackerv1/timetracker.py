import sys
import re
import numpy as np
from datetime import date
import sqlite3
from sqlite3 import Error
from os.path import exists
import database
from database.db import Database
import util.entry as entry

if __name__ == "__main__":
    database = Database("database.db")
    conn = database.create_connection()
    if (exists("database.db") == False):
        database.create_database(conn)
    query = sys.argv
    query.pop(0)
    entry = entry.Entry(query[0], np.array(query[1:6]), conn)
    entry.entryDetect()

    """
    filename = 'database.json'
    if (query[0] == "record"):
        queryObj = {
            "date": query[1],
            "fromtime": query[2],
            "totime": query[3],
            "task": query[4],
            "tag": query[5]
        }
        with open(filename, 'r+') as outfile:
            #data = json.load(outfile)
            # data.append(queryObj)
            json.dump(queryObj, outfile)
            outfile.close()
    elif (query[0] == "query"):
        if (re.search('^:', query[1]) != None):
            with open(filename) as json_file:
                data = json.load(json_file)
                if (data["tag"] == query[1]):
                    print(data)
                json_file.close()

        elif (re.search('^\'', query[1]) != None):
            print(query[1])
            with open(filename) as json_file:
                data = json.load(json_file)
                if (data["task"] == query[1].replace("\'", "")):
                    print(data)
                json_file.close()
        else:
            with open(filename) as json_file:
                data = json.load(json_file)
                if (data["date"] == query[1]):
                    print(data)
                json_file.close()
    """
