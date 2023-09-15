# The bot main python file
# coding:utf-8
import telebot
from telebot import formatting
from instance import instance as ins

#----- API KEY importing -----
import telebot

# Replace 'YOUR_BOT_TOKEN' with the token provided by BotFather
TOKEN = "5428798399:AAH89nqubHm378fQicd1dgTgk7uSAFgIoB8"
adminchatid = 271045586

# Create a TeleBot instance
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Hi! Hit me with a doi/arxiv/youtube/quantamagazine link, I'll share it with everyone.")

@bot.message_handler(commands=['help'])
def handle_help(message):
    help_text = (
        "Available commands:\n"
        "/start - Start the bot.\n"
        "/help - Show this help message.\n"
        "/request - Make a request to admins to share a particular thing."
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['request'])
def handle_request(message):
    requestmessage = message.text
    bot.reply_to(message, "Your request has been received. We will process it shortly.")
    bot.send_message(text = requestmessage, chat_id= adminchatid)

@bot.message_handler(func=lambda message: True)
def handle_other_messages(message):
    try:
        text = message.text
        id  = message.chat.id
        requestinstance = ins(text)
        if requestinstance.identity['type'] != 'quantamag' and requestinstance.message != None:
            bot.send_message(chat_id= -1001183234135, text = requestinstance.message, parse_mode="Markdown")
        elif requestinstance.identity['type'] == 'quantamag' and requestinstance.message[0] != None:
            bot.send_photo(chat_id= -1001183234135, caption= requestinstance.message[0], parse_mode="Markdown", photo= requestinstance.message[1])
        else:
            bot.send_message(chat_id= id, text = "The request cannot be completed. Check if you sent the right link.")
    except:
        pass    
def main():
    bot.polling()

if __name__ == "__main__":
    main()
