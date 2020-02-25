from telegram.ext import Updater, InlineQueryHandler, CallbackQueryHandler
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
import logging
from todo import ToDoEntry, ToDoEntryManager
from helper import Formatter
import telegramcalendar
import keyboard


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


class GimmeWorkBot:

    def __init__(self):
        # TODO 01: hide the value of the token?
        self.updater = Updater(
            token="969883313:AAHS141QmPgF3B8OwYri-F7xY7FlGuH5TN0", use_context=True)
        # j = self.updater.job_queue

        self.dispatcher = self.updater.dispatcher
        self.todoManager = ToDoEntryManager()
        self.add_handlers()

    def command_start(self, update, context):  # /start for basic instructions
        context.bot.send_message(
            chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!!")

    def command_todo(self, update, context):  # /todo _desc_ for adding todo
        if not context.args:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Syntax: /todo insertTodoNameHere")
            return

        todo_name = context.args[0]
        if not self.todoManager.checkUniqueTodoName(self.dispatcher.bot_data, todo_name):
            # edit todo
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Editing todo: {}".format(todo_name), reply_markup=keyboard.editTodoKeyboard())
        else:
            # add new todo
            self.todoManager.prepareToDo(todo_name)

            update.message.reply_text("Click END if you don't want to add a deadline!",
                                      reply_markup=telegramcalendar.create_calendar())

    # def command_todo_edit_callback(self, update, context):

    def command_todo_calendar_callback(self, update, context):
        query = update.callback_query

        keyboard = [[InlineKeyboardButton("Yes", callback_data='CONFIRM_YES'),
                     InlineKeyboardButton("No", callback_data='CONFIRM_NO')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        selected, date = telegramcalendar.process_calendar_selection(
            context.bot, update)

        if selected:
            if not date:
                query.edit_message_text("No deadline added.\nConfirm?",
                                        reply_markup=reply_markup)
            else:
                self.todoManager.changeDeadline(date)
                query.edit_message_text(text="Deadline: {}\nConfirm?".format(
                    date.strftime("%d-%b-%Y")),
                    reply_markup=reply_markup)

    # callback for confirmation of adding todo
    def todo_confirmation(self, update, context):
        query = update.callback_query
        # TODO 02: save todo here

        if (query.data == "CONFIRM_YES"):

            self.dispatcher.bot_data.update(
                self.todoManager.acceptToDo().toDict())
            query.edit_message_text("Your to-do item has been added.")
            print(self.dispatcher.bot_data)
        else:
            self.todoManager.rejectToDo()
            query.edit_message_text(
                "Rejected to-do item. Please enter again through the /todo command.")

    def print_list(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text=Formatter.print_formatted_list(
                                     self.dispatcher.bot_data),
                                 parse_mode='Markdown')

    def unknown(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Sorry, I didn't understand that command.")

    # ========================================== HANDLERS ================================================ #

    def add_handlers(self):
        start_handler = CommandHandler('start', self.command_start)
        todo_handler = CommandHandler('todo', self.command_todo)
        list_handler = CommandHandler('list', self.print_list)
        calendar_handler = CallbackQueryHandler(
            self.command_todo_calendar_callback)
        todo_confirmation_handler = CallbackQueryHandler(
            self.todo_confirmation, pattern="^CONFIRM")

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(todo_handler)
        self.dispatcher.add_handler(todo_confirmation_handler)
        self.dispatcher.add_handler(list_handler)
        self.dispatcher.add_handler(calendar_handler)
        self.dispatcher.add_handler(todo_confirmation_handler)
        # TODO 04: Add error handler

    def start(self):
        self.updater.start_polling()
        print("Bot running...")


if __name__ == "__main__":
    bot = GimmeWorkBot()
    bot.start()
