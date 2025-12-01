class Task:
    priority_levels = ['Low', 'Medium', 'High']

    def __init__(self, title, priority='Medium', due_date=None):
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.completed = False

    def mark_complete(self):
        self.completed = True

    def set_priority(self, new_priority):
        if new_priority in Task.priority_levels:
            self.priority = new_priority

    def to_dict(self):
        return {
            'title': self.title,
            'priority': self.priority,
            'due_date': self.due_date,
            "completed": self.completed
        }

