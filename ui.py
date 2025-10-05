import customtkinter as ctk
from backend import summary_gen, flashcards_gen, quiz_gen, formula_gen
import customtkinter as ctk
from tkinter import filedialog, messagebox
from openai import OpenAI
import fitz  # PyMuPDF for PDF reading
from docx import Document
from PIL import Image
import os



def not_available_popup():
    messagebox.showinfo("Feature Unavailable", "This feature is not available yet.")

def open_profile():
    
    print("Open Profile Page")

def open_settings():
    print("Open Settings")

def open_notifications():
    print("Open Notifications")

def upload_notes():
    uploaded_content = ""

    def extract_pdf_text(file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def extract_docx_text(file_path):
        doc = Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)

    def select_file():
        nonlocal uploaded_content
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=[("Documents", "*.pdf *.docx *.txt"), ("All files", "*.*")]
        )
        if not file_path:
            return
        try:
            if file_path.lower().endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    uploaded_content = f.read()
            elif file_path.lower().endswith(".pdf"):
                uploaded_content = extract_pdf_text(file_path)
            elif file_path.lower().endswith(".docx"):
                uploaded_content = extract_docx_text(file_path)
            else:
                uploaded_content = ""
                messagebox.showwarning("❌Unsupported File", "File type not supported for preview.❌")
                disable_action_buttons()
                return
            status_label.configure(text="✅File uploaded! Choose an action✅", text_color="green")
            enable_action_buttons()
            output_textbox.configure(state="normal")
            output_textbox.delete("1.0", ctk.END)
            output_textbox.configure(state="disabled")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file:\n{e}")
            disable_action_buttons()

    def disable_action_buttons():
        for btn in action_buttons:
            btn.configure(state="disabled")

    def enable_action_buttons():
        for btn in action_buttons:
            btn.configure(state="normal")

    def call_summary():
        if not uploaded_content:
            messagebox.showwarning("😄No Content", "Upload a file first.")
            return
        try:
            result = summary_gen(uploaded_content, client)
        except Exception as e:
            messagebox.showerror("API Error", f"Summary generation failed:\n{e}")
            return
        show_output(result)

    def call_flashcards():
        if not uploaded_content:
            messagebox.showwarning("No Content", "Upload a file first.")
            return
        try:
            result = flashcards_gen(uploaded_content, client)
        except Exception as e:
            messagebox.showerror("API Error", f"Flashcards generation failed:\n{e}")
            return
        show_output(result)

    def call_quiz():
        if not uploaded_content:
            messagebox.showwarning("No Content", "Upload a file first.")
            return
        try:
            result = quiz_gen(uploaded_content, client)
        except Exception as e:
            messagebox.showerror("API Error", f"Quiz generation failed:\n{e}")
            return
        show_output(result)

    def call_formulas():
        if not uploaded_content:
            messagebox.showwarning("No Content", "Upload a file first.")
            return
        try:
            result = formula_gen(uploaded_content, client)
        except Exception as e:
            messagebox.showerror("API Error", f"Formula extraction failed:\n{e}")
            return
        show_output(result)

    def show_output(text):
        output_textbox.configure(state="normal")
        output_textbox.delete("1.0", ctk.END)
        output_textbox.insert(ctk.END, text)
        output_textbox.configure(state="disabled")


    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTk()
    app.geometry("600x800")
    app.title("Upload Your Notes")

    # Top bar with icons
    top_bar = ctk.CTkFrame(app, height=50)
    top_bar.pack(fill="x", side="top")
    ctk.CTkLabel(top_bar, text="Study Hub").pack(side="left", padx=10)

    icons_frame = ctk.CTkFrame(top_bar)
    icons_frame.pack(side="right", padx=10)
    ctk.CTkButton(icons_frame, text="👤", width=40, height=40, command=not_available_popup).pack(side="left", padx=6)
    ctk.CTkButton(icons_frame, text="⚙️", width=40, height=40, command=not_available_popup).pack(side="left", padx=6)
    ctk.CTkButton(icons_frame, text="🔔", width=40, height=40, command=not_available_popup).pack(side="left", padx=6)

    # Header label
    header_label = ctk.CTkLabel(app, text="Upload your lecture notes (PDF, DOCX, TXT)", font=ctk.CTkFont(size=22, weight="bold"))
    header_label.pack(pady=20)

    btn_frame = ctk.CTkFrame(app)
    btn_frame.pack(pady=10)
    ctk.CTkButton(btn_frame, text="📎 Select File", width=140, command=select_file).pack(side="left", padx=20)
    ctk.CTkButton(btn_frame, text="✏️ Paste Text Manually", width=160, command=lambda: messagebox.showinfo("Info", "Manual paste not implemented yet.")).pack(side="left", padx=20)

    actions_frame = ctk.CTkFrame(app)
    actions_frame.pack(pady=15, padx=20, fill="x")

    summarize_btn = ctk.CTkButton(actions_frame, text="📝 Summarize", command=call_summary, state="disabled")
    flashcards_btn = ctk.CTkButton(actions_frame, text="🃏 Generate Flashcards", command=call_flashcards, state="disabled")
    quiz_btn = ctk.CTkButton(actions_frame, text="🧩 Take Quiz", command=call_quiz, state="disabled")
    formulas_btn = ctk.CTkButton(actions_frame, text="📐 Extract Formulas", command=call_formulas, state="disabled")

    summarize_btn.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    flashcards_btn.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    quiz_btn.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
    formulas_btn.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

    actions_frame.grid_columnconfigure((0, 1), weight=1)

    action_buttons = [summarize_btn, flashcards_btn, quiz_btn, formulas_btn]

    # Status label
    status_label = ctk.CTkLabel(app, text="Upload a file to enable actions.", font=ctk.CTkFont(size=14))
    status_label.pack(pady=(10, 20))

    # Output text box (readonly)
    output_textbox = ctk.CTkTextbox(app, width=560, height=300, corner_radius=12, wrap="word")
    output_textbox.pack(padx=20)
    output_textbox.configure(state="disabled")

    # Bottom nav placeholder
    bottom_nav = ctk.CTkFrame(app, height=60)
    bottom_nav.pack(side="bottom", fill="x")

    nav_buttons = [
        ("🏠 Home", lambda: print("Go Home")),
        ("🧑‍🤝‍🧑 Friends", lambda: print("Go Friends")),
        ("📊 Progress", lambda: print("Go Progress")),
        ("🎮 Challenges", lambda: print("Go Challenges")),
        ("⚙️ Settings", lambda: print("Go Settings"))
    ]

    for text, cmd in nav_buttons:
        btn = ctk.CTkButton(bottom_nav, text=text, command=cmd, corner_radius=0,
                            fg_color="transparent", hover_color="#1F6AA5", font=ctk.CTkFont(size=14))
        btn.pack(side="left", expand=True, fill="both", padx=10)

    return app

def summarize_notes():
    upload_notes()
    print("Go to Summarize Notes")

def generate_flashcards():
    upload_notes()
    print("Go to Generate Flashcards")

def take_quiz():
    upload_notes()
    print("Go to Take Quiz")

def extract_formulas():
    upload_notes()
    print("Go to Extract Formulas & Key Terms")

def go_home():
    print("Go to Home")

def go_friends():
    print("Go to Friends")

def go_progress():
    print("Go to Progress")

def go_challenges():
    print("Go to Challenges")

def add_top_icon(parent, symbol, command):
    btn = ctk.CTkButton(parent, text=symbol, width=40, height=40, 
                        font=ctk.CTkFont(size=20), command=command, corner_radius=20)
    btn.pack(side="left", padx=6)

# Set appearance mode and theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def open_home_window():
    # app.destroy()

    # Create the next window
    home_window = ctk.CTk()
    home_window.geometry("1420x1080")
    home_window.title("Home")
    # home_window.wm_iconbitmap("/Users/admin/Desktop/Competitions/SUDS_Hackathon/other_files/app_logo.avif")

    top_bar = ctk.CTkFrame(home_window, height=50)
    top_bar.pack(fill="x", side="top")
    ctk.CTkLabel(top_bar, text="").pack(side="left", padx=10)  # left spacer
    
    icons_frame = ctk.CTkFrame(top_bar)
    icons_frame.pack(side="right", padx=10)
    
    add_top_icon(icons_frame, "👤", open_profile)
    add_top_icon(icons_frame, "⚙️", open_settings)
    add_top_icon(icons_frame, "🔔", open_notifications)
    
    greeting = ctk.CTkLabel(home_window, text="Welcome Back, AlgoRhythms 👋", font=ctk.CTkFont(size=24, weight="bold"))
    greeting.pack(pady=(30, 20))
    
    # Quick actions frame
    qa_frame = ctk.CTkFrame(home_window)
    qa_frame.pack(padx=20, pady=10, fill="both", expand=True)
    
    btn_upload = ctk.CTkButton(qa_frame, text="📂 Upload Notes", command=upload_notes, corner_radius=12, height=100,
                           font=ctk.CTkFont(size=18, weight="bold"))
    btn_upload.grid(row=0, column=0, columnspan=2, padx=15, pady=15, sticky="nsew")

    # Other quick action buttons (2 column grid starting row 1)
    quick_actions = [
        ("🧠 Summarize Notes", summarize_notes),
        ("🪄 Generate Flashcards", generate_flashcards),
        ("🧩 Take a Quiz", take_quiz),
        ("🔢 Extract Formulas & Key Terms", extract_formulas)
    ]

    for i, (text, cmd) in enumerate(quick_actions, start=1):
        btn = ctk.CTkButton(qa_frame, text=text, command=cmd, corner_radius=12, height=80,
                        font=ctk.CTkFont(size=16))
        btn.grid(row=(i+1)//2, column=(i-1) % 2, padx=15, pady=15, sticky="nsew")

    qa_frame.grid_rowconfigure([0, 1, 2], weight=1)
    qa_frame.grid_columnconfigure([0, 1], weight=1)

    # Bottom navigation bar
    bottom_nav = ctk.CTkFrame(home_window, height=60)
    bottom_nav.pack(side="bottom", fill="x")

    nav_buttons = [
        ("🏠 Home", go_home),
        ("🧑‍🤝‍🧑 Friends", go_friends),
        ("📊 Progress", go_progress),
        ("🎮 Challenges", go_challenges),
        ("⚙️ Settings", open_settings)
    ]

    for text, cmd in nav_buttons:
        btn = ctk.CTkButton(bottom_nav, text=text, command=cmd, corner_radius=0, fg_color="transparent", hover_color="#1F6AA5",
                            font=ctk.CTkFont(size=14))
        btn.pack(side="left", expand=True, fill="both", padx=10)
    
    
    # label1 = ctk.CTkLabel(home_window, text="Welcome Back!", font=("Helvetica", 20))
    # label2 = ctk.CTkLabel(home_window, text="Students upload their notes, and the app turns them into summaries, flashcards, quizzes, and formula sheets", font=("Helvetica", 20), wraplength=1000)
    # label1.pack(pady=50)
    # label2.pack(pady=50)

    home_window.mainloop()

# Create signup window


def signup():
    # opening text
    opening_label = ctk.CTkLabel(app, text="Welcome to the SprintStudy", font=("Helvetica", 25))
    opening_label2= ctk.CTkLabel(app, text="Here Students upload their notes, and the app turns them into summaries, flashcards, quizzes, and formula sheets", wraplength=1000)

    opening_label.pack(pady=10)
    opening_label2.pack(pady=10)


    # Username entry
    label_username = ctk.CTkLabel(app, text="Username:")
    label_username.pack(pady=(40,5))
    entry_username = ctk.CTkEntry(app, width=500)
    entry_username.pack(pady=5)

    # Password entry
    label_password = ctk.CTkLabel(app, text="Password:")
    label_password.pack(pady=5)
    entry_password = ctk.CTkEntry(app, show="*", width=500)
    entry_password.pack(pady=5)

    # Sign in button
    signin_button = ctk.CTkButton(app, text="Log In", command=open_home_window, width=300)
    signin_button.pack(pady=30)

    app.mainloop()

def signup2():
    
    side_img_data = Image.open("other_files/side-img.png").resize((750, 800))
    email_icon_data = Image.open("other_files/email-icon.png").resize((24, 24))
    password_icon_data = Image.open("other_files/password-icon.png").resize((20, 20))
    google_icon_data = Image.open("other_files/google-icon.png").resize((20, 20))
    
    side_img = ctk.CTkImage(dark_image=side_img_data, light_image=side_img_data, size=(750, 800))
    email_icon = ctk.CTkImage(dark_image=email_icon_data, light_image=email_icon_data, size=(24,24))
    password_icon = ctk.CTkImage(dark_image=password_icon_data, light_image=password_icon_data, size=(20,20))
    google_icon = ctk.CTkImage(dark_image=google_icon_data, light_image=google_icon_data, size=(20,20))

    ctk.CTkLabel(master=app, text="", image=side_img).pack(expand=True, side="left")

    frame = ctk.CTkFrame(master=app, width=500, height=680, fg_color="#ffffff")
    frame.pack_propagate(0)
    frame.pack(expand=True, side="right")

    ctk.CTkLabel(master=frame, text="Welcome Back!", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 35)).pack(anchor="w", pady=(60, 5), padx=(35, 0))
    ctk.CTkLabel(master=frame, text="Sign in to your account", text_color="#7E7E7E", anchor="w", justify="left", font=("Arial Bold", 12)).pack(anchor="w", padx=(35, 0))

    ctk.CTkLabel(master=frame, text="  Email:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 16), image=email_icon, compound="left").pack(anchor="w", pady=(48, 0), padx=(50, 0))
    ctk.CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000").pack(anchor="w", padx=(50, 0))

    ctk.CTkLabel(master=frame, text="  Password:", text_color="#601E88", anchor="w", justify="left", font=("Arial Bold", 16), image=password_icon, compound="left").pack(anchor="w", pady=(31, 0), padx=(50, 0))
    ctk.CTkEntry(master=frame, width=225, fg_color="#EEEEEE", border_color="#601E88", border_width=1, text_color="#000000", show="*").pack(anchor="w", padx=(50, 0))

    ctk.CTkButton(master=frame, text="Login", fg_color="#601E88", hover_color="#E44982", font=("Arial Bold", 14), text_color="#ffffff", width=225, command=lambda: open_welcome_page(open_home_window)).pack(anchor="w", pady=(50, 0), padx=(50, 0))
    ctk.CTkButton(master=frame, text="Continue With Google", fg_color="#EEEEEE", hover_color="#EEEEEE", font=("Arial Bold", 11), text_color="#601E88", width=275, image=google_icon).pack(anchor="w", pady=(30, 0), padx=(35, 0))

    app.mainloop()
    

def open_welcome_page(on_continue):
    
    # Background color (mild gradient effect using a frame, you could also use a bg image)
    bg = ctk.CTkFrame(app, fg_color="#f9e1fa")
    bg.place(x=0, y=0, relwidth=1, relheight=1)

    # Main branding: big title and subtitle
    title = ctk.CTkLabel(
        bg,
        text="SprintStudy📚",
        font=("Montserrat SemiBold", 52, "bold"),
        text_color="#601E88",
        bg_color="transparent"
    )
    title.place(relx=0.5, rely=0.14, anchor="center")

    subtitle = ctk.CTkLabel(
        bg,
        text="""Presented by AlgoRhythms:
        
            This app was built to make everyday problem-solving easier and more intuitive. 
            Whether you’re brainstorming ideas, organizing tasks, or generating content, it’s designed to give you clear, structured, 
            and helpful responses without the clutter.
            Our motivation was simple: we wanted a lightweight, personal assistant that feels fast and useful something that helps you think better, not just type faster""",
            
        font=("Lato", 20, "italic"),
        text_color="#E44982",
        bg_color="transparent",

        
    )
    subtitle.place(relx=0.5, rely=0.27, anchor="center")
    
    
    # Central team or logo image
    team_img_data = Image.open("other_files/team_image.png").resize((300, 560))
    app.team_img = ctk.CTkImage(light_image=team_img_data, dark_image=team_img_data, size=(260, 260))
    ctk.CTkLabel(bg, image=app.team_img, text="", bg_color="transparent").place(relx=0.5, rely=0.6, anchor="center")

    # label_ = ctk.CTkLabel(bg, text="""This app was built to make everyday problem-solving easier and more intuitive. 
    #                     Whether you’re brainstorming ideas, organizing tasks, or generating content, it’s designed to give you clear, structured, 
    #                     and helpful responses without the clutter.
    #                     Our motivation was simple: we wanted a lightweight, personal assistant that feels fast, human, and useful something that helps you think better, not just type faster""", wraplength=600)
    
    # label_.pack(pady=5)
    
    # subtitle1 = ctk.CTkLabel(
    #     bg,
    #     text="""Presented by AlgoRhythms:
    #         This app was built to make everyday problem-solving easier and more intuitive. 
    #         Whether you’re brainstorming ideas, organizing tasks, or generating content, it’s designed to give you clear, structured, 
    #         and helpful responses without the clutter.
    #         Our motivation was simple: we wanted a lightweight, personal assistant that feels fast, human, and useful something that helps you think better, not just type faster""",
            
    #         font=("Lato", 20, "italic"),
    #         text_color="#E44982",
    #         bg_color="transparent",
    #         # wraplength=800,
    # )
    # subtitle1.place(relx=1.5, rely=1.27, anchor="center")
    
    # Continue button design: floating, bold, rounded
    
    def _go_main():
        for widget in app.winfo_children():
            widget.destroy()
        on_continue()

    continue_btn = ctk.CTkButton(
        bg,
        text="Continue",
        font=("Montserrat SemiBold", 19),
        fg_color="#601E88",
        hover_color="#9B59B6",
        text_color="#ffffff",
        height=54,
        width=220,
        corner_radius=18,
        command=_go_main,
        border_width=2,
        border_color="#E44982"
    )
    continue_btn.place(relx=0.5, rely=0.85, anchor="center")
    
    app.mainloop()


if __name__ == "__main__":
    app = ctk.CTk()
    app.geometry("1420x1080")
    app.title("Log In Page")

    client = OpenAI(api_key=("sk-proj-fgiK2JJBytLimDDWj-TgKTenrTWq5lVc6wkkfoAtKcuAV2j52HEzFK" +
                    "JImKl09XS6c6Jtl8KxjQT3BlbkFJA46oPAdG3DCxwG-DXITmthCNciQXwI73o1-HiaAuqu0BT" +
                    "rWnZFXAuJHyRzMIZ3zL4SA5f1X1EA"))

    # team_img = Image.open("other_files/team_image.png")
    
    signup2()
    