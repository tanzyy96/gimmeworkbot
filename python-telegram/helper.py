from todo import ToDoEntryManager


class Formatter:

    @staticmethod
    def print_formatted_list(bot_data):
        # receives bot_data which is a list of ToDoEntry
        # returns list as a formatted string for printing
        string = "=== My List of ToDos ===\n"
        for entry in bot_data:
            todo = ToDoEntryManager.getToDoFromDict(entry)
            string += todo.toString() + "\n"
        return
