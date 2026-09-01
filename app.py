import tkinter as tk
from datetime import datetime

from sidebar import create_sidebar
from tasks import create_task_manager


root = tk.Tk()
root.title("To-Do App")
root.geometry("800x600")
root.minsize(600, 400)

# Main content area
content = tk.Frame(
    root,
    bg="#F8F7F4"
)
content.pack(
    side="right",
    fill="both",
    expand=True
)

# Today's date
today = datetime.now()

date_label = tk.Label(
    content,
    text=today.strftime("%d %B %Y"),
    font=("Arial", 12),
    bg="#F8F7F4"
)
date_label.pack(
    pady=(15, 0)
)

# Page title
title = tk.Label(
    content,
    text="Today's Tasks",
    font=("Arial", 24, "bold"),
    bg="#F8F7F4"
)
title.pack(
    pady=(20, 15)
)

# Frame containing active or archived tasks
task_frame = tk.Frame(
    content,
    bg="#F8F7F4"
)
task_frame.pack(
    fill="x",
    anchor="nw",
    padx=30,
    pady=10
)

# Create the task manager
task_manager = create_task_manager(
    task_frame,
    title
)

# Add Task button
add_task_button = tk.Button(
    content,
    text="+ Add Task",
    font=("Arial", 11, "bold"),
    bg="#A8D0DF",
    activebackground="#8CBACB",
    cursor="hand2",
    command=task_manager["add_task"]
)
add_task_button.pack(
    anchor="w",
    padx=30,
    pady=15
)

# Create sidebar and connect the relevant pages
sidebar = create_sidebar(
    root,
    show_active_tasks=task_manager["show_active_tasks"],
    show_completed_tasks=task_manager["show_completed_tasks"],
    show_archived_tasks=task_manager["show_archived_tasks"]
)

root.mainloop()
