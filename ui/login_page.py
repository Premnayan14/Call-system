# ui/login_page.py

import tkinter as tk
from tkinter import ttk, messagebox
from ui.dashboard import Dashboard
import platform

def _font(size=12, weight="bold"):
    if platform.system() == "Windows":
        base = "Segoe UI"
    elif platform.system() == "Darwin":
        base = "Helvetica Neue"
    else:
        base = "Arial"
    return (base, size, weight)


# ---------- COLOR THEME (DARK MAROON VARIANT) ----------
LIGHT_MAROON_BG = "#f3e4e4"     # page background (light maroon)
CARD_BG = "#2e0f0f"             # card dark maroon
INPUT_BG = "#fff6f6"            # input pale background
DARK_MAROON = "#5a1a1a"         # button / accent maroon
DARK_MAROON_HOVER = "#3d1111"   # hover shade
TEXT_LIGHT = "#f8eef0"          # light text for dark card
TEXT_DARK = "#2a0c0c"           # dark text for light areas
ICON_BG = "#4b1313"             # small icon circle bg


class LoginPage:
    def __init__(self, master, security_controller, audit_logger):
        self.master = master
        self.security_controller = security_controller
        self.audit_logger = audit_logger

        # Page background (light maroon)
        self.master.configure(bg=LIGHT_MAROON_BG)
        self.container = tk.Frame(self.master, bg=LIGHT_MAROON_BG)
        self.container.pack(expand=True, fill="both")

        self._build_card()
        self._build_interface()

    def _build_card(self):
        # soft shadow under the card
        shadow = tk.Frame(self.container, bg="#ddbcbc")
        shadow.place(relx=0.5, rely=0.5, anchor="center", width=620, height=480, x=10, y=10)

        # main card - dark maroon
        self.card = tk.Frame(self.container, bg=CARD_BG, bd=0)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=620, height=480)

        # top accent bar (very dark)
        tk.Frame(self.card, bg=DARK_MAROON, height=8).pack(fill="x", side="top")

        # header area (logo + title)
        header = tk.Frame(self.card, bg=CARD_BG, padx=28, pady=20)
        header.pack(fill="x")

        # Logo: circle with "OS" instead of "VS"
        logo_canvas = tk.Canvas(header, width=72, height=72, bg=CARD_BG, highlightthickness=0)
        logo_canvas.create_oval(6, 6, 66, 66, fill=DARK_MAROON, outline="")
        logo_canvas.create_text(36, 38, text="OS", fill=TEXT_LIGHT, font=_font(18))
        logo_canvas.pack(side="left")

        title_box = tk.Frame(header, bg=CARD_BG)
        title_box.pack(side="left", padx=14)

        tk.Label(title_box, text="Welcome Back", bg=CARD_BG,
                 fg=TEXT_LIGHT, font=_font(22)).pack(anchor="w")
        tk.Label(title_box, text="Secure sign-in to your workspace", bg=CARD_BG,
                 fg="#f0dede", font=_font(11, "normal")).pack(anchor="w", pady=(6, 0))

        # decorative icons on the right of header (small)
        decor = tk.Frame(header, bg=CARD_BG)
        decor.pack(side="right", padx=12)
        # small circular icons (using emoji as placeholders)
        for em in ("⚙️", "🔒", "📊"):
            ic = tk.Label(decor, text=em, bg=CARD_BG, fg=TEXT_LIGHT, font=_font(12))
            ic.pack(side="left", padx=6)

        # separator
        tk.Frame(self.card, bg="#3b1616", height=1).pack(fill="x", padx=20, pady=(6, 0))

        # form area (light inputs on dark card)
        self.form = tk.Frame(self.card, bg=CARD_BG, padx=36, pady=18)
        self.form.pack(fill="both", expand=True)

    def _build_interface(self):
        # style for ttk entries
        style = ttk.Style(self.master)
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure('TEntry', padding=8, relief='flat', font=_font(12))

        # Username label (light text)
        tk.Label(self.form, text="Username", bg=CARD_BG, fg=TEXT_LIGHT,
                 font=_font(13)).pack(fill="x", pady=(6, 6))

        usr_frame = tk.Frame(self.form, bg=INPUT_BG, highlightthickness=0)
        usr_frame.pack(fill="x", pady=(0, 12))
        usr_frame.configure(highlightthickness=1, highlightbackground="#e5bdbd")

        # user icon inside a small maroon badge
        icon_badge = tk.Canvas(usr_frame, width=36, height=36, bg=INPUT_BG, highlightthickness=0)
        icon_badge.create_oval(4, 4, 32, 32, fill=ICON_BG, outline="")
        icon_badge.create_text(18, 19, text="👤", fill=TEXT_LIGHT, font=_font(11))
        icon_badge.pack(side="left", padx=8, pady=8)

        self.entry_username = ttk.Entry(usr_frame, font=_font(13))
        self.entry_username.pack(side="left", fill="x", expand=True, padx=(8, 12), pady=8)

        # Password label
        tk.Label(self.form, text="Password", bg=CARD_BG, fg=TEXT_LIGHT,
                 font=_font(13)).pack(fill="x", pady=(2, 6))

        pass_frame = tk.Frame(self.form, bg=INPUT_BG, highlightthickness=0)
        pass_frame.pack(fill="x", pady=(0, 12))
        pass_frame.configure(highlightthickness=1, highlightbackground="#e5bdbd")

        # lock icon badge
        lock_badge = tk.Canvas(pass_frame, width=36, height=36, bg=INPUT_BG, highlightthickness=0)
        lock_badge.create_oval(4, 4, 32, 32, fill=ICON_BG, outline="")
        lock_badge.create_text(18, 19, text="🔒", fill=TEXT_LIGHT, font=_font(11))
        lock_badge.pack(side="left", padx=8, pady=8)

        self.entry_password = ttk.Entry(pass_frame, show="*", font=_font(13))
        self.entry_password.pack(side="left", fill="x", expand=True, padx=(8, 6), pady=8)

        # dark eye button (rounded look via padding)
        self._show_pass = False
        eye_btn = tk.Button(pass_frame, text="👁️", fg=TEXT_LIGHT, bg=DARK_MAROON,
                            activebackground=DARK_MAROON_HOVER, bd=0,
                            font=_font(11), cursor="hand2", command=self._toggle_password)
        eye_btn.pack(side="right", padx=8, pady=8)

        # small helper text above the button (optional, subtle)
        tk.Label(self.form, text="Use your OS credentials to login", bg=CARD_BG,
                 fg="#f3d6d6", font=_font(9, "normal")).pack(anchor="w", pady=(2, 6))

        # ------------------------------
        # LOGIN BUTTON (below form)
        # ------------------------------
        btn_outer = tk.Frame(self.card, bg=CARD_BG, pady=8, padx=36)
        btn_outer.pack(fill="x", pady=(6, 4))

        self.btn_login = tk.Button(
            btn_outer,
            text="   🔐   LOGIN   ",
            font=_font(15),
            bg=DARK_MAROON,
            fg=TEXT_LIGHT,
            activebackground=DARK_MAROON_HOVER,
            bd=0,
            relief="flat",
            cursor="hand2",
            command=self._attempt_login
        )
        self.btn_login.pack(fill="x", ipadx=6, ipady=14)

        # hover styling for button
        self.btn_login.bind("<Enter>", lambda e: self.btn_login.configure(bg=DARK_MAROON_HOVER))
        self.btn_login.bind("<Leave>", lambda e: self.btn_login.configure(bg=DARK_MAROON))

        # ------------------------------
        # FORGOT PASSWORD - placed BELOW button (centered)
        # ------------------------------
        forgot_frame = tk.Frame(self.card, bg=CARD_BG, pady=8)
        forgot_frame.pack(fill="x", padx=36)
        forgot = tk.Label(forgot_frame, text="Forgot password?", bg=CARD_BG,
                          fg="#f0cfcf", cursor="hand2", font=_font(11, "normal"))
        forgot.pack(anchor="center")
        forgot.bind("<Button-1>", lambda e: messagebox.showinfo("Forgot Password",
                                                                 "Please contact your administrator to reset your password."))

        # footer with small icons and version
        footer = tk.Frame(self.card, bg="#231010", pady=12)
        footer.pack(fill="x", side="bottom")
        # left cluster: small info icon + text
        left = tk.Frame(footer, bg="#231010")
        left.pack(side="left", padx=18)
        tk.Label(left, text="ℹ️", bg="#231010", fg=TEXT_LIGHT, font=_font(11)).pack(side="left", padx=(0,6))
        tk.Label(left, text="Need help? Contact IT", bg="#231010", fg="#d9bcbc", font=_font(10, "normal")).pack(side="left")

        # right cluster: version and status icon
        right = tk.Frame(footer, bg="#231010")
        right.pack(side="right", padx=18)
        tk.Label(right, text="v1.0", bg="#231010", fg="#bfa7a7", font=_font(10, "normal")).pack(side="right", padx=(8,0))
        tk.Label(right, text="✅", bg="#231010", fg=TEXT_LIGHT, font=_font(11)).pack(side="right")

        # Keyboard bindings and focus
        self.entry_username.focus_set()
        self.entry_username.bind("<Return>", lambda e: self._attempt_login())
        self.entry_password.bind("<Return>", lambda e: self._attempt_login())

    def _toggle_password(self):
        # preserve previous behavior (show/hide)
        if self.entry_password.cget("show") == "*":
            self.entry_password.configure(show="")
        else:
            self.entry_password.configure(show="*")

    def _attempt_login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        # functionality unchanged
        session = self.security_controller.authenticate(username, password)

        if session:
            self.audit_logger.record(username, "login", "success")
            # remove UI and proceed to Dashboard (unchanged)
            self.card.destroy()
            self.container.destroy()
            Dashboard(self.master, session, self.audit_logger)
        else:
            self.audit_logger.record(username, "login", "failed")
            messagebox.showerror("Authentication Failed", "Invalid username or password.")
