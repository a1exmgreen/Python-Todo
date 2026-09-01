import tkinter as tk
from tkinter import messagebox, simpledialog

import customtkinter as ctk

from theme import COLORS

from storage import (
    load_tasks,
    save_tasks,
    load_archived_tasks,
    save_archived_tasks,
    load_completed_tasks,
    save_completed_tasks
)


# Tkinter measures delays in milliseconds.
# 3000 milliseconds equals 3 seconds.
COMPLETION_DELAY = 3000


def create_task_manager(parent, title_label):
    tasks = load_tasks()
    archived_tasks = load_archived_tasks()
    completed_tasks = load_completed_tasks()

    # Remember which page is currently displayed.
    current_page = {
        "name": "todo"
    }

    def clear_task_area():
        """Remove all widgets currently displayed in the task area."""

        for widget in parent.winfo_children():
            widget.destroy()

    def create_counter_label(text):
        """Display a small counter at the top of a page."""

        counter_label = ctk.CTkLabel(
            parent,
            text=text,
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

    def create_empty_label(text):
        """Display a message when the current page has no tasks."""

        empty_label = ctk.CTkLabel(
            parent,
            text=text,
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

    def show_active_tasks():
        """Display all active tasks."""

        current_page["name"] = "todo"

        title_label.configure(
            text="Today's Tasks"
        )

        clear_task_area()

        completing_count = sum(
            1 for task in tasks if task["completed"]
        )

        remaining_count = len(tasks) - completing_count

        create_counter_label(
            f"{remaining_count} remaining"
            f" • {completing_count} completing"
        )

        if not tasks:
            create_empty_label(
                "No active tasks. "
                "Add your first task to get started."
            )
            return

        for task in tasks:
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

            task_card.pack_propagate(False)

            completed_variable = tk.BooleanVar(
                value=task["completed"]
            )

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
                command=lambda selected_task=task,
                variable=completed_variable:
                update_task_completion(
                    selected_task,
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
                command=lambda selected_task=task:
                delete_task(selected_task)
            )

            delete_button.pack(
                side="right",
                padx=(5, 14),
                pady=15
            )

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
                command=lambda selected_task=task:
                archive_task(selected_task)
            )

            archive_button.pack(
                side="right",
                padx=5,
                pady=15
            )

    def show_completed_tasks():
        """Display all completed tasks."""

        current_page["name"] = "completed"

        title_label.configure(
            text="Completed Tasks"
        )

        clear_task_area()

        create_counter_label(
            f"{len(completed_tasks)} completed"
        )

        if not completed_tasks:
            create_empty_label(
                "There are no completed tasks yet."
            )
            return

        for task in completed_tasks:
            completed_card = ctk.CTkFrame(
                parent,
                height=68,
                corner_radius=14,
                fg_color=COLORS["card"],
                border_width=1,
                border_color=COLORS["border"]
            )

            completed_card.pack(
                fill="x",
                pady=6,
                padx=(0, 5)
            )

            completed_card.pack_propagate(False)

            task_label = ctk.CTkLabel(
                completed_card,
                text=task["text"],
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=14,
                    overstrike=True
                ),
                text_color=COLORS["text_secondary"],
                anchor="w"
            )

            task_label.pack(
                side="left",
                fill="x",
                expand=True,
                padx=(18, 10),
                pady=15
            )

            reopen_button = ctk.CTkButton(
                completed_card,
                text="Re-open",
                width=88,
                height=34,
                corner_radius=9,
                font=ctk.CTkFont(
                    family="Segoe UI",
                    size=12,
                    weight="bold"
                ),
                fg_color=COLORS["success"],
                hover_color=COLORS["success_hover"],
                command=lambda selected_task=task:
                reopen_completed_task(selected_task)
            )

            reopen_button.pack(
                side="right",
                padx=14,
                pady=15
            )

    def show_archived_tasks():
        """Display all archived tasks."""

        current_page["name"] = "archive"

        title_label.configure(
            text="Archived Tasks"
        )

        clear_task_area()

        create_counter_label(
            f"{len(archived_tasks)} archived"
        )

        if not archived_tasks:
            create_empty_label(
                "There are no archived tasks."
            )
            return

        for task in archived_tasks:
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

            archived_card.pack_propagate(False)

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
                command=lambda selected_task=task:
                delete_archived_task(selected_task)
            )

            delete_button.pack(
                side="right",
                padx=(5, 14),
                pady=15
            )

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
                command=lambda selected_task=task:
                restore_task(selected_task)
            )

            restore_button.pack(
                side="right",
                padx=5,
                pady=15
            )

    def refresh_current_page():
        """Refresh whichever page the user is currently viewing."""

        if current_page["name"] == "completed":
            show_completed_tasks()

        elif current_page["name"] == "archive":
            show_archived_tasks()

        else:
            show_active_tasks()

    def update_task_completion(
        selected_task,
        completed_variable
    ):
        """Update a task and schedule completed tasks to move."""

        if selected_task not in tasks:
            return

        selected_task["completed"] = (
            completed_variable.get()
        )

        save_tasks(tasks)

        # Redraw immediately so the strikethrough appears.
        show_active_tasks()

        if selected_task["completed"]:
            parent.after(
                COMPLETION_DELAY,
                lambda task_to_move=selected_task:
                move_to_completed(task_to_move)
            )

    def move_to_completed(selected_task):
        """Move a checked task from Todo into Completed."""

        # The task may have been archived or deleted.
        if selected_task not in tasks:
            return

        # The task may have been unchecked during the delay.
        if not selected_task["completed"]:
            return

        tasks.remove(selected_task)

        selected_task["completed"] = True
        completed_tasks.append(selected_task)

        save_tasks(tasks)
        save_completed_tasks(completed_tasks)

        refresh_current_page()

    def reopen_completed_task(selected_task):
        """Move a completed task back into Todo."""

        if selected_task not in completed_tasks:
            return

        completed_tasks.remove(selected_task)

        selected_task["completed"] = False
        tasks.append(selected_task)

        save_completed_tasks(completed_tasks)
        save_tasks(tasks)

        show_completed_tasks()

    def add_task():
        """Ask the user for a task and add it to Todo."""

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

    def delete_task(selected_task):
        """Permanently remove an active task."""

        if selected_task not in tasks:
            return

        confirmed = messagebox.askyesno(
            "Delete Task",
            (
                "Are you sure you want to delete "
                f'"{selected_task["text"]}"?'
            )
        )

        if confirmed:
            tasks.remove(selected_task)
            save_tasks(tasks)
            show_active_tasks()

    def archive_task(selected_task):
        """Move an active task into the archive."""

        if selected_task not in tasks:
            return

        tasks.remove(selected_task)

        # Cancel a pending move into Completed.
        selected_task["completed"] = False

        archived_tasks.append(selected_task)

        save_tasks(tasks)
        save_archived_tasks(archived_tasks)

        show_active_tasks()

    def restore_task(selected_task):
        """Move an archived task back into Todo."""

        if selected_task not in archived_tasks:
            return

        archived_tasks.remove(selected_task)

        selected_task["completed"] = False
        tasks.append(selected_task)

        save_archived_tasks(archived_tasks)
        save_tasks(tasks)

        show_archived_tasks()

    def delete_archived_task(selected_task):
        """Permanently remove a task from the archive."""

        if selected_task not in archived_tasks:
            return

        confirmed = messagebox.askyesno(
            "Delete Archived Task",
            (
                "Permanently delete "
                f'"{selected_task["text"]}"?'
            )
        )

        if confirmed:
            archived_tasks.remove(selected_task)
            save_archived_tasks(archived_tasks)
            show_archived_tasks()

    # Display Todo when the application starts.
    show_active_tasks()

    # Give app.py and sidebar.py access to these functions.
    return {
        "add_task": add_task,
        "show_active_tasks": show_active_tasks,
        "show_completed_tasks": show_completed_tasks,
        "show_archived_tasks": show_archived_tasks
    }