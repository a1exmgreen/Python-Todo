import tkinter as tk
from storage import load_tasks

def create_tasks(parent):

    tasks = [
        "Task 1",
        "Task 2",
        "Task 3",
        "Task 4",
        "Task 5"
    ]

    for task in tasks:
        checkbox = tk.Checkbutton(
            parent,
            text=task,
        )
        checkbox.pack()