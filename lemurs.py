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

    left_frame = tk.Frame(home_window, bg=left_frame_color, width=1)  
    left_frame.pack(side="left", fill="y")  

    # Heading for left frame
    label_books = tk.Label(left_frame, text="Books", font=("Helvetica", 16, "bold"), bg=left_frame_color, fg=text_color)
    label_books.pack(pady=20)

    # Buttons for left frame
    button_add_book = tk.Button(left_frame, text="List Books", font=("Helvetica", 12), bg=button_color, fg="white", borderwidth=2, relief="flat", padx=10, pady=5)
    button_add_book.pack(pady=10, padx=10, fill="x")

    button_assign_book = tk.Button(left_frame, text="Create Book", font=("Helvetica", 12), bg=button_color, fg="white", borderwidth=2, relief="flat", padx=10, pady=5)
    button_assign_book.pack(pady=10, padx=10, fill="x")

    # Create Frames for layout
    remaining_frame = tk.Frame(root, bg=bg_color)
    remaining_frame.pack(fill='both', expand=True)
    
    # Grid-based layout for the remaining_frame
    for i in range(3):
        remaining_frame.grid_columnconfigure(i, weight=1)
    for i in range(3):
        remaining_frame.grid_rowconfigure(i, weight=1)

    # Add rectangles with labels within and below them
    for i in range(3):
        for j in range(3):
            rect_label = tk.Label(remaining_frame, text=f"Rectangle {i}{j}", font=("Helvetica", 10), bg="white", fg="black")
            rect_label.grid(row=i, column=j, padx=10, pady=10, sticky="nsew")

    home_window.mainloop()

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
bg_color = "#F2E5BF"
fg_color = "#257180"
button_color = "#257180"

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
