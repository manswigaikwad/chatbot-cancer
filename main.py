import tkinter as tk
from tkinter import messagebox
from chatbot import open_chatbot
from PIL import Image, ImageTk

# Dummy user storage
users = {}

# ---- Login/Register Window ----
def show_login_register():
    def login():
        username = username_entry.get()
        password = password_entry.get()
        if username in users and users[username] == password:
            messagebox.showinfo("Login", "Login Successful!")
            login_window.destroy()
            open_chatbot()  # Launch chatbot window
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register():
        username = username_entry.get()
        password = password_entry.get()
        if username in users:
            messagebox.showwarning("Register", "Username already exists.")
        else:
            users[username] = password
            messagebox.showinfo("Register", "Registration Successful! You can now log in.")

    # --- UI Setup ---
    global login_window
    login_window = tk.Tk()
    login_window.title("Login/Register")
    login_window.geometry("800x500")

    bg_image = Image.open("assets/login_bg.jpg")
    bg_image = bg_image.resize((800, 500), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(login_window, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    login_frame = tk.Frame(login_window, bg="white", bd=5, relief="ridge")
    login_frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(login_frame, text="Username:", font=("Arial", 14), bg="white").grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(login_frame, font=("Arial", 14), width=25)
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(login_frame, text="Password:", font=("Arial", 14), bg="white").grid(row=1, column=0, padx=10, pady=10)
    password_entry = tk.Entry(login_frame, font=("Arial", 14), width=25, show="*")
    password_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(login_frame, text="Login", command=login, bg="#003366", fg="white",
              font=("Arial", 12, "bold"), width=12).grid(row=2, column=0, pady=10)
    tk.Button(login_frame, text="Register", command=register, bg="#006600", fg="white",
              font=("Arial", 12, "bold"), width=12).grid(row=2, column=1, pady=10)

    login_window.mainloop()

# Start here
show_login_register()
