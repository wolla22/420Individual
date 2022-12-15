from database.db import Database as db


class Rank:
    def __init__(self, conn):
        self.conn = conn

    def reportRank(self):
        return db.select_entries(db, self.conn, "rank", "")
