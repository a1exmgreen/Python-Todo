import customtkinter as ctk

from theme import COLORS


def create_sidebar(
    parent,
    show_active_tasks=None,
    show_archived_tasks=None
):
    sidebar = ctk.CTkFrame(
        parent,
        width=210,
        corner_radius=0,
        fg_color=COLORS["sidebar"]
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    # Prevent the sidebar from shrinking to fit its contents
    sidebar.pack_propagate(False)

    # App name
    app_title = ctk.CTkLabel(
        sidebar,
        text="Task Manager",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=21,
            weight="bold"
        ),
        text_color="#FFFFFF"
    )

    app_title.pack(
        anchor="w",
        padx=22,
        pady=(30, 4)
    )

    # Small description beneath the app name
    app_subtitle = ctk.CTkLabel(
        sidebar,
        text="Organise your day",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=12
        ),
        text_color="#9CA3AF"
    )

    app_subtitle.pack(
        anchor="w",
        padx=22,
        pady=(0, 28)
    )

    # Navigation heading
    navigation_label = ctk.CTkLabel(
        sidebar,
        text="NAVIGATION",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=11,
            weight="bold"
        ),
        text_color="#9CA3AF"
    )

    navigation_label.pack(
        anchor="w",
        padx=22,
        pady=(0, 8)
    )

    # Store references to the navigation buttons
    navigation_buttons = {}

    def set_active_button(active_name):
        """
        Highlight the selected page and reset the other buttons.
        """

        for button_name, button in navigation_buttons.items():
            if button_name == active_name:
                button.configure(
                    fg_color=COLORS["sidebar_active"],
                    hover_color=COLORS["sidebar_active"]
                )
            else:
                button.configure(
                    fg_color="transparent",
                    hover_color=COLORS["sidebar_hover"]
                )

    def open_todo_page():
        set_active_button("Todo")

        if show_active_tasks:
            show_active_tasks()

    def open_archive_page():
        set_active_button("Archive")

        if show_archived_tasks:
            show_archived_tasks()

    def unavailable_page(page_name):
        set_active_button(page_name)

    # Todo button
    todo_button = ctk.CTkButton(
        sidebar,
        text="  Todo",
        anchor="w",
        height=42,
        corner_radius=10,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=14,
            weight="bold"
        ),
        fg_color=COLORS["sidebar_active"],
        hover_color=COLORS["sidebar_active"],
        command=open_todo_page
    )

    todo_button.pack(
        fill="x",
        padx=15,
        pady=4
    )

    navigation_buttons["Todo"] = todo_button

    # Routine button
    routine_button = ctk.CTkButton(
        sidebar,
        text="  Routine",
        anchor="w",
        height=42,
        corner_radius=10,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=14
        ),
        fg_color="transparent",
        hover_color=COLORS["sidebar_hover"],
        command=lambda: unavailable_page("Routine")
    )

    routine_button.pack(
        fill="x",
        padx=15,
        pady=4
    )

    navigation_buttons["Routine"] = routine_button

    # Archive button
    archive_button = ctk.CTkButton(
        sidebar,
        text="  Archive",
        anchor="w",
        height=42,
        corner_radius=10,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=14
        ),
        fg_color="transparent",
        hover_color=COLORS["sidebar_hover"],
        command=open_archive_page
    )

    archive_button.pack(
        fill="x",
        padx=15,
        pady=4
    )

    navigation_buttons["Archive"] = archive_button

    # Settings button
    settings_button = ctk.CTkButton(
        sidebar,
        text="  Settings",
        anchor="w",
        height=42,
        corner_radius=10,
        font=ctk.CTkFont(
            family="Segoe UI",
            size=14
        ),
        fg_color="transparent",
        hover_color=COLORS["sidebar_hover"],
        command=lambda: unavailable_page("Settings")
    )

    settings_button.pack(
        fill="x",
        padx=15,
        pady=4
    )

    navigation_buttons["Settings"] = settings_button

    # Sidebar footer
    footer = ctk.CTkLabel(
        sidebar,
        text="Python Todo App",
        font=ctk.CTkFont(
            family="Segoe UI",
            size=11
        ),
        text_color="#6B7280"
    )

    footer.pack(
        side="bottom",
        anchor="w",
        padx=22,
        pady=20
    )

    return sidebar