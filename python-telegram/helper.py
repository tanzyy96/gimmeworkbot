from todo import ToDoEntryManager


class Formatter:

    @staticmethod
    def print_formatted_list(bot_data):
        # receives bot_data which is a list of ToDoEntry
        # returns list as a formatted string for printing
        string = "```\n=============== My List of ToDos ==============\n"
        td_manager = ToDoEntryManager()
        for name, deadline in bot_data.items():
            td_manager.prepareToDo(name, deadline)
            todo = td_manager.acceptToDo()
            string += todo.toString() + "\n"
        return string + "\n```"
