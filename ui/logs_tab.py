# ui/logs_tab.py

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import Optional
from core.logger import AuditLogger


class LogsTab:
    def __init__(self, master, audit_logger: AuditLogger):
        self.master = master
        self.audit_logger = audit_logger
        self._build_interface()
        self._load_logs()

    def _build_interface(self):
        frame = tk.Frame(self.master)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Filter row
        filter_frame = tk.Frame(frame)
        filter_frame.pack(fill="x", pady=(0, 8))

        tk.Label(filter_frame, text="User:").pack(side="left")
        self.entry_user = tk.Entry(filter_frame, width=12)
        self.entry_user.pack(side="left", padx=(4, 12))

        tk.Label(filter_frame, text="Action:").pack(side="left")
        self.entry_action = tk.Entry(filter_frame, width=16)
        self.entry_action.pack(side="left", padx=(4, 12))

        tk.Label(filter_frame, text="Status:").pack(side="left")
        self.entry_status = tk.Entry(filter_frame, width=10)
        self.entry_status.pack(side="left", padx=(4, 12))

        tk.Button(filter_frame, text="Refresh", command=self._load_logs).pack(side="left", padx=6)
        tk.Button(filter_frame, text="Export CSV", command=self._export_csv).pack(side="left", padx=6)

        # Treeview
        columns = ("username", "action", "status", "timestamp")

        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        for col in columns:
            self.tree.heading(col, text=col.title())
            # sensible column widths
            if col == "timestamp":
                self.tree.column(col, width=160)
            else:
                self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def _load_logs(self):
        # clear
        for row in self.tree.get_children():
            self.tree.delete(row)

        filters = {
            "username": self.entry_user.get().strip() or None,
            "action": self.entry_action.get().strip() or None,
            "status": self.entry_status.get().strip() or None,
        }
        # remove none entries
        filters = {k: v for k, v in filters.items() if v is not None}

        rows = self.audit_logger.fetch_logs(limit=2000, filters=filters)
        for row in rows:
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
