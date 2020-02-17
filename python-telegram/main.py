from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
import logging
from todo import ToDoEntry, ToDoEntryManager
from helper import Formatter
import telegramcalendar


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# TODO 01: hide the value of the token?
updater = Updater(
    token="969883313:AAHS141QmPgF3B8OwYri-F7xY7FlGuH5TN0", use_context=True)
j = updater.job_queue

dispatcher = updater.dispatcher
todoManager = ToDoEntryManager()


def command_start(update, context):  # /start for basic instructions
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!!")


def command_todo(update, context):  # /todo _desc_ for adding todo
    if not context.args:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Please add your todo description after using /todo.")
        return

    todo_name = context.args[0]
    todoManager.prepareToDo(todo_name)

    update.message.reply_text("Deadline: ",
                              reply_markup=telegramcalendar.create_calendar())


def command_todo_calendar_callback(update, context):
    query = update.callback_query

    keyboard = [[InlineKeyboardButton("Yes", callback_data='CONFIRM_YES'),
                 InlineKeyboardButton("No", callback_data='CONFIRM_NO')]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    selected, date = telegramcalendar.process_calendar_selection(
        context.bot, update)

    if selected:
        query.edit_message_text(text="Deadline: {}\nConfirm?".format(
            date.strftime("%d-%b-%Y")),
            reply_markup=reply_markup)
    else:
        query.edit_message_text("No deadline added.\nConfirm?",
                                reply_markup=reply_markup)


def todo_confirmation(update, context):  # callback for confirmation of adding todo
    query = update.callback_query
    # TODO 02: save todo here

    if (query.data == "CONFIRM_YES"):
        dispatcher.bot_data.update(todoManager.acceptToDo().toDict())
        query.edit_message_text("Your to-do item has been added.")
        print(dispatcher.bot_data)
    else:
        todoManager.rejectToDo()
        query.edit_message_text(
            "Rejected to-do item. Please enter again through the /todo command.")


def print_list(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=Formatter.print_formatted_list(
                                 dispatcher.bot_data),
                             parse_mode='Markdown')


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Sorry, I didn't understand that command.")


# ========================================== HANDLERS ================================================ #


start_handler = CommandHandler('start', command_start)
todo_handler = CommandHandler('todo', command_todo)
list_handler = CommandHandler('list', print_list)
calendar_handler = CallbackQueryHandler(command_todo_calendar_callback)
todo_confirmation_handler = CallbackQueryHandler(
    todo_confirmation, pattern="^CONFIRM")

dispatcher.add_handler(start_handler)
dispatcher.add_handler(todo_handler)
dispatcher.add_handler(todo_confirmation_handler)
dispatcher.add_handler(list_handler)
dispatcher.add_handler(calendar_handler)
dispatcher.add_handler(todo_confirmation_handler)
# TODO 04: Add error handler

updater.start_polling()
print("Bot running...")
