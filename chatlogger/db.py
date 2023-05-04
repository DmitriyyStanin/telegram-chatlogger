import sqlite3
from tzlocal import get_localzone_name
from . import utils
import os

class Db:

    def __init__(self):
        path_db = utils.path_db
        conn = sqlite3.connect(os.path.join(path_db, "chatlogger.s3db"))
        cur = conn.cursor()
        self.conn = conn
        self.cur = cur
        cur.execute('CREATE TABLE IF NOT EXISTS media_chats(chats INTEGER);')
        cur.execute('CREATE TABLE IF NOT EXISTS mess_chats(chats INTEGER);')
        cur.execute('CREATE TABLE IF NOT EXISTS timezone(num INT PRIMARY KEY, tz TEXT);')
        cur.execute('CREATE TABLE IF NOT EXISTS logger(num INT PRIMARY KEY, id INTEGER, state TEXT);')
        cur.execute('CREATE TABLE IF NOT EXISTS telegram(num INT PRIMARY KEY, id INTEGER, hash TEXT);')
        self.conn.commit()
        self.on_empty_str()

    def on_empty_str(self):
        self.cur.execute('''SELECT * FROM logger''')
        logger = self.cur.fetchall()
        if len(logger) == 0:
            self.cur.execute("INSERT INTO logger(num, id, state) Values(1, 0, 'False')")
        self.cur.execute('''SELECT * FROM timezone''')
        tz = self.cur.fetchall()
        if len(tz) == 0:
            self.cur.execute(f"INSERT INTO timezone(num, tz) Values(1, '{get_localzone_name()}')")
        self.conn.commit()

    def wr_media(self, chat_id):
        self.cur.execute(f"INSERT INTO media_chats(chats) Values({chat_id})")
        self.conn.commit()

    def wr_mess(self, chat_id):
        self.cur.execute(f"INSERT INTO mess_chats(chats) Values({chat_id})")
        self.conn.commit()

    def replace_tz(self, tz):
        self.cur.execute(f"UPDATE timezone SET tz='{tz}' WHERE num=1")
        self.conn.commit()

    def replace_logger_id(self, id):
        self.cur.execute(f"UPDATE logger SET id={id} WHERE num=1")
        self.conn.commit()

    def replace_logger_state(self, state):
        self.cur.execute(f"UPDATE logger SET state='{state}' WHERE num=1")
        self.conn.commit()

    def telegram(self):
        self.cur.execute('''SELECT * FROM telegram''')
        tg_table = self.cur.fetchall()
        if len(tg_table) == 0:
            id = int(input("введи id: "))
            hash = input("введи hash: ")
            self.cur.execute(f"INSERT INTO telegram(num, id, hash) Values(1, {id}, '{hash}')")
            self.conn.commit()
        elif 'chatlogger.session' not in os.listdir():
            id = int(input("введи id: "))
            hash = input("введи hash: ")
            self.cur.execute(f"UPDATE telegram SET id={id}, hash='{hash}' WHERE num=1")
            self.conn.commit()
        else:
            self.cur.execute('''SELECT * FROM telegram''')
            telegram = self.cur.fetchone()
            id = telegram[1]
            hash = telegram[2]
        return [id, hash]

    def create_dict(self):
        dict = {}
        self.cur.execute('''SELECT * FROM media_chats''')
        media = self.cur.fetchall()
        self.cur.execute('''SELECT * FROM mess_chats''')
        text = self.cur.fetchall()
        self.cur.execute('''SELECT * FROM timezone''')
        tz = self.cur.fetchone()
        self.cur.execute('''SELECT * FROM logger''')
        logger = self.cur.fetchone()

        dict['media'] = [i[0] for i in media]
        dict['text'] = [i[0] for i in text]
        dict['tz'] = tz[1]
        dict['logger'] = logger[1]
        dict['off'] = (logger[2] == 'True')
        return dict

    def del_media(self, id):
        self.cur.execute(f"DELETE FROM media_chats WHERE chats = '{id}'")
        self.conn.commit()

    def del_mess(self, id):
        self.cur.execute(f"DELETE FROM mess_chats WHERE chats = '{id}'")
        self.conn.commit()



