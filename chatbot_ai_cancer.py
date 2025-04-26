import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk, ImageEnhance
import os
import smtplib
import sqlite3
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------- Database Setup ----------------
conn = sqlite3.connect("users.db")
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT)''')
conn.commit()


# ---------------- Email Sending Function ----------------
def send_email(recipient_email, subject, body):
    try:
        sender_email = "your_email@example.com"  # Replace with your email
        sender_password = "your_password"  # Replace with your password

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        messagebox.showinfo("Success", "Email sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {e}")

# ---------------- Global Variables ----------------
selected_cancer_type = ""
prediction_result = ""


# ---------------- Chatbot Functions ----------------
def chatbot_response():
    global selected_cancer_type, prediction_result

    user_input = entry_box.get().lower()
    entry_box.delete(0, tk.END)
    response = ""
    image_path = None

    if "hello" in user_input or "hi" in user_input:
        response = "Hello! I am a Cancer Prediction Chatbot. How can I help you?"

    elif "what is cancer" in user_input:
        response = "Cancer is a disease where cells in the body grow uncontrollably. It can occur in various parts of the body and may spread to other areas."

    elif "what causes cancer" in user_input:
        response = "Cancer can be caused by genetic mutations, lifestyle factors such as smoking, and environmental factors like exposure to carcinogens."

    elif "what are the early signs of breast cancer" in user_input:
        response = "Early signs of breast cancer may include a lump in the breast, changes in the shape or size of the breast, or abnormal discharge from the nipple."

    elif "can cancer be prevented?" in user_input:
        response = "While not all cancers can be prevented, healthy lifestyle choices like avoiding smoking, maintaining a healthy diet, and getting regular screenings can help reduce the risk."

    elif "how does smoking increase the risk of lung cancer?" in user_input:
        response = "Smoking damages the lungs and increases the risk of mutations in lung cells, leading to lung cancer. The more a person smokes, the higher the risk."

    elif "what is the difference between benign and malignant tumors?" in user_input:
        response = "Benign tumors are non-cancerous and do not spread to other parts of the body, while malignant tumors are cancerous and can spread (metastasize) to other areas."

    elif "is cancer genetic" in user_input or "hereditary" in user_input:
        response = "Some cancers are hereditary due to inherited gene mutations, but most are caused by lifestyle and environmental factors."

    elif "how is cancer diagnosed" in user_input:
        response = "Cancer can be diagnosed using imaging tests (MRI, CT scans), blood tests, biopsies, and lab tests depending on the suspected type."

    elif "what is chemotherapy" in user_input:
        response = "Chemotherapy is a treatment that uses drugs to kill or stop the growth of cancer cells. It may have side effects like fatigue or nausea."

    elif "what is radiation therapy" in user_input:
        response = "Radiation therapy uses high-energy radiation to destroy cancer cells or shrink tumors."

    elif "can children get cancer" in user_input:
        response = "Yes, cancer can occur in children. Common types include leukemia, brain tumors, and lymphomas."

    elif "what is metastasis" in user_input:
        response = "Metastasis refers to the spread of cancer cells from the original site to other parts of the body."

    elif "what are cancer stages" in user_input:
        response = "Cancer stages describe how far cancer has spread. Stage 0 means early cancer, while Stage IV indicates advanced spread to other parts of the body."

    elif "is cancer contagious" in user_input:
        response = "No, cancer is not contagious. It cannot be passed from one person to another like an infection."

    elif "can stress cause cancer" in user_input:
        response = "Stress itself doesn't directly cause cancer, but it may weaken the immune system or contribute to unhealthy habits."

    elif "can cancer come back" in user_input:
        response = "Yes, even after successful treatment, cancer can sometimes return. Regular follow-ups are essential."

    elif "how can i reduce cancer risk" in user_input:
        response = "You can reduce your risk by not smoking, eating healthy, staying physically active, getting vaccinated, and having regular screenings."

    elif "breast cancer" in user_input:
        selected_cancer_type = "Breast Cancer"
        response = "Do you have a lump in the breast, nipple discharge, or skin changes? (yes/no)"
        image_path = os.path.join("assets", "breast_cancer.jpg")

    elif "lung cancer" in user_input:
        selected_cancer_type = "Lung Cancer"
        response = "Do you experience persistent cough, chest pain, or shortness of breath? (yes/no)"
        image_path = os.path.join("assets", "lung_cancer.jpg")

    elif "skin cancer" in user_input:
        selected_cancer_type = "Skin Cancer"
        response = "Do you have new or changing moles, irregular skin patches, or sores that won't heal? (yes/no)"
        image_path = os.path.join("assets", "skin_cancer.jpg")

    elif "colorectal cancer" in user_input:
        selected_cancer_type = "Colorectal Cancer"
        response = "Do you have persistent changes in bowel habits, blood in stool, or abdominal pain? (yes/no)"
        image_path = os.path.join("assets", "colorectal_cancer.jpg")

    elif "brain cancer" in user_input:
        selected_cancer_type = "Brain Cancer"
        response = "Do you experience headaches, seizures, or vision problems? (yes/no)"
        image_path = os.path.join("assets", "brain_cancer.jpg")

    elif "liver cancer" in user_input:
        selected_cancer_type = "Liver Cancer"
        response = "Do you have abdominal pain, weight loss, or jaundice? (yes/no)"
        image_path = os.path.join("assets", "liver_cancer.jpg")

    elif "kidney cancer" in user_input:
        selected_cancer_type = "Kidney Cancer"
        response = "Do you have blood in urine, lower back pain, or unexplained weight loss? (yes/no)"
        image_path = os.path.join("assets", "kidney_cancer.jpg")

    elif "bladder cancer" in user_input:
        selected_cancer_type = "Bladder Cancer"
        response = "Do you experience blood in urine, frequent urination, or pelvic pain? (yes/no)"
        image_path = os.path.join("assets", "bladder_cancer.jpg")
    elif user_input in ["yes", "y"]:
        prediction_result = f"{selected_cancer_type}: Symptoms suggest a possible risk. Please consult a doctor."
        response = prediction_result
    elif user_input in ["no", "n"]:
        prediction_result = f"{selected_cancer_type}: No immediate risk detected based on your answers."
        response = prediction_result
    elif "exit" in user_input or "quit" in user_input:
        root.quit()
    else:
        response = "I didn't understand that. Ask about Breast, Lung, Skin, Colorectal, Brain, Liver, Kidney, or Bladder Cancer, or questions about cancer itself."


    chat_window.config(state=tk.NORMAL)
    chat_window.insert(tk.END, f"You: {user_input}\n", "user")
    chat_window.insert(tk.END, f"Bot: {response}\n\n", "bot")
    chat_window.config(state=tk.DISABLED)
    chat_window.yview(tk.END)

    if image_path and os.path.exists(image_path):
        img = Image.open(image_path).resize((280, 200), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        image_label.config(image=photo)
        image_label.image = photo
    else:
        image_label.config(image="", text="")


def play_animation():
    gif_path = os.path.join("assets", "cancer_animation.gif")

    if not os.path.exists(gif_path):
        messagebox.showerror("Error", "Animation GIF not found.")
        return

    top = tk.Toplevel(root)
    top.title("How Cancer Damages Cells")
    top.geometry("600x450")
    top.configure(bg="white")

    label = tk.Label(top, bg="white")
    label.pack()

    # Load frames from gif
    frames = []
    gif = Image.open(gif_path)

    try:
        while True:
            frame = ImageTk.PhotoImage(gif.copy().resize((550, 400), Image.LANCZOS))
            frames.append(frame)
            gif.seek(gif.tell() + 1)
    except EOFError:
        pass

    # Loop animation
    def update_frame(frame_idx=0):
        label.config(image=frames[frame_idx])
        frame_idx = (frame_idx + 1) % len(frames)
        top.after(100, update_frame, frame_idx)

    update_frame()  # start animation


# ---------------- Report Page Function ----------------
def show_report_page():
    # Create a new Toplevel window for the report page
    report_win = tk.Toplevel(root)
    report_win.title("Detailed Report")
    report_win.geometry("500x400")

    # Dummy numeric report values (replace with actual values if available)
    report_values = {
        "Radius": "14.2",
        "Texture": "21.5",
        "Perimeter": "89.4",
        "Area": "115.0",
        "Smoothness": "0.12",
        "Compactness": "0.15",
        "Concavity": "0.20",
        "Concave Points": "0.07"
    }

    # Title label
    tk.Label(report_win, text="Numeric Report", font=("Arial", 16, "bold")).pack(pady=10)

    # Create a frame to hold the report details
    report_frame = tk.Frame(report_win)
    report_frame.pack(pady=10)

    # Display each report parameter and its value
    for i, (key, value) in enumerate(report_values.items()):
        tk.Label(report_frame, text=f"{key}:", font=("Arial", 12)).grid(row=i, column=0, sticky="e", padx=10, pady=5)
        tk.Label(report_frame, text=value, font=("Arial", 12)).grid(row=i, column=1, sticky="w", padx=10, pady=5)

    # Back button to close the report window
    tk.Button(report_win, text="Back", font=("Arial", 12), bg="gray", fg="white",
              command=report_win.destroy).pack(pady=20)

    def play_animation():
        gif_path = os.path.join("assets", "cancer_animation.gif")
        if not os.path.exists(gif_path):
            messagebox.showerror("Error", "Animation GIF not found.")
            return

        top = tk.Toplevel(root)
        top.title("How Cancer Damages Cells")
        top.geometry("600x450")
        top.configure(bg="white")

        label = tk.Label(top, bg="white")
        label.pack()

        # Load frames from gif
        frames = []
        gif = Image.open(gif_path)
        try:
            while True:
                frame = ImageTk.PhotoImage(gif.copy().resize((550, 400)))
                frames.append(frame)
                gif.seek(len(frames))
        except EOFError:
            pass

        def update(index):
            frame = frames[index]
            label.config(image=frame)
            top.after(100, update, (index + 1) % len(frames))

        update(0)


# ---------------- Chatbot UI ----------------
def open_chatbot():
    login_win.destroy()
    global root, entry_box, chat_window, image_label, email_entry

    root = tk.Tk()
    root.title("Cancer Prediction Chatbot")
    root.geometry("900x700")

    # Background image
    bg_image = Image.open("assets/chatbot_bg.jpg").resize((900, 700), Image.LANCZOS)
    enhancer = ImageEnhance.Brightness(bg_image)
    faint_bg = enhancer.enhance(0.5)
    bg_photo = ImageTk.PhotoImage(faint_bg)

    canvas = tk.Canvas(root, width=900, height=700)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")

    # Heading
    heading_label = tk.Label(root, text="Cancer Prediction AI Chatbot",
                             font=("Arial", 20, "bold"), bg="#003366", fg="white", pady=15)
    canvas.create_window(450, 40, window=heading_label)

    # Main frame (holds left and right sections)
    main_frame = tk.Frame(root, bg="white")
    canvas.create_window(450, 220, window=main_frame)

    # Left section frame (for image only)
    left_side_frame = tk.Frame(main_frame, bg="white")
    left_side_frame.pack(side="left", fill="y", padx=(20, 10), pady=10)
    image_label = tk.Label(left_side_frame, bg="white")
    image_label.pack(pady=10)

    # Right section frame for chat window and buttons
    right_side_frame = tk.Frame(main_frame, bg="white")
    right_side_frame.pack(side="left", fill="both", expand=True, padx=(10, 20), pady=10)

    # Frame to hold "Thank You" and "Logout" buttons at the top of the right side
    right_button_frame = tk.Frame(right_side_frame, bg="white")
    right_button_frame.pack(fill="x", pady=(0, 10))
    thank_you_button = tk.Button(right_button_frame, text="Thank You",
                                 command=lambda: messagebox.showinfo("Thank You", "Stay healthy!"),
                                 font=("Arial", 12), bg="orange", width=15)
    thank_you_button.pack(side="right", padx=5)
    logout_button = tk.Button(right_button_frame, text="Logout",
                              command=lambda: [root.destroy(), login_window()],
                              font=("Arial", 12), bg="red", fg="white", width=15)
    logout_button.pack(side="right", padx=5)
    play_button = tk.Button(right_button_frame, text="Play Animation", font=("Arial", 12), bg="#4CAF50", fg="white",
                            command=play_animation)
    play_button.pack(side="left", padx=10)

    # Chat window in the right section below the buttons
    chat_window = scrolledtext.ScrolledText(right_side_frame, wrap=tk.WORD,
                                            state=tk.DISABLED, width=60, height=15,
                                            font=("Arial", 12), bg="#f0f0f0")
    chat_window.pack(fill="both", expand=True)

    # Entry area for user input (placed below via canvas)
    entry_frame = tk.Frame(root, bg="white")
    canvas.create_window(450, 430, window=entry_frame)
    entry_box = tk.Entry(entry_frame, width=50, font=("Arial", 14), bg="#f0f0f0", bd=2, relief="solid")
    entry_box.grid(row=0, column=0, padx=10)
    send_button = tk.Button(entry_frame, text="Send", command=chatbot_response,
                            font=("Arial", 12, "bold"), bg="blue", fg="white", width=10)
    send_button.grid(row=0, column=1)

    # Email frame for email entry and Send Report button (side-by-side)
    email_frame = tk.Frame(root, bg="white")
    canvas.create_window(450, 480, window=email_frame)
    email_label = tk.Label(email_frame, text="Enter Email ID:", bg="white", font=("Arial", 12))
    email_label.grid(row=0, column=0, padx=5, pady=5)
    email_entry = tk.Entry(email_frame, font=("Arial", 12), width=30)
    email_entry.grid(row=0, column=1, padx=5, pady=5)
    report_button = tk.Button(email_frame, text="Send Report via Mail", command=lambda: send_report(),
                              bg="dodger blue", fg="white", font=("Arial", 12, "bold"), width=20)
    report_button.grid(row=0, column=2, padx=5, pady=5)

    def send_report():
        if not selected_cancer_type or not prediction_result:
            messagebox.showwarning("Report", "Please complete a prediction first.")
            return
        recipient = email_entry.get()
        if recipient:
            report_body = (
                f"Report for {selected_cancer_type}:\n\n"
                f"Prediction Result: {prediction_result}\n\n"
                f"Note: This is an AI-based prediction. Kindly consult your doctor for confirmation."
            )
            send_email(recipient, f"Cancer Report - {selected_cancer_type}", report_body)
        else:
            messagebox.showwarning("Input Needed", "Please enter a recipient email.")

    # Frame for cancer type buttons
    button_frame = tk.Frame(root, bg="white")
    canvas.create_window(450, 610, window=button_frame)
    cancers = [
        ("Breast Cancer", "pink"),
        ("Lung Cancer", "gray"),
        ("Skin Cancer", "yellow"),
        ("Colorectal Cancer", "red"),
        ("Brain Cancer", "purple"),
        ("Liver Cancer", "#FFA07A"),
        ("Kidney Cancer", "#90EE90"),
        ("Bladder Cancer", "#87CEEB")
    ]
    for i, (name, color) in enumerate(cancers):
        row, col = divmod(i, 4)
        tk.Button(button_frame, text=name,
                  command=lambda n=name: [
                      entry_box.delete(0, tk.END),
                      entry_box.insert(0, n.lower()),
                      chatbot_response()
                  ],
                  bg=color, font=("Arial", 12, "bold"), width=18, height=2).grid(row=row, column=col, padx=10, pady=5)

    root.mainloop()


# ---------------- Login / Register UI ----------------
def login_window():
    global login_win
    login_win = tk.Tk()
    login_win.title("Login / Register")
    login_win.geometry("500x400")

    bg_img = Image.open("assets/login_bg.jpg").resize((500, 400), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_img)
    bg_label = tk.Label(login_win, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    tk.Label(login_win, text="Username:", bg="white").place(x=150, y=100)
    tk.Label(login_win, text="Password:", bg="white").place(x=150, y=150)
    username_entry = tk.Entry(login_win)
    username_entry.place(x=230, y=100)
    password_entry = tk.Entry(login_win, show="*")
    password_entry.place(x=230, y=150)

    def login():
        user = username_entry.get()
        pw = password_entry.get()
        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pw))
        if cur.fetchone():
            messagebox.showinfo("Login", "Login Successful")
            open_chatbot()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register():
        user = username_entry.get()
        pw = password_entry.get()
        try:
            cur.execute("INSERT INTO users VALUES (?, ?)", (user, pw))
            conn.commit()
            messagebox.showinfo("Register", "User registered successfully")
        except:
            messagebox.showerror("Register Failed", "Username already exists")

    tk.Button(login_win, text="Login", command=login).place(x=180, y=200)
    tk.Button(login_win, text="Register", command=register).place(x=260, y=200)

    login_win.mainloop()


# ---------------- Main Entry ----------------
if __name__ == "__main__":
    login_window()
