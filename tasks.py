import tkinter as tk
from tkinter import simpledialog

from storage import load_tasks, save_tasks


def create_tasks(parent):
    tasks = load_tasks()

    def display_tasks():
        # Remove the old task widgets
        for widget in parent.winfo_children():
            widget.destroy()

        # Show a message when the task list is empty
        if not tasks:
            empty_label = tk.Label(
                parent,
                text="No tasks yet. Please add one.",
                font=("Arial", 11),
                bg="#F8F7F4",
                fg="#666666"
            )
            empty_label.pack(
                anchor="w",
                pady=5
            )
            return

        # Create a checkbox for every task
        for index, task in enumerate(tasks):
            completed_variable = tk.BooleanVar(
                value=task["completed"]
            )

            checkbox = tk.Checkbutton(
                parent,
                text=task["text"],
                variable=completed_variable,
                font=("Arial", 11),
                bg="#F8F7F4",
                activebackground="#F8F7F4",
                command=lambda task_index=index,
                variable=completed_variable:
                update_task_completion(task_index, variable)
            )

            checkbox.pack(
                anchor="w",
                pady=5
            )

    def update_task_completion(task_index, completed_variable):
        tasks[task_index]["completed"] = completed_variable.get()
        save_tasks(tasks)

    def add_task():
        new_task = simpledialog.askstring(
            "Add Task",
            "What task would you like to add?"
        )

        if new_task:
            new_task = new_task.strip()

            if new_task:
                task = {
                    "text": new_task,
                    "completed": False
                }

                tasks.append(task)
                save_tasks(tasks)
                display_tasks()

    # Display saved tasks when the app opens
    display_tasks()

    # Return the function used by the Add Task button
    return add_task
