# -*- coding: utf-8 -*-
from storage import Storage
from task import Task
from typing import List, Optional


class TaskManager:
    def __init__(
            self,
            storage_path: str,
            storage_format:
            str = "json"
    ):
        self.storage = Storage(storage_path, storage_format)
        self.tasks = self.storage.load_tasks()

    def create_task(
            self, title: str,
            description: str,
            category: str,
            due_date: str,
            priority: str
    ) -> Task:
        task = Task(
            id=max([i.id for i in self.tasks], default=0) + 1,
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority
        )
        self.tasks.append(task)
        self.storage.save_tasks(self.tasks)

        return task

    def task_list(
            self,
            category: Optional[str] = None
    ) -> List[Task]:
        if category:
            return [task for task in self.tasks if task.category == category]

        return self.tasks

    def update_task(
            self,
            task_id: int,
            title: Optional[str] = None,
            description: Optional[str] = None,
            category: Optional[str] = None,
            due_date: Optional[str] = None,
            priority: Optional[str] = None
    ):
        for task in self.tasks:
            if task.id == task_id:
                if title:
                    task.title = title
                if description:
                    task.description = description
                if category:
                    task.category = category
                if due_date:
                    task.due_date = due_date
                if priority:
                    task.priority = priority
                self.storage.save_tasks(self.tasks)

                return task

    def mark_task(
            self,
            task_id: int
    ):
        for task in self.tasks:
            if task.id == task_id:
                if task.status == "Выполнена":
                    return f"Задача '{task.title}' уже выполнена."
                task.status = "Выполнена"
                self.storage.save_tasks(self.tasks)

                return task

    def delete_task_by_id(self, task_id: int) -> str:
        for task in self.tasks:
            if task.id == task_id:
                self.tasks.remove(task)
                self.storage.save_tasks(self.tasks)
                return f"Задача удалена."
        return f"Задача указанным ID не найдена."

    def delete_tasks_by_category(self, category: str) -> str:
        category = category.lower()
        tasks_to_delete = [task for task in self.tasks if task.category.lower() == category]
        if tasks_to_delete:
            for task in tasks_to_delete:
                self.tasks.remove(task)
            self.storage.save_tasks(self.tasks)
            return f"Все задачи из категории '{category}' успешно удалены."
        return f"Задачи из указанной категории не найдены."

    def search_tasks_by_keyword(
            self,
            keyword: str
    ) -> List[Task]:
        keyword = keyword.lower()
        return [
            task for task in self.tasks
            if keyword in task.title.lower()
            or keyword in task.description.lower()
            or keyword in task.category.lower()
            or keyword in task.status.lower()
        ]

    def search_task_by_id(
            self,
            task_id: int
    ) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)

    def search_tasks_by_category(
            self,
            category: str
    ) -> List[Task]:
        category = category.lower()
        return [task for task in self.tasks if task.category.lower() == category]
