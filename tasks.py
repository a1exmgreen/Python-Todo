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
        """Remove all widgets currently displayed in the task area."""

        for widget in parent.winfo_children():
            widget.destroy()

    def show_active_tasks():
        """Display all active tasks."""

        title_label.configure(text="Today's Tasks")
        clear_task_area()

        # Count completed and remaining tasks
        completed_count = sum(
            1 for task in tasks if task["completed"]
        )

        remaining_count = len(tasks) - completed_count

        # Display the task counter
        counter_label = ctk.CTkLabel(
            parent,
            text=(
                f"{remaining_count} remaining"
                f" • {completed_count} completed"
            ),
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

        # Display an empty-state message
        if not tasks:
            empty_label = ctk.CTkLabel(
                parent,
                text=(
                    "No active tasks."
                    "Add your first task to get started."
                ),
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=14
                ),
                text_color=COLORS["text_secondary"]
            )

            empty_label.pack(
                anchor="w",
                pady=10
            )

            return

        # Create a modern card for every active task
        for index, task in enumerate(tasks):
            task_card = ctk.CTkFrame(
                parent,
                height=68,
                corner_radius=14,
                fg_color=COLORS["card"],
                border_width=1,
                border_color=COLORS["border"]
            )

            task_card.pack(
                fill="x",
                pady=6,
                padx=(0, 5)
            )

            # Keep every card at a consistant height
            task_card.pack_propagate(False)

            # Store the checkbox state
            completed_variable = tk.BooleanVar(
                value=task["completed"]
            )

            # Style completed and incomplete tasks differently
            if task["completed"]:
                task_font = ctk.CTkFont(
                    family="Segoe UI",
                    size=14,
                    overstrike=True
                )

                task_colour = COLORS["text_secondary"]

            else:
                task_font = ctk.CTkFont(
                    family="Segoe UI",
                    size=14
                )

                task_colour = COLORS["text"]

            # Modern task checkbox
            checkbox = ctk.CTkCheckBox(
                task_card,
                text=task["text"],
                variable=completed_variable,
                font=task_font,
                text_color=task_colour,
                checkbox_width=22,
                checkbox_height=22,
                corner_radius=6,
                border_width=2,
                fg_color=COLORS["primary"],
                hover_color=COLORS["primary_hover"],
                border_color=COLORS["text_secondary"],
                command=lambda task_index=index,
                variable=completed_variable:
                update_task_completion(
                    task_index,
                    variable
                )
            )

            checkbox.pack(
                side="left",
                fill="x",
                expand=True,
                padx=(18, 10),
                pady=15
            )

            # Delete button
            delete_button = ctk.CTkButton(
                task_card,
                text="Delete",
                width=76,
                height=34,
                corner_radius=9,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=12,
                    weight="bold"
                ),
                fg_color=COLORS["delete"],
                hover_color=COLORS["delete_hover"],
                command=lambda task_index=index:
                delete_task(task_index)
            )

            delete_button.pack(
                side="right",
                padx=(5, 14),
                pady=15
            )

            # Archive button
            archive_button = ctk.CTkButton(
                task_card,
                text="Archive",
                width=82,
                height=34,
                corner_radius=9,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=12,
                    weight="bold"
                ),
                fg_color=COLORS["archive"],
                hover_color=COLORS["archive_hover"],
                command=lambda task_index=index:
                archive_task(task_index)
            )

            archive_button.pack(
                side="right",
                padx=5,
                pady=15
            )

    def show_archived_tasks():
        """Display all archived tasks."""

        title_label.configure(text="Archived Tasks")
        clear_task_area()

        # Display the archived task counter
        archived_count_label = ctk.CTkLabel(
            parent,
            text=f"{len(archived_tasks)} archived",
            font=ctk.CTkFont(
                family="Segoe UI",
                size=12
            ),
            text_color=COLORS["text_secondary"]
        )

        archived_count_label.pack(
            anchor="w",
            pady=(0, 10)
        )

        # Display an empty-state message
        if not archived_tasks:
            empty_label = ctk.CTkLabel(
                parent,
                text="There are no archived tasks.",
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=14
                ),
                text_color=COLORS["text_secondary"]
            )

            empty_label.pack(
                anchor="w",
                pady=10
            )

            return

        # Create a modern card for every archived task
        for index, task in enumerate(archived_tasks):
            archived_card = ctk.CTkFrame(
                parent,
                height=68,
                corner_radius=14,
                fg_color=COLORS["card"],
                border_width=1,
                border_color=COLORS["border"]
            )

            archived_card.pack(
                fill="x",
                pady=6,
                padx=(0, 5)
            )

            # Keep every archived card at a consistent height
            archived_card.pack_propagate(False)

            # Archived task name
            task_label = ctk.CTkLabel(
                archived_card,
                text=task["text"],
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=14
                ),
                text_color=COLORS["text"],
                anchor="w"
            )

            task_label.pack(
                side="left",
                fill="x",
                expand=True,
                padx=(18, 10),
                pady=15
            )

            # Permanetly delete archived task
            delete_button = ctk.CTkButton(
                archived_card,
                text="Delete",
                width=76,
                height=34,
                corner_radius=9,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=12,
                    weight="bold"
                ),
                fg_color=COLORS["delete"],
                hover_color=COLORS["delete_hover"],
                command=lambda task_index=index:
                delete_archived_task(task_index)
            )

            delete_button.pack(
                side="right",
                padx=(5, 14),
                pady=15
            )

            # Restore archived task
            restore_button = ctk.CTkButton(
                archived_card,
                text="Restore",
                width=82,
                height=34,
                corner_radius=9,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=12,
                    weight="bold"
                ),
                fg_color=COLORS["success"],
                hover_color=COLORS["success_hover"],
                command=lambda task_index=index:
                restore_task(task_index)
            )

            restore_button.pack(
                side="right",
                padx=5,
                pady=15
            )

    def update_task_completion(
            task_index,
            completed_variable
    ):
        """Save a task's updated checkbox state."""

        tasks[task_index]["completed"] = (
            completed_variable.get()
        )

        save_tasks(tasks)

        # Refresh the page to update styling and totals
        show_active_tasks()

    def add_task():
        """Ask the user for a task and add it to the active list."""

        new_task = simpledialog.askstring(
            "Add Task",
            "What task would you like to add?"
        )

        # Pressing cancel returns None
        if new_task:
            new_task = new_task.strip()

            # Prevent empty or whitespace only tasks
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
            f'Are you sure you wan to delete "{task_text}"?'
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
        """Move an archived task back into the active task list."""

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

    # Display active tasks when the application opens
    show_active_tasks()

    # Give app.py and sidebar.py access to these functions
    return {
        "add_task": add_task,
        "show_active_tasks": show_active_tasks,
        "show_archived_tasks": show_archived_tasks
    }