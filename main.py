import tkinter as tk
from tkinter import messagebox
import openpyxl

# Colors and dimensions
COLORS = {
    "surface": "#F2E5BF",
    "surface_2": "#CB6040",
    "primary": "#257180"
}

WINDOW_DIMENSIONS = {
    "login": (600, 400),
    "home": (1000, 700),
    "create_book": (500, 500),
    "view_book": (500, 500),
    "issue_book": (400, 700)
}

# User credentials and login bypass
VALID_CREDENTIALS = {"admin": "123"}
BYPASS_LOGIN = True
DATABASE_PATH = "database.xlsx"

# Globals
main_frame = None
data = None
workbook = None
issue_window = None

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

def load_data():
    global data
    global workbook

    """Load data from the Excel file."""
    workbook = openpyxl.load_workbook(DATABASE_PATH)
    books_sheet = workbook['Books']
    customers_sheet = workbook["Customers"]

    books = []
    for row in books_sheet.iter_rows(min_row=2, values_only=True):
        books.append(row)
    
    customers = []
    for row in customers_sheet.iter_rows(min_row=2, values_only=True):
        customers.append(row)

    workbook.close()
    data = {
        'books': books,
        'customers': customers
    }


def save_data():
    workbook.save("database.xlsx")
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

    tk.Label(root, text="Library Management System", font=("Georgia", 24), 
             bg=COLORS["surface"], fg=COLORS["primary"]).pack(pady=20)

    for label_text, show_char in [("Username", None), ("Password", "*")]:
        tk.Label(root, text=label_text, font=("Georgia", 12), bg=COLORS["surface"]).pack(pady=10)
        entry = tk.Entry(root, show=show_char)
        entry.pack(pady=10)
        if label_text == "Username":
            username_entry = entry
        else:
            password_entry = entry

    tk.Button(root, text="Login", font=("Georgia", 12), bg=COLORS["primary"], 
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
        tk.Button(sidebar, text=text, font=("Georgia", 12), bg=COLORS["primary"], 
                  fg="white", command=command).pack(fill="x", pady=10)

    main_frame = PAGE_GENERATORS.get(page, generate_default_frame)(home)
    main_frame.pack(side="right", fill="both", expand=True)

def generate_default_frame(parent):
    """Generate the default frame content."""
    frame = tk.Frame(parent, bg=COLORS["surface"])
    tk.Label(frame, text="Library Management Software", font=("Georgia", 24), 
             fg=COLORS["primary"], bg=COLORS["surface"]).place(relx=0.5, rely=0.5, anchor="center")
    return frame

def issue_book(book_customer_frame):
    book, customer, frame = book_customer_frame

    # TODO Update customer sheet with the fact that a customer has borrowed a book
    for row in workbook['Books'].iter_rows(min_row=2, max_col=4):
        if row[1].value == book[1]:
            workbook['Books'].cell(row[3].row, column=4, value=customer[0])
            save_data()
            messagebox.showinfo(f"Issued '{book[1]}'", f"Successfully issued '{book[1]}' to {customer[0]}.")
            load_data()
            print(f"Finally: ", frame)
            frame.destroy()
            issue_window.destroy()

            break
    else:
        messagebox.showerror("Error", f"No row in Excel sheet found with index 1 equal to '{book[1]}'.")

def issue_search(entry, frame, book, window):
    customers = data['customers']

    for widget in frame.winfo_children():
        widget.destroy()

    found_customers = False
    for customer in customers:
        if customer[0].lower().startswith(entry.get().lower()):
            found_customers = True
            tk.Button(frame, text=customer[0], bg=COLORS["primary"], fg=COLORS['surface'], font=("Georgia", 12), command= lambda book_customer=(book, customer, window): issue_book(book_customer)).pack(padx=20, pady=20)

    if not found_customers:
        tk.Label(frame, text="No customers found with that name.", bg=COLORS["surface"], fg=COLORS['surface_2'], font=("Georgia", 12)).pack(padx=20, pady=20)

def open_issue_window(book, main_window):
    global issue_window
    window = tk.Toplevel()
    window.title(f"{book[1]} | Issue")
    window.configure(bg=COLORS["surface"])
    center_window(window, *WINDOW_DIMENSIONS["issue_book"])
    window.focus_force()

    issue_window = window

        
    tk.Label(window, text="Issue to a customer...", bg=COLORS["surface"], fg=COLORS['primary'], font=("Georgia", 24)).pack(padx=20, pady=20)

    search_bar = tk.Frame(window, bg=COLORS["surface"])
    search_bar.pack(fill="x", pady=5, padx=10)

    # Add the text entry box
    search_entry = tk.Entry(search_bar, font=("Georgia", 12))
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

    # Add the search button
    

    issue_book_search_list = data['customers']
    customer_frame = tk.Frame(window, bg=COLORS['surface'])
    customer_frame.pack(fill="both")

    search_button = tk.Button(search_bar, text="Search", font=("Georgia", 12), 
                               bg=COLORS["primary"], fg="white", command=lambda entry=search_entry: issue_search(entry, customer_frame, book, main_window))
    search_button.pack(side="right")

    for customer in data['customers']:
        tk.Button(customer_frame, text=customer[0], bg=COLORS["primary"], fg=COLORS['surface'], font=("Georgia", 12), command= lambda book_customer=(book, customer, main_window): issue_book(book_customer)).pack(padx=20, pady=20)

def open_book_page(book_isbn):
    book = None
    for row in data['books']:
        if row[0] == book_isbn:
            book = row
            break
    else:
        messagebox.showerror("Error", "Could not find book.")

    window = tk.Toplevel()
    window.title(f"{book[1]} | Details")
    window.configure(bg=COLORS["surface"])
    center_window(window, *WINDOW_DIMENSIONS["view_book"])
    window.focus_force()

    tk.Label(window, text=f"{book[1]}", font=("Georgia", 24), bg=COLORS["surface_2"], fg=COLORS["surface"]).pack(fill="x",)
    tk.Label(window, text=f"Book Details", font=("Georgia", 12), bg=COLORS["surface"], fg=COLORS["primary"]).pack(pady=30)
    
    tk.Label(window, text=f"ISBN: {book[0]}", font=("Georgia", 12), bg=COLORS["surface"], fg=COLORS["primary"]).pack(anchor="w", padx=10, pady=10)
    tk.Label(window, text=f"Title: {book[1]}", font=("Georgia", 12), bg=COLORS["surface"], fg=COLORS["primary"]).pack(anchor="w", padx=10, pady=10)
    tk.Label(window, text=f"Author: {book[2]}", font=("Georgia", 12), bg=COLORS["surface"], fg=COLORS["primary"]).pack(anchor="w", padx=10, pady=10)
    
    tk.Label(window, text=f"This book is currently {'available' if book[3] == 'NULL' else f'borrowed by {book[3]}'}.", font=("Georgia", 12), bg=COLORS["surface"], fg=COLORS["primary"]).pack(pady=30)
    tk.Button(window, text="Issue Book", bg=COLORS["primary"], fg=COLORS["surface"], font=("Georgia", 12), command=lambda book=book: open_issue_window(book, window)).pack()
def generate_list_books_frame(parent):
    """Generate the frame displaying a grid of books."""
    frame = tk.Frame(parent, bg=COLORS["surface"])
    
    search_bar = tk.Frame(frame, bg=COLORS["surface"])
    search_bar.pack(fill="x", pady=5, padx=10)

    # Add the text entry box
    search_entry = tk.Entry(search_bar, font=("Georgia", 12))
    search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

    # Add the search button
    search_button = tk.Button(search_bar, text="Search", font=("Georgia", 12), 
                               bg=COLORS["primary"], fg="white")
    search_button.pack(side="right")

    scrollable = VerticalScrolledFrame(frame)
    scrollable.pack(fill="both", expand=True)
    

    for i, book in enumerate(data["books"]):
        col = i % 3
        row = i // 3

        bg_color = COLORS["primary"] if i % 2 == 0 else COLORS["surface_2"]
        tk.Button(scrollable.interior, text=f"{book[1]}", 
                      font=("Georgia", 12), bg=bg_color, 
                      fg="white", width=25, command=lambda book=book: open_book_page(book[0]) ).grid(row=row, column=col, padx=5, pady=5)
    

    return frame

def generate_list_customers_frame(parent):
    """Generate a placeholder frame for customer management."""
    frame = tk.Frame(parent, bg=COLORS["surface"])
    tk.Label(frame, text="Customer Management Coming Soon", font=("Georgia", 24), 
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
        tk.Label(window, text=label_text, font=("Georgia", 12), bg=COLORS["surface"]).pack(pady=10)
        entry = tk.Entry(window, font=("Georgia", 12))
        entry.pack(pady=10)
        entries[label_text.lower()] = entry

    def create_book():
        if all(entry.get().strip() for entry in entries.values()):
            messagebox.showinfo("Success", "Book created successfully!")
            workbook['Books'].append((entries['isbn'].get(), entries['title'].get(), entries['author'].get(), 'NULL'))
            save_data()

        else:
            messagebox.showerror("Error", "All fields must be filled.")

    tk.Button(window, text="Create Book", font=("Georgia", 12), 
              bg=COLORS["primary"], fg="white", command=create_book).pack(pady=20)

    
PAGE_GENERATORS = {
    "default": generate_default_frame,
    "books": generate_list_books_frame,
    "customers": generate_list_customers_frame
}

def run_app():
    """Run the application."""
    load_data()

    if not BYPASS_LOGIN:
        root = create_root()
        display_login(root)
        root.mainloop()
    else:
        open_home_page()

if __name__ == "__main__":
    run_app()
