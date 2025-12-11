# ui/theme.py

import tkinter as tk
from tkinter import ttk
import platform

# Font helper (same as other screens)
def _font(size=12, weight="bold"):
    if platform.system() == "Windows":
        base = "Segoe UI"
    else:
        base = "Arial"
    return (base, size, weight)

# Global Theme Colors
LIGHT_MAROON_BG = "#f3e4e4"
CARD_BG = "#2e0f0f"
INPUT_BG = "#fff6f6"
DARK_MAROON = "#5a1a1a"
DARK_MAROON_HOVER = "#3d1111"
TEXT_LIGHT = "#f8eaea"
TEXT_DARK = "#2a0c0c"


def apply_dark_theme(root: tk.Tk):
    """
    Apply the **Dark Maroon UI Theme** across the entire application.
    This theme is consistent with Login, Dashboard, Actions, Logs, and System Info tabs.
    """

    # -------------------------
    # Root Background
    # -------------------------
    root.configure(bg=LIGHT_MAROON_BG)

    # -------------------------
    # TTK Style Configuration
    # -------------------------
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Notebook (tabs)
    style.configure(
        "TNotebook",
        background=LIGHT_MAROON_BG,
        borderwidth=0,
        padding=6
    )

    style.configure(
        "TNotebook.Tab",
        background=INPUT_BG,
        foreground=TEXT_DARK,
        padding=[14, 6],
        font=_font(12)
    )

    style.map(
        "TNotebook.Tab",
        background=[("selected", "#e2c6c6")],
        foreground=[("selected", TEXT_DARK)]
    )

    # Buttons
    style.configure(
        "TButton",
        font=_font(11),
        padding=8
    )

    style.map(
        "TButton",
        background=[("active", DARK_MAROON_HOVER), ("!active", DARK_MAROON)],
        foreground=[("active", TEXT_LIGHT), ("!active", TEXT_LIGHT)]
    )

    # Labels
    style.configure(
        "TLabel",
        background=LIGHT_MAROON_BG,
        foreground=TEXT_DARK,
        font=_font(12)
    )

    # Frame background
    style.configure(
        "TFrame",
        background=LIGHT_MAROON_BG
    )

    # Entries
    style.configure(
        "TEntry",
        fieldbackground=INPUT_BG,
        background=INPUT_BG,
        foreground=TEXT_DARK,
        font=_font(11)
    )

    # -------------------------
    # Classic Tk Widgets (fallback)
    # -------------------------
    root.option_add("*Label.background", LIGHT_MAROON_BG)
    root.option_add("*Label.foreground", TEXT_DARK)

    root.option_add("*Frame.background", LIGHT_MAROON_BG)

    root.option_add("*Button.background", DARK_MAROON)
    root.option_add("*Button.foreground", TEXT_LIGHT)

    root.option_add("*Entry.background", INPUT_BG)
    root.option_add("*Entry.foreground", TEXT_DARK)

    root.option_add("*Text.background", "white")
    root.option_add("*Text.foreground", TEXT_DARK)
