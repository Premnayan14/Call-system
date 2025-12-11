# ui/login_page.py

import tkinter as tk
from tkinter import messagebox
from ui.dashboard import Dashboard


class LoginPage:
    def __init__(self, master, security_controller, audit_logger):
        self.master = master
        self.security_controller = security_controller
        self.audit_logger = audit_logger

        self.frame = tk.Frame(master, padx=20, pady=20)
        self.frame.pack(expand=True)

        self._build_interface()

    def _build_interface(self):
        tk.Label(self.frame, text="User Authentication", font=("Segoe UI", 16, "bold")).pack(pady=10)

        tk.Label(self.frame, text="Username:", font=("Segoe UI", 11)).pack(anchor="w")
        self.entry_username = tk.Entry(self.frame, width=30)
        self.entry_username.pack(pady=5)

        tk.Label(self.frame, text="Password:", font=("Segoe UI", 11)).pack(anchor="w")
        self.entry_password = tk.Entry(self.frame, show="*", width=30)
        self.entry_password.pack(pady=5)

        tk.Button(
            self.frame,
            text="Login",
            font=("Segoe UI", 11),
            width=12,
            command=self._attempt_login
        ).pack(pady=15)

    def _attempt_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        session = self.security_controller.authenticate(username, password)

        if session:
            self.audit_logger.record(username, "login", "success")
            self.frame.destroy()
            Dashboard(self.master, session, self.audit_logger)
        else:
            self.audit_logger.record(username, "login", "failed")
            messagebox.showerror("Authentication Failed", "Invalid username or password.")
