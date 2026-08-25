TASK_FILE = "tasks.txt"

def load_tasks():
    tasks = []

    try:
        with open(TASK_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                # Ignore  empty lines
                if not line:
                    continue

                # Load tasks saved in the file
                if "|" in line:
                    completed_value, task_test = line.split("|", 1)

                    task = {
                        "text": task_test,
                        "completed": completed_value == "1"
                    }

                # Load older tasks as incomplete
                else:
                    task = {
                        "text": line,
                        "completed": False
                    }

                tasks.append(task)

    except FileNotFoundError:
        pass

    return tasks

def save_tasks(tasks):
    with open(TASK_FILE, "w", ecoding="utf-8") as file:
        for task in tasks:
            if task["completed"]:
                completed_value = "1"
            else:
                completed_value = "0"

            file.write(
                f"{completed_value}|{task['text']}\n"
            )
