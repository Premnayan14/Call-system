# ui/dashboard.py

import tkinter as tk
from tkinter import ttk
from ui.actions_tab import ActionsTab
from ui.logs_tab import LogsTab
from ui.system_info_tab import SystemInfoTab
from core.logger import AuditLogger


class Dashboard:
    def __init__(self, master, session, audit_logger: AuditLogger):
        self.master = master
        self.session = session
        self.audit_logger = audit_logger
        self._build_interface()

    def _build_interface(self):
        self.master.title(f"Secure Interface — Logged in as {self.session['username']}")

        root_frame = tk.Frame(self.master)
        root_frame.pack(fill="both", expand=True)

        # Left sidebar
        sidebar = tk.Frame(root_frame, width=160, padx=8, pady=8)
        sidebar.pack(side="left", fill="y")

        content = tk.Frame(root_frame)
        content.pack(side="left", fill="both", expand=True)

        # Notebook in content
        self.notebook = ttk.Notebook(content)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.actions_frame = tk.Frame(self.notebook)
        self.logs_frame = tk.Frame(self.notebook)
        self.sysinfo_frame = tk.Frame(self.notebook)

        self.notebook.add(self.actions_frame, text="Actions")
        self.notebook.add(self.logs_frame, text="Logs")
        self.notebook.add(self.sysinfo_frame, text="System Info")

        # Sidebar buttons that change notebook tab
        btn_actions = tk.Button(sidebar, text="Actions", width=18, command=lambda: self._select_tab(0))
        btn_logs = tk.Button(sidebar, text="Logs", width=18, command=lambda: self._select_tab(1))
        btn_sysinfo = tk.Button(sidebar, text="System Info", width=18, command=lambda: self._select_tab(2))
        btn_logout = tk.Button(sidebar, text="Logout", width=18, command=self._logout)

        btn_actions.pack(pady=(6, 4))
        btn_logs.pack(pady=4)
        btn_sysinfo.pack(pady=4)
        btn_logout.pack(side="bottom", pady=8)

        # instantiate tab content
        ActionsTab(self.actions_frame, self.session, self.audit_logger)
        LogsTab(self.logs_frame, self.audit_logger)
        SystemInfoTab(self.sysinfo_frame)

    def _select_tab(self, index: int):
        self.notebook.select(index)

    def _logout(self):
        # Simple logout: destroy window. A more advanced flow could return to login.
        self.master.destroy()
