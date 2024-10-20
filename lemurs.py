import tkinter as tk
from tkinter import messagebox

# Function to open the home page after successful login
def open_home_page():
    # Create the home window
    home_window = tk.Tk()
    home_window.title("Library Management System - Home")
    home_window.geometry("1280x720")

    # Colors
    bg_color = "#F4ECE1"  
    left_frame_color = "#D4A373"  
    right_frame_color = "#D4A373"  
    button_color = "#A67B5B"  
    text_color = "#5B4636"  

    home_window.config(bg=bg_color)

    left_frame = tk.Frame(home_window, bg=left_frame_color, width=320)  
    left_frame.pack(side="left", fill="y")  

    # Heading for left frame
    label_books = tk.Label(left_frame, text="Books", font=("Helvetica", 16, "bold"), bg=left_frame_color, fg=text_color)
    label_books.pack(pady=20)

    # Buttons for left frame
    button_add_book = tk.Button(left_frame, text="Add Book", font=("Helvetica", 12), bg=button_color, fg="white", borderwidth=2, relief="flat", padx=10, pady=5)
    button_add_book.pack(pady=10, padx=10, fill="x")

    button_search_book = tk.Button(left_frame, text="Search Book", font=("Helvetica", 12), bg=button_color, fg="white", borderwidth=2, relief="flat", padx=10, pady=5)
    button_search_book.pack(pady=10, padx=10, fill="x")

    button_assign_book = tk.Button(left_frame, text="Assign Book", font=("Helvetica", 12), bg=button_color, fg="white", borderwidth=2, relief="flat", padx=10, pady=5)
    button_assign_book.pack(pady=10, padx=10, fill="x")

    button_remove_book = tk.Button(left_frame, text="Remove Book", font=("Helvetica", 12), bg=button_color, fg="white", borderwidth=2, relief="flat", padx=10, pady=5)
    button_remove_book.pack(pady=10, padx=10, fill="x")

    # Right Frame (Admin) - fixed width
    right_frame = tk.Frame(home_window, bg=right_frame_color, width=320)  
    right_frame.pack(side="right", fill="y")  

    # Heading for right frame
    label_admin = tk.Label(right_frame, text="Admin", font=("Helvetica", 16, "bold"), bg=right_frame_color, fg=text_color)
    label_admin.pack(pady=20)

    # Buttons for right frame
    button_add_customer = tk.Button(right_frame, text="Add Customer", font=("Helvetica", 12), bg=button_color, fg="white", borderwidth=2, relief="flat", padx=10, pady=5)
    button_add_customer.pack(pady=10, padx=10, fill="x")

    button_search_customer = tk.Button(right_frame, text="Search Customer", font=("Helvetica", 12), bg=button_color, fg="white", borderwidth=2, relief="flat", padx=10, pady=5)
    button_search_customer.pack(pady=10, padx=10, fill="x")

    button_remove_customer = tk.Button(right_frame, text="Remove Customer", font=("Helvetica", 12), bg=button_color, fg="white", borderwidth=2, relief="flat", padx=10, pady=5)
    button_remove_customer.pack(pady=10, padx=10, fill="x")

    button_logout = tk.Button(right_frame, text="Logout", font=("Helvetica", 12), bg=button_color, fg="white", borderwidth=2, relief="flat", padx=10, pady=5)
    button_logout.pack(pady=10, padx=10, fill="x")

# Main Login Function
def login():
    global entry_username, entry_password  

    username = entry_username.get()
    password = entry_password.get()

    if username == "Admin" and password == "123":
        messagebox.showinfo("Login", "Login Successful!")
        root.destroy()  
        open_home_page()  
    else:
        messagebox.showerror("Login", "Invalid username or password")

# Create main window (Login window)
root = tk.Tk()  
root.title("Library Management System - Login")
root.geometry("800x500")  

#color 
bg_color = "#E8F0F2"
fg_color = "#333333"
button_color = "#00796B"

root.config(bg=bg_color)

# Create Frames for layout
frame = tk.Frame(root, bg=bg_color)
frame.pack(pady=20)

# Labels for Login
label_title = tk.Label(frame, text="Admin Login", font=("Helvetica", 16), bg=bg_color, fg=fg_color)
label_title.grid(row=0, column=0, columnspan=2, pady=10)

label_username = tk.Label(frame, text="Username:", font=("Helvetica", 12), bg=bg_color, fg=fg_color)
label_username.grid(row=1, column=0, pady=10, padx=10, sticky="e")

label_password = tk.Label(frame, text="Password:", font=("Helvetica", 12), bg=bg_color, fg=fg_color)
label_password.grid(row=2, column=0, pady=10, padx=10, sticky="e")

# Entry fields for Login
entry_username = tk.Entry(frame, font=("Helvetica", 12))
entry_username.grid(row=1, column=1, pady=10, padx=10)

entry_password = tk.Entry(frame, font=("Helvetica", 12), show="*")
entry_password.grid(row=2, column=1, pady=10, padx=10)

# Login Button
button_login = tk.Button(frame, text="Login", font=("Helvetica", 12), bg=button_color, fg="white", command=login)
button_login.grid(row=3, column=0, columnspan=2, pady=20)

# Start
root.mainloop()
