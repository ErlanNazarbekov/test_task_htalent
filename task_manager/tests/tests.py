# -*- coding: utf-8 -*-
import pytest
import os
from manager import TaskManager
from task import Task


@pytest.fixture
def json_task_manager(tmp_path):
    file_path = tmp_path / "tasks.json"
    return TaskManager(storage_path=str(file_path), storage_format="json")


@pytest.fixture
def csv_task_manager(tmp_path):
    file_path = tmp_path / "tasks.csv"
    return TaskManager(storage_path=str(file_path), storage_format="csv")


@pytest.fixture
def sample_task():
    return Task(
        id=1,
        title="Задача",
        description="Описание",
        category="Категория",
        due_date="2024-12-01",
        priority="Высокий",
        status="Не выполнена"
    )


def test_create_task(json_task_manager):
    manager = json_task_manager
    task = manager.create_task(
        title="Задача 1",
        description="Описание 1",
        category="Обучение",
        due_date="2024-12-01",
        priority="Средний"
    )
    assert task.title == "Задача 1"
    assert task.description == "Описание 1"
    assert task.category == "Обучение"
    assert task.due_date == "2024-12-01"
    assert task.priority == "Средний"
    assert len(manager.task_list()) == 1


def test_task_list(json_task_manager):
    manager = json_task_manager
    manager.create_task("Задача 1", "Описание 1", "Обучение", "2024-12-01", "Средний")
    manager.create_task("Задача 2", "Описание 2", "Работа", "2024-12-02", "Высокий")
    tasks = manager.task_list()
    assert len(tasks) == 2
    assert tasks[0].title == "Задача 1"
    assert tasks[1].title == "Задача 2"


def test_update_task(json_task_manager, sample_task):
    manager = json_task_manager
    manager.tasks.append(sample_task)
    updated_task = manager.update_task(
        task_id=1,
        title="Измененная задача",
        description="Измененное описание",
        priority="Низкий"
    )
    assert updated_task.title == "Измененная задача"
    assert updated_task.description == "Измененное описание"
    assert updated_task.priority == "Низкий"


def test_mark_task(json_task_manager, sample_task):
    manager = json_task_manager
    manager.tasks.append(sample_task)
    message = manager.mark_task(task_id=1)
    assert message.status == "Выполнена"
    assert manager.mark_task(1) == "Задача 'Задача' уже выполнена."


def test_delete_task_by_id(json_task_manager, sample_task):
    manager = json_task_manager
    manager.tasks.append(sample_task)
    message = manager.delete_task_by_id(1)
    assert message == "Задача удалена."
    assert len(manager.task_list()) == 0


def test_delete_tasks_by_category(json_task_manager):
    manager = json_task_manager
    manager.create_task("Задача 1", "Описание 1", "Работа", "2024-12-01", "Средний")
    manager.create_task("Задача 2", "Описание 2", "Работа", "2024-12-02", "Высокий")
    manager.create_task("Задача 3", "Описание 3", "Личное", "2024-12-03", "Низкий")
    message = manager.delete_tasks_by_category("Работа")
    assert message == "Все задачи из категории 'работа' успешно удалены."
    assert len(manager.task_list()) == 1


def test_search_task_by_id(json_task_manager, sample_task):
    manager = json_task_manager
    manager.tasks.append(sample_task)
    task = manager.search_task_by_id(1)
    assert task.title == "Задача"
    assert manager.search_task_by_id(99) is None


def test_search_tasks_by_category(json_task_manager):
    manager = json_task_manager
    manager.create_task("Задача 1", "Описание 1", "Работа", "2024-12-01", "Средний")
    manager.create_task("Задача 2", "Описание 2", "Работа", "2024-12-02", "Высокий")
    tasks = manager.search_tasks_by_category("Работа")
    assert len(tasks) == 2
    assert tasks[0].title == "Задача 1"
    assert tasks[1].title == "Задача 2"


def test_search_tasks_by_keyword(json_task_manager):
    manager = json_task_manager
    manager.create_task("Задача 1", "Описание 1", "Работа", "2024-12-01", "Средний")
    manager.create_task("Задача 2", "Описание 2", "Работа", "2024-12-02", "Высокий")
    tasks = manager.search_tasks_by_keyword("Задача")
    assert len(tasks) == 2
    assert tasks[0].title == "Задача 1"
    assert tasks[1].title == "Задача 2"


def test_csv_storage(csv_task_manager):
    manager = csv_task_manager
    manager.create_task("Задача CSV 1", "Описание 1", "Работа", "2024-12-01", "Средний")
    manager.create_task("Задача CSV 2", "Описание 2", "Обучение", "2024-12-02", "Высокий")
    manager.storage.save_tasks(manager.tasks)
    loaded_manager = TaskManager(manager.storage.file_path, "csv")
    tasks = loaded_manager.task_list()
    assert len(tasks) == 2
    assert tasks[0].title == "Задача CSV 1"
