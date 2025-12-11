# ui/dashboard.py

import tkinter as tk
from tkinter import ttk
from ui.actions_tab import ActionsTab
from ui.logs_tab import LogsTab
from ui.system_info_tab import SystemInfoTab
from core.logger import AuditLogger
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


LIGHT_MAROON_BG = "#f3e4e4"     # background for main workspace
DARK_MAROON = "#5a1a1a"         # main sidebar color
DARK_MAROON_HOVER = "#3c1111"   # hover shade
TEXT_LIGHT = "#f8eaea"          # light text for dark sidebar
TEXT_DARK = "#2a0c0c"           # headings


class Dashboard:
    def __init__(self, master, session, audit_logger: AuditLogger):
        self.master = master
        self.session = session
        self.audit_logger = audit_logger
        self._build_interface()

    def _build_interface(self):
        username = self.session["username"]
        self.master.title(f"Secure Interface — Logged in as {username}")

        # Main background
        self.master.configure(bg=LIGHT_MAROON_BG)

        # Root frame
        root_frame = tk.Frame(self.master, bg=LIGHT_MAROON_BG)
        root_frame.pack(fill="both", expand=True)

        # ---------------------
        # LEFT SIDEBAR (Dark)
        # ---------------------
        sidebar = tk.Frame(
            root_frame,
            width=180,
            bg=DARK_MAROON,
            padx=12,
            pady=12
        )
        sidebar.pack(side="left", fill="y")

        # Sidebar title/logo
        title_label = tk.Label(
            sidebar,
            text=f"DASHBOARD",
            fg=TEXT_LIGHT,
            bg=DARK_MAROON,
            font=_font(18)
        )
        title_label.pack(anchor="center", pady=(0, 20))

        # ---------------
        # CONTENT AREA
        # ---------------
        content = tk.Frame(root_frame, bg=LIGHT_MAROON_BG)
        content.pack(side="left", fill="both", expand=True)

        # Notebook (Tabs)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=LIGHT_MAROON_BG, padding=6)
        style.configure("TNotebook.Tab", font=_font(12), padding=[10, 6])
        style.map("TNotebook.Tab",
                  background=[("selected", "#d9bcbc")],
                  foreground=[("selected", "#2a0c0c")])

        self.notebook = ttk.Notebook(content)
        self.notebook.pack(fill="both", expand=True, padx=12, pady=12)

        self.actions_frame = tk.Frame(self.notebook, bg=LIGHT_MAROON_BG)
        self.logs_frame = tk.Frame(self.notebook, bg=LIGHT_MAROON_BG)
        self.sysinfo_frame = tk.Frame(self.notebook, bg=LIGHT_MAROON_BG)

        self.notebook.add(self.actions_frame, text="⚡ Actions")
        self.notebook.add(self.logs_frame, text="📜 Logs")
        self.notebook.add(self.sysinfo_frame, text="💻 System Info")

        # ---------------------------------
        # Sidebar Buttons (Styled + Icons)
        # ---------------------------------
        def sidebar_btn(text, icon, command):
            frame = tk.Frame(sidebar, bg=DARK_MAROON)
            btn = tk.Button(
                frame,
                text=f"{icon}  {text}",
                font=_font(13),
                bg=DARK_MAROON,
                fg=TEXT_LIGHT,
                activebackground=DARK_MAROON_HOVER,
                bd=0,
                cursor="hand2",
                command=command,
                anchor="w",
                padx=10
            )
            btn.pack(fill="x")

            # Hover effects
            btn.bind("<Enter>", lambda e: btn.configure(bg=DARK_MAROON_HOVER))
            btn.bind("<Leave>", lambda e: btn.configure(bg=DARK_MAROON))

            frame.pack(fill="x", pady=6)
            return btn

        btn_actions = sidebar_btn("Actions", "⚡", lambda: self._select_tab(0))
        btn_logs = sidebar_btn("Logs", "📜", lambda: self._select_tab(1))
        btn_sysinfo = sidebar_btn("System Info", "💻", lambda: self._select_tab(2))

        # -------------------------
        # Logout Button (Bottom)
        # -------------------------
        logout_frame = tk.Frame(sidebar, bg=DARK_MAROON)
        logout_frame.pack(side="bottom", fill="x", pady=(20, 6))

        btn_logout = tk.Button(
            logout_frame,
            text="🚪 Logout",
            font=_font(13),
            bg="#7a1f1f",
            fg="white",
            activebackground="#571414",
            bd=0,
            cursor="hand2",
            command=self._logout
        )
        btn_logout.pack(fill="x", padx=6, pady=6)

        # ---------------------------------
        # Instantiate Tab Content (same logic)
        # ---------------------------------
        ActionsTab(self.actions_frame, self.session, self.audit_logger)
        LogsTab(self.logs_frame, self.audit_logger)
        SystemInfoTab(self.sysinfo_frame)

    def _select_tab(self, index: int):
        self.notebook.select(index)

    def _logout(self):
        self.master.destroy()
