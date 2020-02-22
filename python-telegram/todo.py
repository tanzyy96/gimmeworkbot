
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
        return self._deadline

    @deadline.setter
    def deadline(self, deadline):
        self._deadline = deadline

    def toDict(self):
        return {self._title: self._deadline}

    def toString(self):
        if not self._deadline:
            return "{:30}|  N.A.".format(self._title)
        return "{:30}|  {:20}".format(self._title, self._deadline.strftime("%d-%b-%Y"))


class ToDoEntryManager:

    def __init__(self):
        self.queue = []

    def prepareToDo(self, desc, deadline=None):
        new_todo = ToDoEntry(desc, deadline)
        self.queue.append(new_todo)

    def changeDeadline(self, deadline):
        self.queue[0].deadline = deadline

    def rejectToDo(self):
        self.queue.pop(0)

    def acceptToDo(self):
        return self.queue.pop(0)
