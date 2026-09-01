TASK_FILE = "tasks.txt"
ARCHIVE_FILE = "archived_tasks.txt"
COMPLETED_FILE = "completed_tasks.txt"


def load_task_file(filename):
    """Load task dictionaries from a text file."""

    tasks = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Ignore empty lines
                if not line:
                    continue

                # Load tasks saved with completion information
                if "|" in line:
                    completed_value, task_text = line.split("|", 1)

                    task = {
                        "text": task_text,
                        "completed": completed_value == "1"
                    }

                # Support tasks stored using the older plain-text format
                else:
                    task = {
                        "text": line,
                        "completed": False
                    }

                # Add every loaded task to the list
                tasks.append(task)

    except FileNotFoundError:
        # Return an empty list if the file does not exist yet
        pass

    return tasks


def save_task_file(filename, tasks):
    """Save task dictionaries to a text file."""

    with open(filename, "w", encoding="utf-8") as file:
        for task in tasks:
            completed_value = (
                "1" if task["completed"] else "0"
            )

            file.write(
                f"{completed_value}|{task['text']}\n"
            )


def load_tasks():
    """Load active tasks."""

    return load_task_file(TASK_FILE)


def save_tasks(tasks):
    """Save active tasks."""

    save_task_file(TASK_FILE, tasks)


def load_archived_tasks():
    """Load archived tasks."""

    return load_task_file(ARCHIVE_FILE)


def save_archived_tasks(tasks):
    """Save archived tasks."""

    save_task_file(ARCHIVE_FILE, tasks)


def load_completed_tasks():
    """Load completed tasks."""

    return load_task_file(COMPLETED_FILE)


def save_completed_tasks(tasks):
    """Save completed tasks."""

    save_task_file(COMPLETED_FILE, tasks)