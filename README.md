# Univnoti

## How to run

### Windows

1. Download and install GIT (https://git-scm.com/downloads).
2. Download and install Python (https://www.python.org/downloads/).
3. Open cmd.exe with admin privileges, change directory for that one (<code>cd <path></code>), where you want to install the project, and clone this repository with next command: <code>git clone https://github.com/thegradle/univnoti</code>
4. Type in command line: <code>cd univnoti</code>
5. Install pyTelegramBotAPI with next command: <code>pip install pyTelegramBotAPI</code>
6. Install schedule with next command: <code>pip install schedule</code>
7. Create file secret.py and type the following code, where [tg-token] is token of your bot given by @botfather (https://sendpulse.com/knowledge-base/chatbot/telegram/create-telegram-chatbot) and chat-id is chat's id where you want to have notifications (you can use https://t.me/RawDataBot):<br>
<pre><code>TOKEN = '[tg-token]'
CHAT_ID = [chat-id]
</code></pre>
8. Start the bot by following code: <code>python main.py</code>
  
#### "ModuleNotFoundError: No module named 'telebot'" problem solved there https://stackoverflow.com/questions/58121141/how-to-fix-importerror-no-module-named-telebot
