import tkinter as tk
from tkinter import messagebox

# Colors and dimensions
COLORS = {
    "surface": "#F2E5BF",
    "surface_2": "#CB6040",
    "primary": "#257180"
}

WINDOW_DIMENSIONS = {
    "login": (600, 400),
    "home": (1000, 700),
    "create_book": (500, 500)
}

# User credentials and login bypass
VALID_CREDENTIALS = {"admin": "123"}
BYPASS_LOGIN = True

# Globals
main_frame = None

class VerticalScrolledFrame(tk.Frame):
    """Scrollable frame with vertical scrolling."""
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas = tk.Canvas(self, bg=COLORS["surface"], bd=0, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.interior = tk.Frame(self.canvas, bg=COLORS["surface"], padx=25, pady=25)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.interior.bind("<Configure>", self._update_scroll_region)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)

    def _update_scroll_region(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(-int(event.delta / 120), "units")

def center_window(window, width, height):
    """Center a window on the screen."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def create_root():
    """Create and configure the main application window."""
    root = tk.Tk()
    root.title("Login | Library Management System")
    root.configure(bg=COLORS["surface"], padx=10, pady=10)
    center_window(root, *WINDOW_DIMENSIONS["login"])
    return root

def display_login(root):
    """Display the login page."""
    def handle_login():
        username, password = username_entry.get(), password_entry.get()
        if BYPASS_LOGIN or VALID_CREDENTIALS.get(username) == password:
            root.destroy()
            open_home_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    tk.Label(root, text="Library Management System", font=("Helvetica", 24), 
             bg=COLORS["surface"], fg=COLORS["primary"]).pack(pady=20)

    for label_text, show_char in [("Username", None), ("Password", "*")]:
        tk.Label(root, text=label_text, font=("Helvetica", 12), bg=COLORS["surface"]).pack(pady=10)
        entry = tk.Entry(root, show=show_char)
        entry.pack(pady=10)
        if label_text == "Username":
            username_entry = entry
        else:
            password_entry = entry

    tk.Button(root, text="Login", font=("Helvetica", 12), bg=COLORS["primary"], 
              fg="white", command=handle_login).pack(pady=20)

def open_home_page():
    """Open the home page."""
    home = tk.Tk()
    home.title("Home | Library Management System")
    home.configure(bg=COLORS["surface"])
    center_window(home, *WINDOW_DIMENSIONS["home"])
    display_home_page(home, "default")
    home.mainloop()

def display_home_page(home, page):
    """Display the home page with a sidebar and dynamic content."""
    global main_frame

    def switch_page(new_page):
        global main_frame
        main_frame.destroy()
        main_frame = PAGE_GENERATORS.get(new_page, generate_default_frame)(home)
        main_frame.pack(side="right", fill="both", expand=True)

    sidebar = tk.Frame(home, bg=COLORS["surface_2"], width=200, pady=50, padx=5)
    sidebar.pack(side="left", fill="y")

    buttons = [
        ("List Books", lambda: switch_page("books")),
        ("Create Book", open_create_book_page),
        ("List Customers", lambda: switch_page("customers")),
        ("Logout", home.destroy)
    ]

    for text, command in buttons:
        tk.Button(sidebar, text=text, font=("Helvetica", 12), bg=COLORS["primary"], 
                  fg="white", command=command).pack(fill="x", pady=10)

    main_frame = PAGE_GENERATORS.get(page, generate_default_frame)(home)
    main_frame.pack(side="right", fill="both", expand=True)

def generate_default_frame(parent):
    """Generate the default frame content."""
    frame = tk.Frame(parent, bg=COLORS["surface"])
    tk.Label(frame, text="Library Management Software", font=("Helvetica", 24), 
             fg=COLORS["primary"], bg=COLORS["surface"]).place(relx=0.5, rely=0.5, anchor="center")
    return frame

def generate_books_frame(parent):
    """Generate the frame displaying a grid of books."""
    frame = tk.Frame(parent, bg=COLORS["surface"])
    scrollable = VerticalScrolledFrame(frame)
    scrollable.pack(fill="both", expand=True)

    for col in range(100):
        for row in range(5):
            tk.Button(scrollable.interior, text=f"Book {col * 4 + row + 1}", 
                      font=("Helvetica", 12), bg=COLORS["primary"], 
                      fg="white", width=10).grid(row=col, column=row, padx=5, pady=5)
    return frame

def generate_customers_frame(parent):
    """Generate a placeholder frame for customer management."""
    frame = tk.Frame(parent, bg=COLORS["surface"])
    tk.Label(frame, text="Customer Management Coming Soon", font=("Helvetica", 24), 
             fg=COLORS["primary"], bg=COLORS["surface"]).place(relx=0.5, rely=0.5, anchor="center")
    return frame

def open_create_book_page():
    """Open the 'Create Book' window."""
    window = tk.Toplevel()
    window.title("Create Book")
    window.configure(bg=COLORS["surface"])
    center_window(window, *WINDOW_DIMENSIONS["create_book"])

    entries = {}
    for label_text in ["Title", "Author", "ISBN"]:
        tk.Label(window, text=label_text, font=("Helvetica", 12), bg=COLORS["surface"]).pack(pady=10)
        entry = tk.Entry(window, font=("Helvetica", 12))
        entry.pack(pady=10)
        entries[label_text.lower()] = entry

    def create_book():
        if all(entry.get().strip() for entry in entries.values()):
            messagebox.showinfo("Success", "Book created successfully!")
        else:
            messagebox.showerror("Error", "All fields must be filled.")

    tk.Button(window, text="Create Book", font=("Helvetica", 12), 
              bg=COLORS["primary"], fg="white", command=create_book).pack(pady=20)

PAGE_GENERATORS = {
    "default": generate_default_frame,
    "books": generate_books_frame,
    "customers": generate_customers_frame
}

def run_app():
    """Run the application."""
    root = create_root()
    display_login(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()
