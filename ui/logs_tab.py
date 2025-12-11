# ui/logs_tab.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional
from core.logger import AuditLogger
import platform

# Theme/font helpers (consistent with other UI files)
def _font(size=12, weight="bold"):
    if platform.system() == "Windows":
        base = "Segoe UI"
    else:
        base = "Arial"
    return (base, size, weight)

# Colors
LIGHT_MAROON_BG = "#f3e4e4"
CARD_BG = "#2e0f0f"
INPUT_BG = "#fff6f6"
DARK_MAROON = "#5a1a1a"
DARK_MAROON_HOVER = "#3d1111"
TEXT_LIGHT = "#f8eaea"
TEXT_DARK = "#2a0c0c"


class LogsTab:
    def __init__(self, master, audit_logger: AuditLogger):
        self.master = master
        self.audit_logger = audit_logger
        self._build_interface()
        self._load_logs()

    def _build_interface(self):
        frame = tk.Frame(self.master, bg=LIGHT_MAROON_BG)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Card area to match other screens
        card = tk.Frame(frame, bg=INPUT_BG, bd=0, padx=12, pady=12)
        card.pack(fill="both", expand=True)

        # Header row
        header = tk.Frame(card, bg=INPUT_BG)
        header.pack(fill="x", pady=(0, 8))
        tk.Label(header, text="Audit Logs", bg=INPUT_BG, fg=TEXT_DARK, font=_font(16)).pack(side="left", anchor="w")
        tk.Label(header, text="View and export audit trails", bg=INPUT_BG, fg="#7a4f4f", font=_font(10, "normal")).pack(side="left", padx=(12,0))

        # ---------------- Filter Row ----------------
        filter_frame = tk.Frame(card, bg=INPUT_BG)
        filter_frame.pack(fill="x", pady=(6, 10))

        tk.Label(filter_frame, text="User:", bg=INPUT_BG, fg=TEXT_DARK, font=_font(11)).pack(side="left")
        self.entry_user = ttk.Entry(filter_frame, width=12, font=_font(11))
        self.entry_user.pack(side="left", padx=(4, 12))

        tk.Label(filter_frame, text="Action:", bg=INPUT_BG, fg=TEXT_DARK, font=_font(11)).pack(side="left")
        self.entry_action = ttk.Entry(filter_frame, width=16, font=_font(11))
        self.entry_action.pack(side="left", padx=(4, 12))

        tk.Label(filter_frame, text="Status:", bg=INPUT_BG, fg=TEXT_DARK, font=_font(11)).pack(side="left")
        self.entry_status = ttk.Entry(filter_frame, width=10, font=_font(11))
        self.entry_status.pack(side="left", padx=(4, 12))

        # Styled buttons
        def styled_btn(parent, text, command):
            b = tk.Button(parent, text=text, font=_font(11), bg=DARK_MAROON, fg=TEXT_LIGHT,
                          activebackground=DARK_MAROON_HOVER, bd=0, padx=10, pady=6, cursor="hand2",
                          command=command)
            b.pack(side="left", padx=6)
            b.bind("<Enter>", lambda e: b.configure(bg=DARK_MAROON_HOVER))
            b.bind("<Leave>", lambda e: b.configure(bg=DARK_MAROON))
            return b

        styled_btn(filter_frame, "Refresh", self._load_logs)
        styled_btn(filter_frame, "Export CSV", self._export_csv)

        # ---------------- Treeview ----------------
        columns = ("username", "action", "status", "timestamp")
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        # Treeview styling
        style.configure("Logs.Treeview", font=_font(11), rowheight=26)
        style.configure("Logs.Treeview.Heading", font=_font(12, "bold"))
        style.map("Logs.Treeview", background=[("selected", "#e6bcbc")], foreground=[("selected", "#2a0c0c")])

        self.tree = ttk.Treeview(card, columns=columns, show="headings", height=16, style="Logs.Treeview")
        for col in columns:
            self.tree.heading(col, text=col.title())
            if col == "timestamp":
                self.tree.column(col, width=180, anchor="center")
            else:
                self.tree.column(col, width=140, anchor="w")

        # Scrollbar
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Place tree and scrollbar
        tree_frame = tk.Frame(card, bg=INPUT_BG)
        tree_frame.pack(fill="both", expand=True, pady=(6, 0))
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _load_logs(self):
        # clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        filters = {
            "username": self.entry_user.get().strip() or None,
            "action": self.entry_action.get().strip() or None,
            "status": self.entry_status.get().strip() or None,
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        rows = self.audit_logger.fetch_logs(limit=2000, filters=filters)
        for row in rows:
            # Expecting row to match (username, action, status, timestamp)
            self.tree.insert("", tk.END, values=row)

    def _export_csv(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv")],
            title="Export logs to CSV"
        )
        if not path:
            return

        filters = {
            "username": self.entry_user.get().strip() or None,
            "action": self.entry_action.get().strip() or None,
            "status": self.entry_status.get().strip() or None,
        }
        filters = {k: v for k, v in filters.items() if v is not None}

        try:
            self.audit_logger.export_csv(path, limit=5000, filters=filters)
            messagebox.showinfo("Export Complete", f"Logs exported to:\n{path}")
        except Exception as exc:
            messagebox.showerror("Export Failed", str(exc))
