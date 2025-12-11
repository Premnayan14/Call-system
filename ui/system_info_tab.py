# ui/system_info_tab.py

import tkinter as tk
from tkinter import scrolledtext, ttk
from core.syscalls import SyscallEngine


class SystemInfoTab:
    def __init__(self, master):
        self.master = master
        self._build_interface()
        self._refresh_info()

    def _build_interface(self):
        frame = tk.Frame(self.master)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        top_frame = tk.Frame(frame)
        top_frame.pack(fill="x", pady=(0, 8))

        ttk.Button(top_frame, text="Refresh", command=self._refresh_info).pack(side="left")

        self.text_box = scrolledtext.ScrolledText(frame, width=80, height=20, font=("Consolas", 11))
        self.text_box.pack(fill="both", expand=True)

        self.text_box.configure(state="disabled")

    def _refresh_info(self):
        success, info = SyscallEngine.system_info()
        self.text_box.configure(state="normal")
        self.text_box.delete("1.0", tk.END)
        if success:
            # pretty print multi-line info
            self.text_box.insert("1.0", info)
        else:
            self.text_box.insert("1.0", f"Failed to obtain system information:\n{info}")
        self.text_box.configure(state="disabled")
