import tkinter as tk
from tasks import create_tasks
from sidebar import create_sidebar
from datetime import datetime

root = tk.Tk()
root.title("To-Do App")
root.geometry("800x600")

# Sidebar
sidebar = create_sidebar(root)

# Main content
content = tk.Frame(root, bg="#F8F7F4")
content.pack(side="right", fill="both", expand=True)

# Today's date
today = datetime.now()

date_label = tk.Label(
    content,
    text=today.strftime("%d %B %Y"),
    font=("Arial", 12),
    bg="#F8F7F4"
)

# Title
title = tk.Label(
    content,
    text="Today's Tasks",
    font=("Arial", 24, "bold"),
    bg="#F8F7F4"
)
title.pack(pady=20)

# Task container
task_frame = tk.Frame(content, bg="#F8F7F4")
task_frame.pack(anchor="nw", padx=30)

# Load tasks
create_tasks(task_frame)

root.mainloop()