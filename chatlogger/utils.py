import os
from pathlib import Path
from pytz import timezone
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.channels import CreateChannelRequest


path_db = os.path.join(Path.home(), 'chatlogger', 'db')
path = os.path.join(Path.home(), 'chatlogger', 'chats')

chatlogger = '''
┏━━━┓┏┓━┏┓┏━━━┓┏━━━━┓┏┓━━━┏━━━┓┏━━━┓┏━━━┓┏━━━┓┏━━━┓
┃┏━┓┃┃┃━┃┃┃┏━┓┃┃┏┓┏┓┃┃┃━━━┃┏━┓┃┃┏━┓┃┃┏━┓┃┃┏━━┛┃┏━┓┃
┃┃━┗┛┃┗━┛┃┃┃━┃┃┗┛┃┃┗┛┃┃━━━┃┃━┃┃┃┃━┗┛┃┃━┗┛┃┗━━┓┃┗━┛┃
┃┃━┏┓┃┏━┓┃┃┗━┛┃━━┃┃━━┃┃━┏┓┃┃━┃┃┃┃┏━┓┃┃┏━┓┃┏━━┛┃┏┓┏┛
┃┗━┛┃┃┃━┃┃┃┏━┓┃━┏┛┗┓━┃┗━┛┃┃┗━┛┃┃┗┻━┃┃┗┻━┃┃┗━━┓┃┃┃┗┓
┗━━━┛┗┛━┗┛┗┛━┗┛━┗━━┛━┗━━━┛┗━━━┛┗━━━┛┗━━━┛┗━━━┛┗┛┗━┛
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
             made by @kibersportovich
'''

async def create_logger_chat(cl, db, db_tools):
    ids = []
    async for chat in cl.iter_dialogs(
            offset_date=None,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=None):
        ids.append(chat.id)
    if db['off'] is False and db['logger'] not in ids:
        channel = await cl(CreateChannelRequest(
            title='ChatLogger',
            about='',
            megagroup=False))
        id = int('-100' + str(channel.chats[0].id))
        db['logger'] = id
        db_tools.replace_logger_id(id)

def create_path():
    if os.path.exists(path_db) is False:
        os.makedirs(path_db)
    if os.path.exists(path) is False:
        os.mkdir(path)
    return path

def date(message, tz):
    date = message.date
    date = date.astimezone(timezone(tz))
    str_date = date.strftime('%d/%m/%Y %H:%M:%S')
    return str_date

async def check_number(str, chat, cl):
    str = str.split(' ')
    if len(str) < 2:
        await cl.send_message(chat, 'enter id')
        return False
    number = str[1]
    try:
        number = int(number)
    except:
        await cl.send_message(chat, 'argument should be a number')
        return False
    return number
