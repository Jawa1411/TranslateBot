from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from flask import Flask, request
import telegram
import re
from credentials import bot_token, bot_user_name,URL

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

def translate(word):
    firefox_binary = FirefoxBinary('/usr/bin/firefox/')
    driver = webdriver.Firefox(firefox_binary=firefox_binary)
    # driver = webdriver.Firefox()
    driver.get("http://dictionary.tamilcube.com")

    search_box = driver.find_element_by_id("name")
    search_box.send_keys(word)
    search_button = driver.find_element_by_id("Submit1")
    search_button.click()

    transword = driver.find_element_by_xpath("/html/body/div[3]/table/tbody/tr/td[2]/form/table[2]/tbody/tr/td[1]/div/table/tbody/tr[2]/td").text
    return transword
@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
       # retrieve the message in JSON and then transform it to Telegram object
   update = telegram.Update.de_json(request.get_json(force=True), bot)


#    update = bot.getUpdates()

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram understands UTF-8, so encode text for unicode compatibility
   text = update.message.text.encode('utf-8').decode()
   # for debugging purposes only
   print("got text message :", text)
   # the first time you chat with the bot AKA the welcoming message
   if text == "/start":
       # print the welcoming message
       bot_welcome = """
       Welcome to Translation bot, Enter the word to translate.
       """

    #    word = str(input("Enter the word to Translate"))
       # send the welcoming message
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)
   else :
       if(text):
            # word = text
    #    word = update.message.text.encode('utf-8').decode()
            tw=translate(text)
            bot.sendMessage(chat_id=chat_id, text=tw, reply_to_message_id=msg_id)
    


#    else:
#        try:
#            # clear the message we got from any non alphabets
#            text = re.sub(r"\W", "_", text)
#            # create the api link for the avatar based on http://avatars.adorable.io/
#            welcome = "Welcome to Translation bot, Enter the following commands to start translation"
#            # reply with a photo to the name the user sent,
#            # note that you can send photos by url and telegram will fetch it for you
#            bot.sendPhoto(chat_id=chat_id, text=welcome, reply_to_message_id=msg_id)
#        except Exception:
#            # if things went wrong
#            bot.sendMessage(chat_id=chat_id, text="There was a problem in the command you used, please enter correct command", reply_to_message_id=msg_id)

   return 'ok'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # something to let us know things work
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"

@app.route('/')
def index():
    return '.'
if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)


