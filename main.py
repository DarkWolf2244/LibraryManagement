from tkinter import *
from tkinter import messagebox

SURFACE_COLOR = "#F2E5BF" # Neutral background color
SURFACE_2_COLOR = "#CB6040" # Color of the sidebar on the home screen and anywhere else we need another surface
PRIMARY_COLOR = "#257180" # Buttons and cool stuff like that

LOGIN_WINDOW_WIDTH = 600
LOGIN_WINDOW_HEIGHT = 400

HOME_WINDOW_WIDTH = 1000
HOME_WINDOW_HEIGHT = 700

VALID_USERNAMES = ['admin']
VALID_PASSWORDS = ['123']

BYPASS_LOGIN = True # Set to True if you want any username/password (even empty) to work

main_frame = None

# Copy-pasted from StackOverflow with my own monkeypatches my sanity is rended from my soul
class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = canvas = Canvas(self, bd=0, highlightthickness=0,
                           yscrollcommand=vscrollbar.set, bg=SURFACE_COLOR)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = Frame(canvas, bg=SURFACE_COLOR, padx=25, pady=25)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def create_root() -> Tk:
    """
    Create the main window of the application and set its title, size, and position.
    
    Returns:
        window (Tk): The main window of the application.
    """
    root = Tk()
    root.focus_force()
    root.title("Login | Library Management System")
    root.config(bg=SURFACE_COLOR, padx=10, pady=10)

    screen_width: int = root.winfo_screenwidth()
    screen_height: int = root.winfo_screenheight()

    x: int = int((screen_width / 2) - (LOGIN_WINDOW_WIDTH / 2))
    y: int = int((screen_height / 2) - (LOGIN_WINDOW_HEIGHT / 2))

    root.geometry(f"{LOGIN_WINDOW_WIDTH}x{LOGIN_WINDOW_HEIGHT}+{x}+{y}")

    return root

def display_login(root: Tk):
    """
    Display the login page.

    Args:
        root (Tk): The main window of the application.
    """
    heading_label = Label(root, text="Library Management System", font=("Helvetica", 24), bg=SURFACE_COLOR, fg=PRIMARY_COLOR)

    username_label = Label(root, text="Username", font=("Helvetica", 12), bg=SURFACE_COLOR)
    username_entry = Entry(root)

    password_label = Label(root, text="Password", font=("Helvetica", 12), bg=SURFACE_COLOR)
    password_entry = Entry(root, show="*")

    login_button = Button(root, text="Login", relief=GROOVE,command=lambda: login(root, username_entry, password_entry), bg=PRIMARY_COLOR, fg="white", font=("Helvetica", 12))

    heading_label.pack(pady=20)
    username_label.pack(pady=20)
    username_entry.pack(pady=10)
    password_label.pack(pady=20)
    password_entry.pack(pady=10)
    login_button.pack(pady=20)

def login(root: Tk, username_entry: Entry, password_entry: Entry):
    if BYPASS_LOGIN:
        root.destroy()
        open_home_page()
    else:
        username = username_entry.get()
        password = password_entry.get()

        if username in VALID_USERNAMES and password in VALID_PASSWORDS:
            root.destroy()
            open_home_page()
        else:
            messagebox.showerror("Invalid Credentials", "Invalid username or password.")

def logout(tk: Tk):
    tk.destroy()

def generate_books_frame(home_page):
    main_frame = Frame(home_page, bg=SURFACE_COLOR, width=HOME_WINDOW_WIDTH//10, height=HOME_WINDOW_HEIGHT)
    main_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    

    search_frame = Frame(main_frame, bg=SURFACE_COLOR)
    search_frame.pack(side=TOP, fill=X)

    search_label = Label(search_frame, text="Search", font=("Helvetica", 12), bg=SURFACE_COLOR)
    search_label.pack(side=LEFT, padx=10, pady=10)

    search_entry = Entry(search_frame, font=("Helvetica", 12))
    search_entry.pack(side=LEFT, fill=X, expand=True)

    search_btn = Button(search_frame, text="Search", font=("Helvetica", 12), bg=PRIMARY_COLOR, fg="white", command=lambda: search_books(search_entry, main_frame))
    search_btn.pack(side=RIGHT, padx=10, pady=10)

    scroll_frame = VerticalScrolledFrame(main_frame, bg=SURFACE_COLOR, width=HOME_WINDOW_WIDTH//10, height=HOME_WINDOW_HEIGHT)
    scroll_frame.pack(side=TOP, fill=BOTH, expand=True)

    for x in range(20):
        for y in range(8):
            book_btn = Button(scroll_frame.interior, borderwidth=2, relief=RIDGE, text=f"Book {y + 8*x}", font=("Helvetica", 12), bg=PRIMARY_COLOR, fg="white", width=7, height=3)
            book_btn.grid(row=x, column=y, padx=5, pady=5)

    return main_frame

def generate_customers_frame(home_page):
    main_frame = Frame(home_page, bg=SURFACE_COLOR, width=HOME_WINDOW_WIDTH//10, height=HOME_WINDOW_HEIGHT)
    main_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    label = Label(main_frame, text="Not yet implemented.", font=("Helvetica", 24), fg=PRIMARY_COLOR, bg=SURFACE_COLOR)
    label.place(relx=0.5, rely=0.5, anchor=CENTER)

    return main_frame

def generate_default_frame(home_page):
    main_frame = Frame(home_page, bg=SURFACE_COLOR, width=HOME_WINDOW_WIDTH//10, height=HOME_WINDOW_HEIGHT)
    main_frame.pack(side=RIGHT, fill=BOTH, expand=True)

    label = Label(main_frame, text="Library Management Software", font=("Helvetica", 24), fg=PRIMARY_COLOR, bg=SURFACE_COLOR)
    label.place(relx=0.5, rely=0.5, anchor=CENTER)
    return main_frame

def switch_home_page(home_page: Tk, page):
    global main_frame
    main_frame.destroy()
    if page == 'list_books':
        main_frame = generate_books_frame(home_page)
    elif page == 'list_customers':
        main_frame = generate_customers_frame(home_page)
    elif page == 'default':
        main_frame = generate_default_frame(home_page)

def display_home_page(home_page: Tk, page):
    global main_frame
    sidebar = Frame(home_page, bg=SURFACE_2_COLOR, width=2*HOME_WINDOW_WIDTH//10, height=HOME_WINDOW_HEIGHT, pady=50, padx=5)

    list_books_btn = Button(sidebar, borderwidth=2, relief=RIDGE, text="List Books", font=("Helvetica", 12), bg=PRIMARY_COLOR, fg="white", height=2, command= lambda: switch_home_page(home_page, 'list_books'))
    create_book_btn = Button(sidebar, borderwidth=2, relief=RIDGE, text="Create Book", font=("Helvetica", 12), bg=PRIMARY_COLOR, fg="white", height=2)
    list_customers_btn = Button(sidebar, borderwidth=2, relief=RIDGE, text="List Customers", font=("Helvetica", 12), bg=PRIMARY_COLOR, fg="white", height=2, command=lambda: switch_home_page(home_page, 'list_customers'))
    create_customer_btn = Button(sidebar, borderwidth=2, relief=RIDGE, text="Create Customer", font=("Helvetica", 12), bg=PRIMARY_COLOR, fg="white", height=2)
    logout_btn = Button(sidebar, borderwidth=2, relief=RIDGE, text="Logout", font=("Helvetica", 12), bg=PRIMARY_COLOR, fg="white", height=2, command=lambda: logout(home_page))
    sidebar.pack(side=LEFT, fill=Y)

    list_books_btn.pack(fill=X)
    create_book_btn.pack(fill=X, pady=20)
    list_customers_btn.pack(fill=X)
    create_customer_btn.pack(fill=X, pady=20)
    logout_btn.pack(fill=X)

    if page == 'list_books':
        main_frame = generate_books_frame(home_page)
    elif page == 'list_customers':
        main_frame = generate_customers_frame(home_page)
    elif page == 'default':
        main_frame = generate_default_frame(home_page)
        
    main_frame.pack(side=RIGHT, fill=BOTH, expand=True)

def search_books(search_entry: Entry, main_frame: Frame):
    pass
def open_home_page():
    home = Tk()
    home.focus_force()
    home.title("Home | Library Management System")
    home.config(bg=SURFACE_COLOR)
    screen_width: int = home.winfo_screenwidth()
    screen_height: int = home.winfo_screenheight()

    x: int = int((screen_width / 2) - (HOME_WINDOW_WIDTH / 2))
    y: int = int((screen_height / 2) - (HOME_WINDOW_HEIGHT / 2))

    home.geometry(f"{HOME_WINDOW_WIDTH}x{HOME_WINDOW_HEIGHT}+{x}+{y}")

    display_home_page(home, 'default')
    home.mainloop()

    run_app()
def run_app():
    """
    Initialize and run the application.
    """
    root = create_root()
    display_login(root)

    root.mainloop()

if __name__ == "__main__":
    run_app()