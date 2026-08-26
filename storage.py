TASK_FILE = "tasks.txt"
ARCHIVE_FILE = "archived_tasks.txt"


def load_task_file(filename):
    tasks = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                # New format: completion status followed by task text
                if "|" in line:
                    completed_value, task_text = line.split("|", 1)

                    task = {
                        "text": task_text,
                        "completed": completed_value == "1"
                    }

                # Older plain-text tasks are loaded as incomplete
                else:
                    task = {
                        "text": line,
                        "completed": False
                    }

                tasks.append(task)

    except FileNotFoundError:
        pass

    return tasks


def save_task_file(filename, tasks):
    with open(filename, "w", encoding="utf-8") as file:
        for task in tasks:
            if task["completed"]:
                completed_value = "1"
            else:
                completed_value = "0"

            file.write(
                f"{completed_value}|{task['text']}\n"
            )


def load_tasks():
    return load_task_file(TASK_FILE)


def save_tasks(tasks):
    save_task_file(TASK_FILE, tasks)


def load_archived_tasks():
    return load_task_file(ARCHIVE_FILE)


def save_archived_tasks(tasks):
    save_task_file(ARCHIVE_FILE, tasks)
