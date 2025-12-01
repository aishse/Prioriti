from models.task import Task
from datetime import date
class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, title, priority='Medium', due_date=None):
        task = Task(title, priority, due_date)
        self.tasks.append(task)
        return task

    def remove_task(self, title):
        self.tasks = [T for T in self.tasks if T.title != title]

    def show_all_tasks(self):
        return self.tasks

    def sort_priority(self):
        priority_stake = {'High': 3, 'Medium': 2, 'Low': 1}
        self.tasks.sort(key=lambda T: priority_stake[T.priority], reverse=True)
        
    def sort_date(self): 
        self.tasks.sort(key=lambda T: T.due_date or date.max)
    
    
    def sort_by_due_date(self):
        self.tasks.sort(key=lambda T: T.due_date or '')

    def delete_task(self, title):
        self.tasks = [T for T in self.tasks if T.title != title]

    def mark_complete(self, title):
        for T in self.tasks:
            if T.title == title:
                T.mark_complete()

