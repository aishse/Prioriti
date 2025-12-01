from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import Session
from models.task import Task

Base = declarative_base()


class TaskModel(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String)
    priority = Column(String, nullable=False)  # e.g., 'High', 'Medium', 'Low'
    due_date = Column(Date)
    completed = Column(Boolean, default=False)

    def __repr__(self):
        return f"<TaskModel(id={self.id}, title='{self.title}', priority='{self.priority}', due_date={self.due_date}, completed={self.completed})>"


class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, task: Task):
        db_obj = TaskModel(
            title=task.title,
            priority=task.priority,
            due_date=task.due_date,
            completed=task.completed,
        )
        self.session.add(db_obj)
        try:
            self.session.commit()
            # Return the database id for diagnostics
            return db_obj.id
        except Exception:
            # Roll back the session so subsequent operations can proceed
            try:
                self.session.rollback()
            except Exception:
                pass
            # Re-raise so callers can handle/log the original problem
            raise

    def load_all(self):
        db_tasks = self.session.query(TaskModel).all()
        tasks = []
        for db_task in db_tasks:
            task = Task(
                title=db_task.title,
                priority=db_task.priority,
                due_date=db_task.due_date,
            )
            task.completed = db_task.completed
            tasks.append(task)
        return tasks

    def delete(self, title: str):
        db_task = self.session.query(TaskModel).filter_by(title=title).first()
        if db_task:
            self.session.delete(db_task)
            self.session.commit()

    def update_completion(self, title: str, completed: bool):
        db_task = self.session.query(TaskModel).filter_by(title=title).first()
        if db_task:
            db_task.completed = completed
            self.session.commit()
