import re
import os
from telethon import TelegramClient, events
from telethon.tl.types import Message
from pytz import all_timezones
from .db import Db
from . import utils

path = utils.create_path()
me = int()
db_tools = Db()
db = db_tools.create_dict()

telegram = db_tools.telegram()
api_id = telegram[0]  
api_hash = telegram[1] 
client = TelegramClient('chatlogger', api_id, api_hash)


async def init_me():
    global me
    me_entity = await client.get_me()
    me = me_entity.id

@client.on(events.NewMessage(pattern=r'^\.set_tz$|^\.set_tz\s', outgoing=True))
async def set_tz(event: events.NewMessage.Event):
    '''
    If the time of the logged messages is not displayed correctly, set your time zone with ".set_tz"
    tz can be taken from here --> https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    '''
    message = event.message
    await message.delete()
    tz = message.text.split(' ', 1)
    chat_id = message.chat_id
    if len(tz) == 1:
        await client.send_message(chat_id, "You didn't write the time zone")
        return
    tz = tz[1]
    if tz not in all_timezones:
        await client.send_message(chat_id, 'this tz is not in the database')
        return
    db['tz'] = tz
    db_tools.replace_tz(tz)
    await client.send_message(chat_id, 'successfully')

@client.on(events.NewMessage(pattern=r'^\.logmedia$', outgoing=True))
async def logmedia(event: events.NewMessage.Event):
    '''Log media messages (does not log stickers and gifs) they will be signed and sent to the logger-chat'''
    message = event.message
    await message.delete()
    chat_id = message.chat_id
    if db['logger'] == chat_id:
        await client.send_message(me, "You can't log the logger-chat")
        return
    if chat_id == me:
        await client.send_message(me, "you can't log yourself")
        return
    if chat_id == message.sender_id:
        await client.send_message(me, "You can't log a channel")
        return
    if chat_id in db['media']:
        await client.send_message(me, 'chat is already logged')
        return

    await utils.create_logger_chat(client, db, db_tools)

    db['media'].append(chat_id)
    db_tools.wr_media(chat_id)
    await client.send_message(me, f'successfully added chat {chat_id}')

@client.on(events.NewMessage(pattern=r'^\.log$', outgoing=True))
async def log(event: events.NewMessage.Event):
    '''log messages; messages will be logged in a txt document, it can be retrieved with .get_backup'''
    message = event.message
    await message.delete()
    chat_id = message.chat_id
    if db['logger'] == chat_id:
        await client.send_message(me, "You can't log the logger chat")
        return
    if chat_id == me:
        await client.send_message(me, "you can't log yourself")
        return
    if chat_id == message.sender_id:
        await client.send_message(me, "You can't log a channel")
        return
    if chat_id in db['text']:
        await client.send_message(me, 'chat is already logged')
        return
    if message.is_private:
        chat_entity = await client.get_entity(chat_id)
        title = chat_entity.username
    else:
        title = message.chat.title
    name_group = f'{title} {str(chat_id)}.txt'
    f = open(os.path.join(path, name_group), 'x')
    f.close()
    db['text'].append(chat_id)
    db_tools.wr_mess(chat_id)
    await client.send_message(me, f'successfully added chat {chat_id}')

@client.on(events.NewMessage(pattern=r'^\.chats$', outgoing=True))
async def chats(event: events.NewMessage.Event):
    '''to see the logged chats'''
    message = event.message
    await message.delete()
    l = []
    for i in os.listdir(path):
        i = i.split('.')[:-1]
        i = '.'.join(i)
        l.append(i)
    mess_logged = '\n'.join(l)
    media_logged = '\n'.join(str(i) for i in db['media'])
    text = (f'**only messages**\n'
            f' CHATS:\n{mess_logged}\n\n'
            f'**media**\n'
            f'logger = {db["logger"]}\n'
            f' CHATS:\n{media_logged}')
    await client.send_message(message.chat_id, text, parse_mode='md')

@client.on(events.NewMessage(pattern=r'^\.del$|^\.del\s', outgoing=True))
async def del_log_mess(event: events.NewMessage.Event):
    '''disable message logging in chat'''
    message = event.message
    await message.delete()
    id = await utils.check_number(event.raw_text, message.chat_id, client)
    if id is False:
        return
    if id not in db['text']:
        await client.send_message(message.chat_id, 'this chat is not in the database')
        return
    db['text'].remove(id)
    db_tools.del_mess(id)
    for file in os.listdir(path):
        if re.split("[ .]", file)[-2] == str(id):
            os.remove(os.path.join(path, file))
            break
    await client.send_message(message.chat_id, 'successfully')

@client.on(events.NewMessage(pattern=r'^\.del_media$|^\.del_media\s', outgoing=True))
async def del_log_media(event: events.NewMessage.Event):
    '''disable media message logging in chat'''
    message = event.message
    await message.delete()
    id = await utils.check_number(event.raw_text, message.chat_id, client)
    if id is False:
        return
    if id not in db['media']:
        await client.send_message(message.chat_id, 'this chat is not in the database')
        return
    db['media'].remove(id)
    db_tools.del_media(id)
    await client.send_message(message.chat_id, 'successfully')

@client.on(events.NewMessage(pattern=r'^\.get_backup$|^\.get_backup\s', outgoing=True))
async def get_backup(event: events.NewMessage.Event):
    '''get txt document with logged messages'''
    message = event.message
    await message.delete()
    id = await utils.check_number(event.raw_text, message.chat_id, client)
    if id is False:
        return
    if id not in db['text']:
        await client.send_message(message.chat_id, 'this chat is not in the database')
        return
    for file in os.listdir(path):
        if re.split("[ .]", file)[-2] == str(id):
            path_file = os.path.join(path, file)
            await client.send_file(message.chat_id, path_file)
            return

@client.on(events.NewMessage(pattern=r'^\.fast_backup$', outgoing=True))
async def fast_backup(event: events.NewMessage.Event):
    '''Create a backup of all chat messages'''
    message = event.message
    await message.delete()
    chat_id = message.chat_id
    if chat_id == me:
        await client.send_message(me, 'you cannot get a backup of yourself')
        return
    if chat_id == message.sender_id:
        await client.send_message(me, 'you cannot get a backup of channel')
        return
    file_path = os.path.join(path, f'backup({chat_id}).txt')
    async for iter_message in client.iter_messages(message.chat_id, reverse=True):
        if isinstance(iter_message, Message) is False:
            continue
        if iter_message.media is not None:
            continue
        str_date = utils.date(iter_message, db['tz'])
        user = f'{iter_message.sender.first_name} ({iter_message.sender.username})'
        txt = open(file_path, "a", encoding="utf-8")
        txt.write(f'{user} >>> {str_date} >>> {iter_message.text}\n')
        txt.close()
    await client.send_file(me, file_path)
    os.remove(file_path)

@client.on(events.NewMessage(pattern=r'^\.set_logger$', outgoing=True))
async def set_logger_chat(event: events.NewMessage.Event):
    '''make the chat a logger-chat'''
    message = event.message
    await message.delete()
    if message.chat_id in db['media']:
        await client.send_message(me, "you can't make a logged chat a logger-chat")
        return
    db['logger'] = message.chat_id
    db_tools.replace_logger_id(message.chat_id)

@client.on(events.NewMessage(pattern=r'^\.off_media$', outgoing=True))
async def off_log_media(event: events.NewMessage.Event):
    '''Disable media message logging'''
    message = event.message
    await message.delete()
    if db['off'] is False:
        await client.send_message(message.chat_id, 'media logging is disabled')
    else:
        await client.send_message(message.chat_id, 'media logging is enabled')
    db['off'] = not db['off']
    db_tools.replace_logger_state(db['off'])


@client.on(events.NewMessage(func=lambda event: event.media is None))
async def just_message_handler(event: events.NewMessage.Event):
    message = event.message
    if message.chat_id not in db['text']:
        return
    sender = await client.get_entity(message.sender_id)
    str_date = utils.date(message, db['tz'])
    user = f'{sender.first_name} {sender.username}'
    path_file = str()
    for file in os.listdir(path):
        if re.split("[ .]", file)[-2] == str(message.chat_id):
            path_file = os.path.join(path, file)
            break
    txt = open(path_file, "a", encoding="utf-8")
    txt.write(f'{user} >>> {str_date} >>> {event.raw_text}\n')
    txt.close()

@client.on(events.NewMessage(func=lambda event: event.media is not None))
async def media_message_handler(event: events.NewMessage.Event):
    message = event.message
    if message.chat_id not in db['media'] or db['off']:
        return
    if message.sticker is not None or message.gif is not None:
        return
    if me == message.sender_id:
        return
    str_date = utils.date(message, db['tz'])
    if message.is_private:
        chat = await client.get_entity(message.chat_id)
        title = chat.first_name
        name_group = f'{title} ({str(message.chat_id)})'
        if message.video_note is not None:
            text = f'{name_group} >>> {str_date}'
            round = await client.send_file(entity=db['logger'], file=message.media)
            await round.reply(text)
            return
        if message.text != '':
            descrip = f'{message.text}\n\n{name_group} >>> {str_date}'
        else:
            descrip = f'{name_group} >>> {str_date}'
    else:
        title = message.chat.title
        sender = message.sender
        user = f'{sender.first_name} ({sender.username})'
        name_group = f'{title} ({str(message.chat_id)})'
        if message.video_note is not None:
            text = f'{name_group}: {user} >>> {str_date}'
            round = await client.send_file(entity=db['logger'], file=message.media)
            await round.reply(text)
            return
        if message.text != '':
            descrip = f'{message.text}\n\n{name_group}: {user} >>> {str_date}'
        else:
            descrip = f'{name_group}: {user} >>> {str_date}'

    await client.send_file(entity=db['logger'], file=message.media, caption=descrip)


with client as cl:
    cl.loop.run_until_complete(init_me())
    print(utils.chatlogger)
    cl.run_until_disconnected()

