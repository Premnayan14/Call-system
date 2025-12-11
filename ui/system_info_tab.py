# ui/system_info_tab.py

import tkinter as tk
from tkinter import scrolledtext, ttk
from core.syscalls import SyscallEngine
import platform

# -------------------------
# Global Theme + Font Setup
# -------------------------
def _font(size=12, weight="bold"):
    if platform.system() == "Windows":
        base = "Segoe UI"
    else:
        base = "Arial"
    return (base, size, weight)

# Theme Colors
LIGHT_MAROON_BG = "#f3e4e4"
CARD_BG = "#2e0f0f"
INPUT_BG = "#fff6f6"
DARK_MAROON = "#5a1a1a"
DARK_MAROON_HOVER = "#3d1111"
TEXT_LIGHT = "#f8eaea"
TEXT_DARK = "#2a0c0c"


class SystemInfoTab:
    def __init__(self, master):
        self.master = master
        self._build_interface()
        self._refresh_info()

    def _build_interface(self):
        # Main area background
        frame = tk.Frame(self.master, bg=LIGHT_MAROON_BG)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        # Card container
        card = tk.Frame(frame, bg=INPUT_BG, bd=0, padx=14, pady=14)
        card.pack(fill="both", expand=True)

        # Title row
        title_row = tk.Frame(card, bg=INPUT_BG)
        title_row.pack(fill="x", pady=(0, 10))

        tk.Label(
            title_row,
            text="System Information",
            bg=INPUT_BG,
            fg=TEXT_DARK,
            font=_font(16)
        ).pack(side="left", anchor="w")

        # Styled Refresh button
        refresh_btn = tk.Button(
            title_row,
            text="⟳ Refresh",
            font=_font(12),
            bg=DARK_MAROON,
            fg=TEXT_LIGHT,
            activebackground=DARK_MAROON_HOVER,
            bd=0,
            pady=6,
            padx=12,
            cursor="hand2",
            command=self._refresh_info
        )
        refresh_btn.pack(side="right", padx=4)

        # Hover effect
        refresh_btn.bind("<Enter>", lambda e: refresh_btn.configure(bg=DARK_MAROON_HOVER))
        refresh_btn.bind("<Leave>", lambda e: refresh_btn.configure(bg=DARK_MAROON))

        # Output text area
        self.text_box = scrolledtext.ScrolledText(
            card,
            width=100,
            height=20,
            font=("Consolas", 11),
            bg="white",
            fg="#1a1a1a",
            relief="flat",
            padx=10,
            pady=10
        )
        self.text_box.pack(fill="both", expand=True, pady=(8, 0))
        self.text_box.configure(state="disabled")

    # ---------------------------------------
    # Refresh System Information (same logic)
    # ---------------------------------------
    def _refresh_info(self):
        success, info = SyscallEngine.system_info()
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", tk.END)

        if success:
            self.text_box.insert("1.0", info)
        else:
            self.text_box.insert("1.0", f"Failed to obtain system information:\n{info}")

        self.text_box.configure(state="disabled")
