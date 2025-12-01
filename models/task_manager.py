from typing import Optional
from models.task import Task


class TaskManager:
    def __init__(self, repository: Optional[object] = None):
        """TaskManager can operate in-memory or with a repository for persistence.

        If `repository` is provided it must implement `load_all`, `save`,
        `delete` and `update_completion` methods (see `models.orm_models.TaskRepository`).
        """
        self.repo = repository
        self.tasks = []
        if self.repo:
            try:
                self.tasks = self.repo.load_all() or []
            except Exception:
                self.tasks = []

    def add_task(self, title, priority='Medium', due_date=None):
        task = Task(title, priority, due_date)
        self.tasks.append(task)
        if self.repo:
            try:
                self.repo.save(task)
            except Exception:
                pass
        return task

    def remove_task(self, title):
        self.tasks = [t for t in self.tasks if t.title != title]
        if self.repo:
            try:
                self.repo.delete(title)
            except Exception:
                pass

    def show_all_tasks(self):
        return self.tasks

    def sort_priority(self):
        priority_stake = {'High': 3, 'Medium': 2, 'Low': 1}
        self.tasks.sort(key=lambda t: priority_stake.get(t.priority, 0), reverse=True)

    def filter_priority(self, priority):
        return [t for t in self.tasks if t.priority == priority]

    def sort_by_due_date(self):
        self.tasks.sort(key=lambda t: t.due_date or '')

    def delete_task(self, title):
        # alias for remove_task kept for compatibility
        self.remove_task(title)

    def mark_complete(self, title):
        for t in self.tasks:
            if t.title == title:
                t.mark_complete()
                if self.repo:
                    try:
                        self.repo.update_completion(title, True)
                    except Exception:
                        pass
