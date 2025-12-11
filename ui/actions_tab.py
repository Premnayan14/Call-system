# ui/actions_tab.py

import tkinter as tk
from tkinter import scrolledtext
from core.syscalls import SyscallEngine


class ActionsTab:
    def __init__(self, master, session, audit_logger):
        self.master = master
        self.session = session
        self.audit_logger = audit_logger
        self._build_interface()

    # ----------------------------------------------------
    def _is_allowed(self, action):
        """Check if the user's role allows the given action."""
        return action in self.session["permissions"]

    def _log_and_show(self, success, action, result):
        status = "success" if success else "failed"
        self.audit_logger.record(self.session["username"], action, status)

        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, f"{result}")
        self.output_box.configure(state="normal")

    # ----------------------------------------------------
    def _build_interface(self):
        """Main layout builder with corrected frame handling."""
        frame = tk.Frame(self.master)
        frame.pack(fill="both", expand=True)

        # Configure grid so widgets expand
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # ------------------ Output area ------------------
        self.output_box = scrolledtext.ScrolledText(
            frame, width=80, height=20, font=("Consolas", 11)
        )
        self.output_box.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        # ------------------ Buttons area -----------------
        permitted_actions = [
            p for p in self.session["permissions"]
            if p in ["read_file", "write_file", "list_processes", "spawn_process", "ping_host"]
        ]

        if not permitted_actions:
            # Guest user or restricted role
            self.output_box.insert(
                tk.END,
                "⚠ This user role has no permission to perform system actions."
            )
            self.output_box.configure(state="disabled")
            return

        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        btn_frame.grid_columnconfigure(0, weight=1)

        actions = [
            ("Read File", "read_file", self._action_read_file),
            ("Write File", "write_file", self._action_write_file),
            ("List Processes", "list_processes", self._action_list_processes),
            ("Spawn Process", "spawn_process", self._action_spawn_process),
            ("Ping Host", "ping_host", self._action_ping_host),
        ]

        for label, action_name, callback in actions:
            state = tk.NORMAL if self._is_allowed(action_name) else tk.DISABLED
            tk.Button(
                btn_frame,
                text=label,
                width=15,
                command=callback,
                state=state
            ).pack(side="left", padx=5)

    # ----------------------------------------------------
    # ACTION HANDLERS
    # ----------------------------------------------------

    def _action_read_file(self):
        path = self._prompt("Enter file path to read:")
        if not path:
            return
        success, result = SyscallEngine.read_file(path)
        self._log_and_show(success, "read_file", result)

    def _action_write_file(self):
        path = self._prompt("Enter file path to write:")
        if not path:
            return
        text = self._prompt("Enter text to write:")
        if text is None:
            return
        success, result = SyscallEngine.write_file(path, text)
        self._log_and_show(success, "write_file", result)

    def _action_list_processes(self):
        success, result = SyscallEngine.list_processes()
        self._log_and_show(success, "list_processes", result)

    def _action_spawn_process(self):
        command = self._prompt("Enter command to run (example: notepad):")
        if not command:
            return
        success, result = SyscallEngine.spawn_process(command)
        self._log_and_show(success, "spawn_process", result)

    def _action_ping_host(self):
        host = self._prompt("Enter hostname/IP to ping:")
        if not host:
            return
        success, result = SyscallEngine.ping_host(host)
        self._log_and_show(success, "ping_host", result)

    # ----------------------------------------------------
    # PROMPT DIALOG
    # ----------------------------------------------------
    def _prompt(self, message):
        """Small popup dialog for user input."""
        win = tk.Toplevel(self.master)
        win.title("Input Required")
        win.geometry("350x150")
        win.grab_set()

        tk.Label(win, text=message, font=("Segoe UI", 10)).pack(pady=10)

        entry = tk.Entry(win, width=40)
        entry.pack(pady=5)

        value = {"result": None}

        def submit():
            value["result"] = entry.get().strip()
            win.destroy()

        tk.Button(win, text="Submit", width=12, command=submit).pack(pady=10)
        win.wait_window()

        return value["result"]
