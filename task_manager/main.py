# -*- coding: utf-8 -*-
from manager import TaskManager


def main():
    print("Выберите формат хранения данных:")
    print("J. JSON")
    print("C. CSV")
    format_choice = input("Введите номер формата: ")
    storage_format = "json" if format_choice == "J" else "csv"

    manager = TaskManager("tasks." + storage_format, storage_format)

    while True:
        print("\nМеню:")
        print("1. Просмотр задач")
        print("2. Добавить задачу")
        print("3. Редактировать задачу")
        print("4. Удалить задачу")
        print("5. Поиск задач")
        print("0. Выход")

        choice = input("Выберите действие: ")
        if choice == "1":
            tasks = manager.task_list()
            if tasks:
                for task in tasks:
                    print(task)
            else:
                print("Задач нет.")

        elif choice == "2":
            title = input("Название: ")
            description = input("Описание: ")
            category = input("Категория: ")
            due_date = input("Дата выполнения: ")
            priority = input("Приоритет (Низкий|Средний|Высокий): ")
            manager.create_task(title, description, category, due_date, priority)
            print("Задача добавлена.")

        elif choice == "3":
            try:
                task_id = int(input("ID задачи: "))
                task = next((task for task in manager.tasks if task.id == task_id), None)
                if not task:
                    print(f"Задача с указанным ID не найдена.")
                    continue

                print("1. Изменить поля")
                print("2. Изменить статус выполнения")
                update_choice = input("Выберите действие: ")

                if update_choice == "1":
                    print("Оставьте поля пустыми, если не хотите их изменять.")
                    title = input("Название: ")
                    description = input("Описание: ")
                    category = input("Категория: ")
                    due_date = input("Дата выполнения: ")
                    priority = input("Приоритет (Низкий|Средний|Высокий): ")

                    updated_task = manager.update_task(
                        task_id=task_id,
                        title=title if title.strip() else None,
                        description=description if description.strip() else None,
                        category=category if category.strip() else None,
                        due_date=due_date if due_date.strip() else None,
                        priority=priority if priority.strip() else None,
                    )

                    print("Задача обновлена:", updated_task)

                elif update_choice == "2":
                    message = manager.mark_task(task_id)
                    print(message)

                else:
                    print("Неверное действие.")
            except ValueError:
                print("Вводимый ID должен быть числом.")

        elif choice == "4":
            print("\nВыберите тип удаления:")
            print("1. Удалить задачу по ID")
            print("2. Удалить задачи по категории")

            delete_choice = input("Выберите действие: ")

            if delete_choice == "1":
                try:
                    task_id = int(input("Введите ID: "))
                    message = manager.delete_task_by_id(task_id)
                    print(message)
                except ValueError:
                    print("Вводимый ID должен быть числом.")

            elif delete_choice == "2":
                category = input("Введите категорию: ")
                message = manager.delete_tasks_by_category(category)
                print(message)
            else:
                print("Неверное действие.")

        elif choice == "5":
            print("Выберите тип поиска:")
            print("1. Поиск по ID")
            print("2. Поиск по категории")
            print("3. Поиск по ключевому слову")

            search_choice = input("Выберите действие: ")

            if search_choice == "1":
                try:
                    task_id = int(input("ID задачи: "))
                    task = manager.search_task_by_id(task_id)
                    if task:
                        print("\nРезультат:")
                        print(task)
                    else:
                        print("Задача с указанным ID не найдена.")
                except ValueError:
                    print("Вводимый ID должен быть числом.")

            elif search_choice == "2":
                category = input("Введите категорию для поиска: ")
                tasks = manager.search_tasks_by_category(category)
                if tasks:
                    print("\nРезультаты поиска по категории:")
                    for task in tasks:
                        print(task)
                else:
                    print("Задачи в указанной категории не найдены.")

            elif search_choice == "3":
                keyword = input("Введите ключевое слово для поиска: ")
                tasks = manager.search_tasks_by_keyword(keyword)
                if tasks:
                    print("\nРезультаты поиска по ключевому слову:")
                    for task in tasks:
                        print(task)
                else:
                    print("Задачи с указанным ключевым словом не найдены.")
            else:
                print("Неверное действие.")

        elif choice == "0":
            break

        else:
            print("Неверное действие.")


if __name__ == "__main__":
    main()
