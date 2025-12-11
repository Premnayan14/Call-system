# main.py

import tkinter as tk
from ui.login_page import LoginPage
from core.security import SecurityController
from core.logger import AuditLogger
from core.policy import PolicyManager
from ui.theme import apply_dark_theme

def main():
    root = tk.Tk()
    apply_dark_theme(root) 
    root.title("Secure System Call Interface")
    root.geometry("480x360")
    
    # Instantiate core controllers
    policy_manager = PolicyManager("data/policy.json")
    security_controller = SecurityController("data/users.json", policy_manager)
    audit_logger = AuditLogger("logs/actions.db")

    # Launch login interface
    LoginPage(root, security_controller, audit_logger)
    root.mainloop()


if __name__ == "__main__":
    main()
