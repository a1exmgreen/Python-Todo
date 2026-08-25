import tkinter as tk
from tkinter import simpledialog

from storage import load_tasks, save_tasks


def create_tasks(parent):
    tasks = load_tasks()

    def display_tasks():
        # Remove the old task widgets before rebuilding the list
        for widget in parent.winfo_children():
            widget.destroy()

        # Show a message if there are no tasks
        if not tasks:
            empty_label = tk.Label(
                parent,
                text="No tasks yet. Please add a task.",
                font=("Arial", 11),
                bg="#F8F7F4",
                fg="#666666"
            )
            empty_label.pack(anchor="w", pady=5)
            return

        # Create a checkbox for every task
        for task in tasks:
            checkbox = tk.Checkbutton(
                parent,
                text=task,
                font=("Arial", 11),
                bg="#F8F7F4",
                activebackground="#F8F7F4"
            )
            checkbox.pack(
                anchor="w",
                pady=5
            )

    def add_task():
        new_task = simpledialog.askstring(
            "Add Task",
            "What task would you like to add?"
        )

        # Cancel returns None, so only continue if text was entered
        if new_task:
            new_task = new_task.strip()

            # Prevent a task containing only spaces
            if new_task:
                tasks.append(new_task)
                save_tasks(tasks)
                display_tasks()

    # Display saved tasks when the application starts
    display_tasks()

    return add_task
