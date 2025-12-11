# ui/actions_tab.py

import tkinter as tk
from tkinter import scrolledtext, ttk, messagebox
from core.syscalls import SyscallEngine
import platform

# Theme + font helpers (match dashboard/login theme)
def _font(size=12, weight="bold"):
    if platform.system() == "Windows":
        base = "Segoe UI"
    else:
        base = "Arial"
    return (base, size, weight)


# Colors (consistent with dark-maroon theme)
LIGHT_MAROON_BG = "#f3e4e4"
CARD_BG = "#2e0f0f"
INPUT_BG = "#fff6f6"
DARK_MAROON = "#5a1a1a"
DARK_MAROON_HOVER = "#3d1111"
TEXT_LIGHT = "#f8eaea"
TEXT_DARK = "#2a0c0c"


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

        # show result in output box (preserve original behavior: writable while writing)
        self.output_box.configure(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, f"{result}")
        # keep editable state as original code did (left as normal)
        self.output_box.configure(state="normal")

    # ----------------------------------------------------
    def _build_interface(self):
        """Main layout builder with corrected frame handling and themed visuals."""
        frame = tk.Frame(self.master, bg=LIGHT_MAROON_BG)
        frame.pack(fill="both", expand=True)

        # Use internal card area for content to match other screens
        card = tk.Frame(frame, bg=INPUT_BG, bd=0, padx=12, pady=12)
        card.pack(fill="both", expand=True, padx=12, pady=12)

        # Title row
        title_row = tk.Frame(card, bg=INPUT_BG)
        title_row.pack(fill="x", pady=(0, 8))
        tk.Label(
            title_row,
            text="Actions",
            bg=INPUT_BG,
            fg=TEXT_DARK,
            font=_font(16)
        ).pack(side="left", anchor="w")
        tk.Label(
            title_row,
            text=f"User: {self.session.get('username', 'unknown')}",
            bg=INPUT_BG,
            fg="#7a4f4f",
            font=_font(10, "normal")
        ).pack(side="right", anchor="e")

        # ------------------ Output area ------------------
        self.output_box = scrolledtext.ScrolledText(
            card,
            width=100,
            height=18,
            font=("Consolas", 11),
            bg="white",
            fg="#111827",
            relief="flat",
            padx=8,
            pady=8
        )
        self.output_box.pack(fill="both", expand=True, padx=8, pady=(4, 12))

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

        btn_frame = tk.Frame(card, bg=INPUT_BG)
        btn_frame.pack(fill="x", padx=6, pady=(0, 8))

        # helper to create styled action buttons with icons
        def make_btn(parent, text, icon, command, state=tk.NORMAL):
            btn = tk.Button(
                parent,
                text=f"{icon}  {text}",
                font=_font(12),
                bg=DARK_MAROON,
                fg=TEXT_LIGHT,
                activebackground=DARK_MAROON_HOVER,
                bd=0,
                padx=12,
                pady=8,
                cursor="hand2",
                state=state,
                command=command
            )
            btn.pack(side="left", padx=6, pady=4)
            btn.bind("<Enter>", lambda e: btn.configure(bg=DARK_MAROON_HOVER))
            btn.bind("<Leave>", lambda e: btn.configure(bg=DARK_MAROON))
            return btn

        # Ordered actions (icons chosen to be descriptive)
        actions = [
            ("Read File", "📂", self._action_read_file, "read_file"),
            ("Write File", "✏️", self._action_write_file, "write_file"),
            ("List Processes", "📋", self._action_list_processes, "list_processes"),
            ("Spawn Process", "▶️", self._action_spawn_process, "spawn_process"),
            ("Ping Host", "📶", self._action_ping_host, "ping_host"),
        ]

        for label, icon, callback, action_name in actions:
            state = tk.NORMAL if self._is_allowed(action_name) else tk.DISABLED
            make_btn(btn_frame, label, icon, callback, state=state)

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
        """Small popup dialog for user input (themed)."""
        win = tk.Toplevel(self.master)
        win.title("Input Required")
        win.configure(bg=INPUT_BG)
        win.geometry("420x160")
        win.resizable(False, False)
        win.grab_set()

        tk.Label(win, text=message, font=_font(11, "normal"), bg=INPUT_BG, fg=TEXT_DARK).pack(pady=(14, 6))

        entry_frame = tk.Frame(win, bg=INPUT_BG)
        entry_frame.pack(fill="x", padx=18)

        entry = ttk.Entry(entry_frame, width=48, font=_font(11))
        entry.pack(fill="x", pady=(6, 12))

        result = {"value": None}

        def submit():
            result["value"] = entry.get().strip()
            win.destroy()

        btn_frame = tk.Frame(win, bg=INPUT_BG)
        btn_frame.pack(fill="x", pady=(6, 12), padx=18)

        submit_btn = tk.Button(
            btn_frame,
            text="Submit",
            font=_font(11),
            bg=DARK_MAROON,
            fg=TEXT_LIGHT,
            activebackground=DARK_MAROON_HOVER,
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=submit
        )
        submit_btn.pack(side="right")

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            font=_font(11),
            bg="#bfa7a7",
            fg=TEXT_LIGHT,
            bd=0,
            padx=12,
            pady=8,
            cursor="hand2",
            command=win.destroy
        )
        cancel_btn.pack(side="right", padx=(0, 8))

        entry.focus_set()
        win.wait_window()
        return result["value"]
