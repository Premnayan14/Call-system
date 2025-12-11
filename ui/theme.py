# ui/theme.py

import tkinter as tk
from tkinter import ttk

def apply_dark_theme(root: tk.Tk):
    """
    Apply a minimal dark-ish theme by setting background colors and
    ttk style tweaks. This is intentionally unobtrusive and portable.
    """
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # general colors
    bg = "#2e2e2e"
    fg = "#eaeaea"
    entry_bg = "#3b3b3b"
    accent = "#5aa9ff"

    root.configure(bg=bg)

    # configure ttk styles
    style.configure("TLabel", background=bg, foreground=fg)
    style.configure("TFrame", background=bg)
    style.configure("TButton", padding=6)
    style.configure("TNotebook", background=bg)
    style.configure("TNotebook.Tab", background="#3b3b3b", foreground=fg)
    style.map("TButton",
              background=[("active", accent)],
              foreground=[("active", "#ffffff")])

    # configure classic widgets where possible
    root.option_add("*Button.background", "#3b3b3b")
    root.option_add("*Button.foreground", fg)
    root.option_add("*Label.background", bg)
    root.option_add("*Label.foreground", fg)
    root.option_add("*Entry.background", entry_bg)
    root.option_add("*Entry.foreground", fg)
    root.option_add("*Text.background", entry_bg)
    root.option_add("*Text.foreground", fg)
