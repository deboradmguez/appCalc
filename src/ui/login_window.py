import tkinter as tk
from tkinter import messagebox
from supabase import Client
from PIL import Image, ImageTk
from pathlib import Path
import logging

# Se importan los nuevos nombres de colores y estilos
from config import *

class LoginWindow:
    def __init__(self, master, supabase_client: Client, auth_service, app_state):
        self.master = master
        self.supabase_client = supabase_client
        self.auth_service = auth_service
        self.app_state = app_state
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # --- ESTILOS ACTUALIZADOS ---
        self.master.configure(bg=GRAPHITE)
        self.master.resizable(False, False)
        
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_me_var = tk.BooleanVar()
        self.is_login_mode = True

        main_frame = tk.Frame(self.master, bg=DARK_GRAY, relief='flat', 
                             highlightbackground=MEDIUM_GRAY, highlightthickness=1)
        main_frame.pack(padx=50, pady=50, fill=tk.BOTH, expand=True)

        content_frame = tk.Frame(main_frame, bg=DARK_GRAY)
        content_frame.pack(pady=20, padx=20)
        
        try:
            logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
            self.logo_img = Image.open(logo_path)
            self.logo_img = self.logo_img.resize((150, 150))
            self.logo_photo = ImageTk.PhotoImage(self.logo_img)
            
            logo_label = tk.Label(content_frame, image=self.logo_photo, bg=DARK_GRAY)
            logo_label.pack(pady=(20, 10))
        except FileNotFoundError:
            logging.error("No se encontró el archivo de logo. Asegúrate de que assets/logo.png existe.")
            
        self.title_label = tk.Label(content_frame, text="Iniciar Sesión", font=(FONT_PRIMARY, FONT_SIZE_TITLE, "bold"), fg=NEAR_WHITE, bg=DARK_GRAY)
        self.title_label.pack(pady=(0, 10))

        self.subtitle_label = tk.Label(content_frame, text="Bienvenido de nuevo.", font=(FONT_PRIMARY, FONT_SIZE_NORMAL), fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY)
        self.subtitle_label.pack(pady=(0, 20))

        self.email_entry = tk.Entry(content_frame, textvariable=self.email_var, **ENTRY_STYLE)
        self.email_entry.pack(fill=tk.X, padx=30, pady=(0, 10), ipady=5)
        self.email_entry.insert(0, "Email")
        self.email_entry.bind("<FocusIn>", self.on_entry_focus)
        self.email_entry.bind("<FocusOut>", self.on_entry_unfocus)
        
        self.password_entry = tk.Entry(content_frame, textvariable=self.password_var, show="", **ENTRY_STYLE)
        self.password_entry.pack(fill=tk.X, padx=30, pady=(0, 20), ipady=5)
        self.password_entry.insert(0, "Contraseña")
        self.password_entry.bind("<FocusIn>", self.on_entry_focus)
        self.password_entry.bind("<FocusOut>", self.on_entry_unfocus)

        self.login_btn = tk.Button(content_frame, text="Iniciar Sesión", command=self.login, **BUTTON_STYLE_PRIMARY)
        self.login_btn.pack(fill=tk.X, padx=30, ipady=8)
        
        self.toggle_btn = tk.Button(content_frame, text="¿No tienes cuenta? Regístrate aquí.", command=self.toggle_mode, **BUTTON_STYLE_SECONDARY)
        self.toggle_btn.pack(fill=tk.X, padx=30, pady=(10, 0), ipady=8)

        self.remember_me_check = tk.Checkbutton(content_frame, text="Recordar sesión", variable=self.remember_me_var,
                                               bg=DARK_GRAY, fg=LIGHT_GRAY_TEXT, selectcolor=DARK_GRAY,
                                               activebackground=DARK_GRAY, activeforeground=NEAR_WHITE,
                                               font=(FONT_PRIMARY, FONT_SIZE_SMALL))
        self.remember_me_check.pack(pady=10)

    # El resto de los métodos de la clase (on_closing, on_entry_focus, etc.) no cambian...
    def on_closing(self):
        self.app_state['is_closing'] = True
        self.master.destroy()

    def on_entry_focus(self, event):
        if event.widget.get() in ["Email", "Contraseña"]:
            event.widget.delete(0, tk.END)
        if event.widget == self.password_entry:
            event.widget.config(show="*")

    def on_entry_unfocus(self, event):
        if not event.widget.get():
            if event.widget == self.email_entry:
                event.widget.insert(0, "Email")
            elif event.widget == self.password_entry:
                event.widget.insert(0, "Contraseña")
                event.widget.config(show="")
    
    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        if self.is_login_mode:
            self.title_label.config(text="Iniciar Sesión")
            self.subtitle_label.config(text="Bienvenido de nuevo.")
            self.login_btn.config(text="Iniciar Sesión", command=self.login)
            self.toggle_btn.config(text="¿No tienes cuenta? Regístrate aquí.")
        else:
            self.title_label.config(text="Registrarse")
            self.subtitle_label.config(text="Crea tu cuenta.")
            self.login_btn.config(text="Registrarse", command=self.signup)
            self.toggle_btn.config(text="¿Ya tienes cuenta? Inicia sesión aquí.")

    def login(self):
        email = self.email_var.get().strip()
        password = self.password_var.get()

        if not email or not password:
            messagebox.showerror("Error", "Por favor, ingresa tu email y contraseña.")
            return

        try:
            auth_response = self.supabase_client.auth.sign_in_with_password({"email": email, "password": password})
            
            if auth_response:
                messagebox.showinfo("Éxito", "¡Inicio de sesión exitoso!")
                if self.remember_me_var.get():
                    self.auth_service.save_session(auth_response.session.refresh_token)
                self.master.destroy()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas.")
        except Exception as e:
            messagebox.showerror("Error", f"Error de inicio de sesión: {e}")

    def signup(self):
        email = self.email_var.get().strip()
        password = self.password_var.get()

        if not email or not password:
            messagebox.showerror("Error", "Por favor, ingresa un email y contraseña.")
            return

        try:
            auth_response = self.supabase_client.auth.sign_up({"email": email, "password": password})
            
            if auth_response:
                messagebox.showinfo("Registro Exitoso", "¡Cuenta creada! Revisa tu email para confirmar.")
                self.toggle_mode() # Cambiamos a modo login
            else:
                messagebox.showerror("Error", "No se pudo crear la cuenta.")
        except Exception as e:
            messagebox.showerror("Error", f"Error de registro: {e}")