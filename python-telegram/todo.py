
class ToDoEntry:

    def __init__(self, title, deadline=None):
        self._title = title
        self._deadline = deadline

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def deadline(self):
        return self._title

    @deadline.setter
    def deadline(self, deadline):
        self._deadline = deadline

    def toDict(self):
        return {self._title: self._deadline}

    def toString(self):
        return "Name:{:8%s} |  {%s}".format(self._title, self._deadline)


class ToDoEntryManager:

    def __init__(self):
        self.queue = []

    def createToDo(self, desc, deadline=None):
        new_todo = ToDoEntry(desc, deadline)
        self.queue.append(new_todo)

    def rejectToDo(self):
        self.queue.pop(0)

    def acceptToDo(self):
        return self.queue.pop(0)

    @staticmethod
    def getToDoFromDict(_dict):
        # dict format {"name": "...", "deadline": "..."}
        return ToDoEntry(_dict["name"], _dict["deadline"])
