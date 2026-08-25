import tkinter as tk

def create_sidebar(parent):
    sidebar = tk.Frame(
        parent,
        width=200,
        bg="#A6C8D8"
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    buttons = [
        "Todo",
        "Routine",
        "Event",
        "Checklist",
        "Settings"
    ]

    for item in buttons:
        btn = tk.Button(
            sidebar,
            text=item,
            width=12
        )
        btn.pack(
            pady=10
        )

    return sidebar