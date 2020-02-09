from telegram.ext import Updater, InlineQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters, CallbackContext
import telegram
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

TOKEN = "969883313:AAHS141QmPgF3B8OwYri-F7xY7FlGuH5TN0"

bot = telegram.Bot(token=TOKEN)
print(bot.getMe())

# TODO 01: hide the value of the token?
updater = Updater(
    token=TOKEN, use_context=True)
j = updater.job_queue

dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


# using MessageHandler
def echo(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=update.message.text)


# using command arguments
def caps(update, context):
    text_caps = ''.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


# takes your inline input and return its capitilized form
def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


def callback_minute(context: CallbackContext):
    context.bot.send_message(chat_id='366058116',
                             text='One message every minute')


start_handler = CommandHandler('start', start)
caps_handler = CommandHandler('caps', caps)
echo_handler = MessageHandler(Filters.text, echo)
inline_caps_handler = InlineQueryHandler(inline_caps)
unknown_handler = MessageHandler(Filters.command, unknown)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(echo_handler)
dispatcher.add_handler(inline_caps_handler)
# must be added last, else all commands will trigger this handler
dispatcher.add_handler(unknown_handler)

job_minute = j.run_repeating(callback_minute, interval=60, first=0)

updater.start_polling()
print("Bot running...")
