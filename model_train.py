import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import joblib

# Database setup
conn = sqlite3.connect('cancer_chatbot.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, email TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS predictions (username TEXT, cancer_type TEXT, prediction TEXT)''')
conn.commit()
conn.close()

selected_cancer_type = ""
prediction_result = ""

# Function to send email
def send_email(recipient_email, subject, body):
    sender_email = "your_email@gmail.com"  # Replace with your email
    sender_password = "your_password"  # Replace with your app password

    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    message.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")

# Function to predict cancer
def run_prediction():
    try:
        model = joblib.load("breast_cancer_model.pkl")
        features = [
            int(lump_entry.get()),
            int(discharge_entry.get()),
            int(skin_entry.get())
        ]
        result = model.predict([features])[0]
        global selected_cancer_type, prediction_result
        selected_cancer_type = "Breast Cancer"
        prediction_result = "High Risk of Breast Cancer" if result == 1 else "Low Risk of Breast Cancer"
        messagebox.showinfo("Prediction", prediction_result)

        # Save prediction to DB
        conn = sqlite3.connect('cancer_chatbot.db')
        c = conn.cursor()
        c.execute("INSERT INTO predictions (username, cancer_type, prediction) VALUES (?, ?, ?)",
                  (current_user, selected_cancer_type, prediction_result))
        conn.commit()
        conn.close()

    except Exception as e:
        messagebox.showerror("Error", f"Prediction failed: {e}")

# Function to show chatbot window
def open_chatbot(username):
    global lump_entry, discharge_entry, skin_entry, current_user
    current_user = username

    root = tk.Toplevel()
    root.title("Cancer Prediction Chatbot")
    root.geometry("900x700")

    chat_frame = tk.Frame(root, bg="white")
    chat_frame.pack(pady=10)

    chat_log = tk.Text(chat_frame, height=20, width=100, bg="lightyellow")
    chat_log.pack()

    def respond_to_query():
        user_query = user_input.get()
        chat_log.insert(tk.END, "You: " + user_query + "\n")
        if "what is cancer" in user_query.lower():
            response = "Cancer is a disease caused when cells divide uncontrollably and spread."
        else:
            response = "I am here to help with cancer-related questions."
        chat_log.insert(tk.END, "Bot: " + response + "\n")
        user_input.delete(0, tk.END)

    user_input = tk.Entry(root, width=60)
    user_input.pack(pady=10)
    send_button = tk.Button(root, text="Send", command=respond_to_query)
    send_button.pack()

    def set_cancer_type(cancer):
        global selected_cancer_type
        selected_cancer_type = cancer
        chat_log.insert(tk.END, f"Bot: You selected {cancer}.\n")
        try:
            image = Image.open(f"images/{cancer.lower().replace(' ', '_')}.jpg")
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)
            img_label.config(image=photo)
            img_label.image = photo
        except:
            chat_log.insert(tk.END, "Bot: Image not found.\n")

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    for cancer in ["Breast Cancer", "Lung Cancer", "Liver Cancer", "Bladder Cancer"]:
        tk.Button(button_frame, text=cancer, command=lambda c=cancer: set_cancer_type(c)).pack(side=tk.LEFT, padx=5)

    img_label = tk.Label(root)
    img_label.pack()

    prediction_frame = tk.LabelFrame(root, text="Cancer Prediction Form", font=("Arial", 12, "bold"), padx=10, pady=10, bg="white")
    prediction_frame.pack(pady=10)

    tk.Label(prediction_frame, text="Lump (0/1):", bg="white").grid(row=0, column=0, padx=5, pady=5)
    lump_entry = tk.Entry(prediction_frame, width=5)
    lump_entry.grid(row=0, column=1)

    tk.Label(prediction_frame, text="Discharge (0/1):", bg="white").grid(row=0, column=2, padx=5, pady=5)
    discharge_entry = tk.Entry(prediction_frame, width=5)
    discharge_entry.grid(row=0, column=3)

    tk.Label(prediction_frame, text="Skin Changes (0/1):", bg="white").grid(row=0, column=4, padx=5, pady=5)
    skin_entry = tk.Entry(prediction_frame, width=5)
    skin_entry.grid(row=0, column=5)

    def auto_fill_form():
        lump_entry.delete(0, tk.END)
        discharge_entry.delete(0, tk.END)
        skin_entry.delete(0, tk.END)
        lump_entry.insert(0, "1")
        discharge_entry.insert(0, "1")
        skin_entry.insert(0, "0")

    auto_fill_form()

    tk.Button(prediction_frame, text="Predict Breast Cancer", bg="blue", fg="white",
              command=run_prediction, font=("Arial", 12, "bold")).grid(row=1, column=0, columnspan=6, pady=10)

    def send_report():
        conn = sqlite3.connect('cancer_chatbot.db')
        c = conn.cursor()
        c.execute("SELECT email FROM users WHERE username=?", (username,))
        email = c.fetchone()[0]
        conn.close()
        subject = "Cancer Prediction Report"
        body = f"Dear {username},\n\nPrediction for {selected_cancer_type}: {prediction_result}"
        send_email(email, subject, body)

    tk.Button(root, text="Send Report via Email", bg="green", fg="white",
              command=send_report, font=("Arial", 12)).pack(pady=10)

    tk.Button(root, text="Thank You", bg="orange", fg="white", font=("Arial", 12), command=root.destroy).pack(pady=5)
    tk.Button(root, text="Logout", bg="red", fg="white", font=("Arial", 12), command=root.destroy).pack(pady=5)

# Register function
def register():
    reg_win = tk.Toplevel()
    reg_win.title("Register")
    reg_win.geometry("400x300")

    bg = Image.open("images/bg.jpg")
    bg = ImageTk.PhotoImage(bg.resize((400, 300)))
    bg_label = tk.Label(reg_win, image=bg)
    bg_label.image = bg
    bg_label.place(x=0, y=0)

    tk.Label(reg_win, text="Username").pack()
    username = tk.Entry(reg_win)
    username.pack()

    tk.Label(reg_win, text="Password").pack()
    password = tk.Entry(reg_win, show="*")
    password.pack()

    tk.Label(reg_win, text="Email").pack()
    email = tk.Entry(reg_win)
    email.pack()

    def save_user():
        conn = sqlite3.connect('cancer_chatbot.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users VALUES (?, ?, ?)", (username.get(), password.get(), email.get()))
            conn.commit()
            messagebox.showinfo("Success", "Registered successfully!")
            reg_win.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")
        conn.close()

    tk.Button(reg_win, text="Register", command=save_user).pack()

# Login function
def login():
    conn = sqlite3.connect('cancer_chatbot.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (user_entry.get(), pass_entry.get()))
    result = c.fetchone()
    conn.close()
    if result:
        messagebox.showinfo("Login Success", "Welcome!")
        root.destroy()
        open_chatbot(user_entry.get())
    else:
        messagebox.showerror("Error", "Invalid credentials")

# Main login/register screen
root = tk.Tk()
root.title("Cancer Chatbot Login")
root.geometry("400x300")

bg = Image.open("images/bg.jpg")
bg = ImageTk.PhotoImage(bg.resize((400, 300)))
bg_label = tk.Label(root, image=bg)
bg_label.image = bg
bg_label.place(x=0, y=0)

user_entry = tk.Entry(root)
pass_entry = tk.Entry(root, show="*")

tk.Label(root, text="Username", bg="lightblue").pack(pady=5)
user_entry.pack(pady=5)

tk.Label(root, text="Password", bg="lightblue").pack(pady=5)
pass_entry.pack(pady=5)

tk.Button(root, text="Login", command=login).pack(pady=5)
tk.Button(root, text="Register", command=register).pack(pady=5)

root.mainloop()
