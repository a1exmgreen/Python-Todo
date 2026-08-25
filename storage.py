TASK_FILE = "tasks.txt"

def load_tasks():
    try:
        with open(TASK_FILE, "r") as file:
            return file.read().splitlines()

    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open(TASK_FILE, "w") as file:
        for task in tasks:
            file.write(task + "\n")