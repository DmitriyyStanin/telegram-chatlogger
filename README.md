# telegram-chatlogger

_with this tool you can log incoming messages and media messages from telegram chats. And also you can create backup of selected chat._
___

# Requirements
* **[api id and hash](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id)**
* **Python 3.6+**
___
# Installation

`apt update && apt install git && git clone https://github.com/kibersportovich/telegram-chatlogger && cd telegram-chatlogger && pip3 install -r requirements.txt`

# Start

`python3 -m chatlogger`

# Usage

_use the **[commands](#commands)** in telegram._ 

**For example:**
<details>
  <summary><b>.chats</b></summary>
  <img src="https://user-images.githubusercontent.com/131992312/235720286-7b669f99-8677-44b4-9674-6435aedc1de9.gif">
 </details>

 <details>
  <summary><b>.get_backup</b></summary>
  <img src="https://user-images.githubusercontent.com/131992312/235721739-bcd2004c-7c97-41c2-a342-f3df998cc4f4.gif">
 </details>
 
 ___

* If you want to connect new Telegram account, you just need to remove the chatlogger.session file from the directory
* With some commands, feedback messages are sent to "Saved Messages" (_**.log | .logmedia | .fast_backup**_)

# Commands
**.logmedia** - Log media messages in this chat (does not log stickers and gifs) </br>they will be signed and sent to the [logger-chat](#logger-chat)

**.log** - log messages in this chat; messages will be logged in a txt document, it can be retrieved with .get_backup

**.get_backup** *"chat id"* - get txt document with logged messages

**.del** *"chat id"* - disable message logging in chat

**.del_media** *"chat id"* - disable media message logging in chat

**.chats** - to see the logged chats

**.fast_backup** - Create a backup of all chat messages

**.set_logger** - makes this chat a [logger-chat](#logger-chat)

**.off_media** - on/off media message logging

**.set_tz** *"tz identifier"* - If the time of the logged messages is not displayed correctly, you can change tz;
tz identifier can be taken from [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

# logger-chat
a chat that receives media messages from logged chats
<p><img src="https://user-images.githubusercontent.com/131992312/235978342-e037c1f8-0189-4f26-85f8-637f935c0737.gif", width="500"></p>

