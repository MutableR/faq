import sqlite3

class DBHelper:
    def __init__(self,dbname="faq.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)
    def setup(self):
        tblestmt = "CREATE TABLE IF NOT EXISTS items (description text, owner text, answer text)"
        itemidx = "CREATE INDEX IF NOT EXISTS itemIndex ON items (description)"
        ownidx = "CREATE INDEX IF NOT EXISTS ownIndex ON items (owner)"
        answidx = "CREATE INDEX IF NOT EXISTS answIndex ON items (answer)"
        self.conn.execute(tblestmt)
        self.conn.execute(itemidx)
        self.conn.execute(ownidx)
        self.conn.execute(answidx)
        self.conn.commit()
    def add_item(self, item_text, owner, answer):
        stmt = "INSERT INTO items (description, owner, answer) VALUES (?, ?, ?)"
        args = (item_text, owner, answer)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_owmers(self,):
        stmt = "SELECT owner FROM items"
        return [x[0] for x in self.conn.execute(stmt)]

    def delete_item(self, item_text, owner, answer):
        stmt = "DELETE FROM items WHERE description = (?) AND (owner = (?) AND answer = (?)"
        args = (item_text, owner, answer)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self, owner):
        stmt = "SELECT description,answer FROM items WHERE owner = (?)"
        args = (owner, )
        return [x[0] for x in self.conn.execute(stmt, args)]
    def get_answer(self,item_text):
        stmt = "SELECT answer FROM items WHERE description = (?)"
        args = (item_text, )
        return [x[0] for x in self.conn.execute(stmt, args)]