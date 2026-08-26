import tkinter as tk


def create_sidebar(
    parent,
    show_active_tasks=None,
    show_archived_tasks=None
):
    sidebar = tk.Frame(
        parent,
        width=140,
        bg="#A8D0DF"
    )
    sidebar.pack(
        side="left",
        fill="y"
    )

    sidebar.pack_propagate(False)

    todo_button = tk.Button(
        sidebar,
        text="Todo",
        width=14,
        command=show_active_tasks
    )
    todo_button.pack(
        pady=(15, 5)
    )

    routine_button = tk.Button(
        sidebar,
        text="Routine",
        width=14
    )
    routine_button.pack(
        pady=5
    )

    archive_button = tk.Button(
        sidebar,
        text="Archive",
        width=14,
        command=show_archived_tasks
    )
    archive_button.pack(
        pady=5
    )

    settings_button = tk.Button(
        sidebar,
        text="Settings",
        width=14
    )
    settings_button.pack(
        pady=5
    )

    return sidebar
