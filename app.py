import tkinter as tk
from datetime import datetime

from sidebar import create_sidebar
from tasks import create_tasks

root = tk.Tk()
root.title("To-Do App")
root.geometry("800x600")
root.minsize(600, 400)

# Sidebar
sidebar = create_sidebar(root)

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

# Frame that holds task checkboxes
task_frame = tk.Frame(
    content,
    bg="#F8F7F4"
)
task_frame.pack(
    anchor="w",
    padx=30,
    pady=10
)

# Create the task list and receive the add_task function
add_task = create_tasks(task_frame)


# Add task button
add_task_button = tk.Button(
    content,
    text="+ Add Task",
    font=("Arial", 11, "bold"),
    bg="#A8D0DF",
    activebackground="#8CBACB",
    cursor="hand2",
    command=add_task
)
add_task_button.pack(
    anchor="w",
    padx=30,
    pady=15
)

# Start the application
root.mainloop()
