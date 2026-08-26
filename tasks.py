import tkinter as tk
from tkinter import messagebox, simpledialog

from storage import load_tasks, save_tasks

def create_tasks(parent):
    tasks = load_tasks()

    def display_tasks():
        # Remove the existing tasks before rebuilding the list
        for widget in parent.winfo_children():
            widget.destroy()

        # Show a message when there aren't any tasks
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

        # Create a row for each task
        for index, task in enumerate(tasks):
            task_row = tk.Frame(
                parent,
                bg="#F8F7F4"
            )
            task_row.pack(
                fill="x",
                anchor="w",
                pady=5
            )

            completed_variable = tk.BooleanVar(
                value=task["completed"]
            )

            checkbox = tk.Checkbutton(
                task_row,
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
                side="left"
            )

            delete_button = tk.Button(
                task_row,
                text="Delete",
                font=("Arial", 9),
                bg="#E8A0A0",
                activebackground="#D78484",
                cursor="hand2",
                command=lambda task_index=index:
                delete_task(task_index)
            )
            delete_button.pack(
                side="right",
                padx=(15, 0)
            )

    def update_task_completion(task_index, completed_variable):
        tasks[task_index]["completed"] = completed_variable.get()
        save_tasks(tasks)

    def delete_task(task_index):
        task_text = tasks[task_index]["text"]

        confirmed = messagebox.askyesno(
            "Delete Task",
            f'Are you sure you want to delete "{task_text}"?'
        )

        if confirmed:
            tasks.pop(task_index)
            save_tasks(tasks)
            display_tasks()

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

    # Display saved tasks when the app starts
    display_tasks()

    # Give app.py access to the add_task function
    return add_task
