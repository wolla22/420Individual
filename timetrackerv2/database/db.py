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

    def checkReport(rows, search):
        entries = []
        for row in rows:
            dateArray = str(row[1]).split("/")
            if len(dateArray) < 3:
                continue
            dateArray[0] = int(dateArray[0])
            dateArray[1] = int(dateArray[1])
            dateArray[2] = int(dateArray[2])
            if ((dateArray[0] >= int(search[0][0]) and dateArray[1] >= int(search[0][1]) and dateArray[2] >= int(search[0][2]))):
                if (dateArray[0] <= int(search[1][0]) and dateArray[1] <= int(search[1][1])):
                    entries.append(row)
        return entries

    def checkRank(rows):
        entries = []
        timeDiff = 0
        # loop through each database entry
        for row in rows:
            fromtime = row[2]
            totime = row[3]

            fromTimeInt = 0
            toTimeInt = 0
            # determine if the values for fromtime and totime end in AM or PM and change values to an int value
            if (fromtime[len(fromtime)-2:len(fromtime)] == "AM"):
                fromtime = fromtime[0:len(totime)-2]
                tempFromTime = fromtime.replace(":", "")
                fromTimeInt = int(tempFromTime)
            elif (fromtime[len(fromtime)-2:len(fromtime)] == "PM"):
                tempFromTime = fromtime[0:len(totime)-2]
                time = tempFromTime.replace(":", "")
                fromTimeInt = int(time)+1200
            if (totime[len(totime)-2:len(totime)] == "AM"):
                tempToTime = totime[0:len(totime)-2]
                time = tempToTime.replace(":", "")
                toTimeInt = int(time)
            elif (totime[len(totime)-2:len(totime)] == "PM"):
                tempToTime = totime[0:len(totime)-2]
                time = tempToTime.replace(":", "")
                toTimeInt = int(time)+1200

            if (fromtime[len(fromtime)-1:len(fromtime)] != "M" and totime[len(totime)-1:len(totime)] != "M"):
                time = fromtime.replace(":", "")
                fromTimeInt = int(time)
                time = totime.replace(":", "")
                toTimeInt = int(time)

            if (timeDiff == 0):
                entries.append(row)
                timeDiff = toTimeInt-fromTimeInt
            elif (timeDiff != 0):
                newTimeDiff = toTimeInt-fromTimeInt
                for entry in entries:
                    entryFromTime = entry[2]
                    entryToTime = entry[3]
                    entryFromTimeInt = 0
                    entryToTimeInt = 0
                    if (entryFromTime[len(entryFromTime)-2:len(entryFromTime)] == "AM"):

                        entryFromTime = entryFromTime[0:len(totime)-2]
                        tempEntryFromTime = entryFromTime.replace(":", "")
                        tempEntryFromTime = tempEntryFromTime.replace(
                            "A", "")
                        tempEntryFromTime = tempEntryFromTime.replace(
                            "P", "")
                        tempEntryFromTime = tempEntryFromTime.replace(
                            "M", "")
                        entryFromTimeInt = int(tempEntryFromTime)
                    if (entryFromTime[len(entryFromTime)-2:len(entryFromTime)] == "PM"):
                        tempFromTime = entryFromTime[0:len(totime)-2]
                        time = tempFromTime.replace(":", "")
                        time = time.replace(
                            "A", "")
                        time = time.replace(
                            "P", "")
                        time = time.replace(
                            "M", "")
                        entryFromTimeInt = int(time)+1200
                    if (entryToTime[len(entryToTime)-2:len(entryToTime)] == "AM"):
                        tempEntryToTime = entryToTime[0:len(entryToTime)-2]
                        time = tempEntryToTime.replace(":", "")
                        entryToTimeInt = int(time)
                    if (entryToTime[len(entryToTime)-2:len(entryToTime)] == "PM"):
                        tempEntryToTime = entryToTime[0:len(entryToTime)-2]
                        time = tempEntryToTime.replace(":", "")
                        entryToTimeInt = int(time)+1200
                    if ((entryFromTime[len(entryFromTime)-2:len(entryFromTime)] != "AM" and entryFromTime[len(entryFromTime)-2:len(entryFromTime)] == "PM") and (entryToTime[len(entryToTime)-2:len(entryToTime)] == "AM" and entryToTime[len(entryToTime)-2:len(entryToTime)] == "PM")):
                        time = entryFromTime.replace(":", "")
                        entryFromTimeInt = int(time)
                        time = entryToTime.replace(":", "")
                        entryToTimeInt = int(time)
                    entryTimeDiff = entryToTimeInt-entryFromTimeInt
                    if (newTimeDiff > entryTimeDiff):
                        entries.insert(entries.index(entry), row)
                        break
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
        elif (query == "report"):
            entries = self.checkReport(rows, search)
        elif (query == "rank"):
            entries = self.checkRank(rows)
        for entry in entries:
            print(entry)

        """if (query == "tag"):
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
        elif (query == "report"):
            for row in rows:
                dateArray = str(row[1]).split("/")
                if len(dateArray) < 3:
                    continue
                dateArray[0] = int(dateArray[0])
                dateArray[1] = int(dateArray[1])
                dateArray[2] = int(dateArray[2])
                if ((dateArray[0] >= int(search[0][0]) and dateArray[1] >= int(search[0][1]) and dateArray[2] >= int(search[0][2]))):
                    if (dateArray[0] <= int(search[1][0]) and dateArray[1] <= int(search[1][1])):
                        entries.append(row)
        elif (query == "rank"):
            timeDiff = 0
            # loop through each database entry
            for row in rows:
                fromtime = row[2]
                totime = row[3]

                fromTimeInt = 0
                toTimeInt = 0
                # determine if the values for fromtime and totime end in AM or PM and change values to an int value
                if (fromtime[len(fromtime)-2:len(fromtime)] == "AM"):
                    fromtime = fromtime[0:len(totime)-2]
                    tempFromTime = fromtime.replace(":", "")
                    fromTimeInt = int(tempFromTime)
                elif (fromtime[len(fromtime)-2:len(fromtime)] == "PM"):
                    tempFromTime = fromtime[0:len(totime)-2]
                    time = tempFromTime.replace(":", "")
                    fromTimeInt = int(time)+1200
                if (totime[len(totime)-2:len(totime)] == "AM"):
                    tempToTime = totime[0:len(totime)-2]
                    time = tempToTime.replace(":", "")
                    toTimeInt = int(time)
                elif (totime[len(totime)-2:len(totime)] == "PM"):
                    tempToTime = totime[0:len(totime)-2]
                    time = tempToTime.replace(":", "")
                    toTimeInt = int(time)+1200

                if (fromtime[len(fromtime)-1:len(fromtime)] != "M" and totime[len(totime)-1:len(totime)] != "M"):
                    time = fromtime.replace(":", "")
                    fromTimeInt = int(time)
                    time = totime.replace(":", "")
                    toTimeInt = int(time)

                if (timeDiff == 0):
                    entries.append(row)
                    timeDiff = toTimeInt-fromTimeInt
                elif (timeDiff != 0):
                    newTimeDiff = toTimeInt-fromTimeInt
                    for entry in entries:
                        entryFromTime = entry[2]
                        entryToTime = entry[3]
                        entryFromTimeInt = 0
                        entryToTimeInt = 0
                        if (entryFromTime[len(entryFromTime)-2:len(entryFromTime)] == "AM"):

                            entryFromTime = entryFromTime[0:len(totime)-2]
                            tempEntryFromTime = entryFromTime.replace(":", "")
                            tempEntryFromTime = tempEntryFromTime.replace(
                                "A", "")
                            tempEntryFromTime = tempEntryFromTime.replace(
                                "P", "")
                            tempEntryFromTime = tempEntryFromTime.replace(
                                "M", "")
                            entryFromTimeInt = int(tempEntryFromTime)
                        if (entryFromTime[len(entryFromTime)-2:len(entryFromTime)] == "PM"):
                            tempFromTime = entryFromTime[0:len(totime)-2]
                            time = tempFromTime.replace(":", "")
                            time = time.replace(
                                "A", "")
                            time = time.replace(
                                "P", "")
                            time = time.replace(
                                "M", "")
                            entryFromTimeInt = int(time)+1200
                        if (entryToTime[len(entryToTime)-2:len(entryToTime)] == "AM"):
                            tempEntryToTime = entryToTime[0:len(entryToTime)-2]
                            time = tempEntryToTime.replace(":", "")
                            entryToTimeInt = int(time)
                        if (entryToTime[len(entryToTime)-2:len(entryToTime)] == "PM"):
                            tempEntryToTime = entryToTime[0:len(entryToTime)-2]
                            time = tempEntryToTime.replace(":", "")
                            entryToTimeInt = int(time)+1200
                        if ((entryFromTime[len(entryFromTime)-2:len(entryFromTime)] != "AM" and entryFromTime[len(entryFromTime)-2:len(entryFromTime)] == "PM") and (entryToTime[len(entryToTime)-2:len(entryToTime)] == "AM" and entryToTime[len(entryToTime)-2:len(entryToTime)] == "PM")):
                            time = entryFromTime.replace(":", "")
                            entryFromTimeInt = int(time)
                            time = entryToTime.replace(":", "")
                            entryToTimeInt = int(time)
                        entryTimeDiff = entryToTimeInt-entryFromTimeInt
                        if (newTimeDiff > entryTimeDiff):
                            entries.insert(entries.index(entry), row)
                            break

        for entry in entries:
            print(entry)"""


"""elif (query == "report"):
            for row in rows:
                if (row[1] != "today"):
                    dateArray = str(row[1]).split("/")
                    dateArray[0] = int(dateArray[0])
                    dateArray[1] = int(dateArray[1])
                    dateArray[2] = int(dateArray[2])
                    if ((dateArray[0] >= int(search[0][0]) and dateArray[1] >= int(search[0][1]) and dateArray[2] >= int(search[0][2])) and (dateArray[0] <= int(search[1][0]) and dateArray[1] <= int(search[1][1]) and dateArray[2] <= int(search[1][2]))):
                        entries.append(row)
        elif (query == "rank"):
            timeDiff = 0
            # loop through each database entry
            for row in rows:
                fromtime = row[2]
                totime = row[3]

                fromTimeInt = 0
                toTimeInt = 0
                # determine if the values for fromtime and totime end in AM or PM and change values to an int value
                if (fromtime[len(fromtime)-2:len(fromtime)] == "AM"):
                    fromtime = fromtime[0:len(totime)-2]
                    tempFromTime = fromtime.replace(":", "")
                    fromTimeInt = int(tempFromTime)
                elif (fromtime[len(fromtime)-2:len(fromtime)] == "PM"):
                    tempFromTime = fromtime[0:len(totime)-2]
                    time = tempFromTime.replace(":", "")
                    fromTimeInt = int(time)+1200
                if (totime[len(totime)-2:len(totime)] == "AM"):
                    tempToTime = totime[0:len(totime)-2]
                    time = tempToTime.replace(":", "")
                    toTimeInt = int(time)
                elif (totime[len(totime)-2:len(totime)] == "PM"):
                    tempToTime = totime[0:len(totime)-2]
                    time = tempToTime.replace(":", "")
                    toTimeInt = int(time)+1200

                if (fromtime[len(fromtime)-1:len(fromtime)] != "M" and totime[len(totime)-1:len(totime)] != "M"):
                    time = fromtime.replace(":", "")
                    fromTimeInt = int(time)
                    time = totime.replace(":", "")
                    toTimeInt = int(time)

                if (timeDiff == 0):
                    entries.append(row)
                    timeDiff = toTimeInt-fromTimeInt
                elif (timeDiff != 0):
                    newTimeDiff = toTimeInt-fromTimeInt
                    for entry in entries:
                        entryFromTime = entry[2]
                        entryToTime = entry[3]
                        entryFromTimeInt = 0
                        entryToTimeInt = 0
                        if (entryFromTime[len(entryFromTime)-2:len(entryFromTime)] == "AM"):

                            entryFromTime = entryFromTime[0:len(totime)-2]
                            tempEntryFromTime = entryFromTime.replace(":", "")
                            entryFromTimeInt = int(tempEntryFromTime)
                        if (entryFromTime[len(entryFromTime)-2:len(entryFromTime)] == "PM"):
                            tempFromTime = entryFromTime[0:len(totime)-2]
                            time = tempFromTime.replace(":", "")
                            entryFromTimeInt = int(time)+1200
                        if (entryToTime[len(entryToTime)-2:len(entryToTime)] == "AM"):
                            tempEntryToTime = entryToTime[0:len(entryToTime)-2]
                            time = tempEntryToTime.replace(":", "")
                            entryToTimeInt = int(time)
                        if (entryToTime[len(entryToTime)-2:len(entryToTime)] == "PM"):
                            tempEntryToTime = entryToTime[0:len(entryToTime)-2]
                            time = tempEntryToTime.replace(":", "")
                            entryToTimeInt = int(time)+1200
                        if ((entryFromTime[len(entryFromTime)-2:len(entryFromTime)] != "AM" and entryFromTime[len(entryFromTime)-2:len(entryFromTime)] == "PM") and (entryToTime[len(entryToTime)-2:len(entryToTime)] == "AM" and entryToTime[len(entryToTime)-2:len(entryToTime)] == "PM")):
                            time = entryFromTime.replace(":", "")
                            entryFromTimeInt = int(time)
                            time = entryToTime.replace(":", "")
                            entryToTimeInt = int(time)
                        entryTimeDiff = entryToTimeInt-entryFromTimeInt
                        if (newTimeDiff > entryTimeDiff):
                            entries.insert(entries.index(entry), row)
                            break"""
