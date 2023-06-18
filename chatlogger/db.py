import sqlite3
from tzlocal import get_localzone_name
from . import utils
import os

class Db:

    def __init__(self):
        path_db = utils.path_db
        conn = sqlite3.connect(os.path.join(path_db, "chatlogger.s3db"))
        cur = conn.cursor()
        cur.execute('CREATE TABLE IF NOT EXISTS media_chats(chats INTEGER);')
        cur.execute('CREATE TABLE IF NOT EXISTS mess_chats(chats INTEGER);')
        cur.execute('CREATE TABLE IF NOT EXISTS settings(num INT PRIMARY KEY, tg_id INTEGER, tg_hash TEXT, logger_id INTEGER, logger_state TEXT, timezone TEXT);')
        conn.commit()
        self.conn = conn
        self.cur = cur
        self.on_empty_str()

    def on_empty_str(self):
        self.cur.execute('''SELECT * FROM settings''')
        settings = self.cur.fetchall()
        if len(settings) == 0:
            self.cur.execute(f"INSERT INTO settings(num, logger_id, logger_state, timezone) Values(1, 0, 'False', '{get_localzone_name()}')")
        self.conn.commit()

    def wr_media(self, chat_id):
        self.cur.execute(f"INSERT INTO media_chats(chats) Values({chat_id})")
        self.conn.commit()

    def wr_mess(self, chat_id):
        self.cur.execute(f"INSERT INTO mess_chats(chats) Values({chat_id})")
        self.conn.commit()

    def replace_tz(self, tz):
        self.cur.execute(f"UPDATE settings SET timezone='{tz}' WHERE num=1")
        self.conn.commit()

    def replace_logger_id(self, id):
        self.cur.execute(f"UPDATE settings SET logger_id={id} WHERE num=1")
        self.conn.commit()

    def replace_logger_state(self, state):
        self.cur.execute(f"UPDATE settings SET logger_state='{state}' WHERE num=1")
        self.conn.commit()

    def telegram(self):
        if 'chatlogger.session' not in os.listdir():
            id = int(input("enter id: "))
            hash = input("enter hash: ")
            self.cur.execute(f"UPDATE settings SET tg_id={id}, tg_hash='{hash}' WHERE num=1")
            self.conn.commit()
        else:
            self.cur.execute('''SELECT tg_id, tg_hash FROM settings''')
            telegram = self.cur.fetchone()
            id = telegram[0]
            hash = telegram[1]
        return [id, hash]

    def create_dict(self):
        dict = {}
        self.cur.execute('''SELECT * FROM media_chats''')
        media = self.cur.fetchall()
        self.cur.execute('''SELECT * FROM mess_chats''')
        text = self.cur.fetchall()
        self.cur.execute('''SELECT timezone, logger_id, logger_state FROM settings''')
        settings = self.cur.fetchone()
        dict['media'] = [i[0] for i in media]
        dict['text'] = [i[0] for i in text]
        dict['tz'] = settings[0]
        dict['logger'] = settings[1]
        dict['off'] = (settings[2] == 'True')
        return dict

    def del_media(self, id):
        self.cur.execute(f"DELETE FROM media_chats WHERE chats = '{id}'")
        self.conn.commit()

    def del_mess(self, id):
        self.cur.execute(f"DELETE FROM mess_chats WHERE chats = '{id}'")
        self.conn.commit()



