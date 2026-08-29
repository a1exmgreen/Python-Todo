import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter as ctk

from theme import COLORS

from storage import (
    load_tasks,
    save_tasks,
    load_archived_tasks,
    save_archived_tasks
)


def create_task_manager(parent, title_label):
    tasks = load_tasks()
    archived_tasks = load_archived_tasks()

    def clear_task_area():
        """Remove the widgets currently displayed in the task area."""

        for widget in parent.winfo_children():
            widget.destroy()

    def show_active_tasks():
        """Display all active tasks."""

        title_label.configure(text="Today's Tasks")
        clear_task_area()

        completed_count = sum(
            1 for task in tasks if task["completed"]
        )

        remaining_count = len(tasks) - completed_count

        counter_label = ctk.CTkLabel(
            parent,
            text=f"{remaining_count} remaining • {completed_count} completed",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12
            ),
            text_color=COLORS["text_secondary"]
        )

        counter_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        if not tasks:
            empty_label = ctk.CTkLabel(
                parent,
                text="No active tasks. Add your first task to get started.",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=14
                ),
            )
            empty_label.pack(
                anchor="w",
                pady=5
            )
            return

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

            if task["completed"]:
                task_font = ("Segoe UI", 11, "overstrike")
                task_colour = COLORS["text_secondary"]
            else:
                task_font = ("Segoe UI", 11)
                task_colour = COLORS["text"]

            checkbox = tk.Checkbutton(
                task_row,
                text=task["text"],
                variable=completed_variable,
                font=task_font,
                fg=task_colour,
                bg="#F8F7F4",
                activebackground="#F8F7F4",
                activeforeground=task_colour,
                selectcolor="#F8F7F4",
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
                padx=(5, 0)
            )

            archive_button = tk.Button(
                task_row,
                text="Archive",
                font=("Arial", 9),
                bg="#D8C7EC",
                activebackground="#C4ADDE",
                cursor="hand2",
                command=lambda task_index=index:
                archive_task(task_index)
            )
            archive_button.pack(
                side="right",
                padx=(15, 0)
            )

    def show_archived_tasks():
        """Display all archived tasks."""

        title_label.configure(text="Archived Tasks")
        clear_task_area()

        if not archived_tasks:
            empty_label = tk.Label(
                parent,
                text="There are no archived tasks.",
                font=("Arial", 11),
                bg="#F8F7F4",
                fg="#666666"
            )
            empty_label.pack(
                anchor="w",
                pady=5
            )
            return

        for index, task in enumerate(archived_tasks):
            task_row = tk.Frame(
                parent,
                bg="#F8F7F4"
            )
            task_row.pack(
                fill="x",
                anchor="w",
                pady=5
            )

            task_label = tk.Label(
                task_row,
                text=task["text"],
                font=("Arial", 11),
                bg="#F8F7F4"
            )
            task_label.pack(
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
                delete_archived_task(task_index)
            )
            delete_button.pack(
                side="right",
                padx=(5, 0)
            )

            restore_button = tk.Button(
                task_row,
                text="Restore",
                font=("Arial", 9),
                bg="#A8DDB5",
                activebackground="#8FCCA0",
                cursor="hand2",
                command=lambda task_index=index:
                restore_task(task_index)
            )
            restore_button.pack(
                side="right",
                padx=(15, 0)
            )

    def update_task_completion(task_index, completed_variable):
        """Save a task's updated checkbox state."""

        tasks[task_index]["completed"] = completed_variable.get()
        save_tasks(tasks)
        show_active_tasks()

    def add_task():
        """Ask the user for a task and add it to the active list."""

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
                show_active_tasks()

    def delete_task(task_index):
        """Permanently remove an active task."""

        task_text = tasks[task_index]["text"]

        confirmed = messagebox.askyesno(
            "Delete Task",
            f'Are you sure you want to delete "{task_text}"?'
        )

        if confirmed:
            tasks.pop(task_index)
            save_tasks(tasks)
            show_active_tasks()

    def archive_task(task_index):
        """Move an active task into the archive."""

        task = tasks.pop(task_index)

        archived_tasks.append(task)

        save_tasks(tasks)
        save_archived_tasks(archived_tasks)

        show_active_tasks()

    def restore_task(task_index):
        """Move an archived task back to the active task list."""

        task = archived_tasks.pop(task_index)

        tasks.append(task)

        save_archived_tasks(archived_tasks)
        save_tasks(tasks)

        show_archived_tasks()

    def delete_archived_task(task_index):
        """Permanently remove a task from the archive."""

        task_text = archived_tasks[task_index]["text"]

        confirmed = messagebox.askyesno(
            "Delete Archived Task",
            f'Permanently delete "{task_text}"?'
        )

        if confirmed:
            archived_tasks.pop(task_index)
            save_archived_tasks(archived_tasks)
            show_archived_tasks()

    # Display active tasks when the app starts
    show_active_tasks()

    # Return functions that app.py and sidebar.py can use
    return {
        "add_task": add_task,
        "show_active_tasks": show_active_tasks,
        "show_archived_tasks": show_archived_tasks
    }
