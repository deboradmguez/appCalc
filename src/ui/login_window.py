import tkinter as tk
from tkinter import messagebox
from supabase import Client
from PIL import Image, ImageTk
from pathlib import Path
import logging

# Importación de la configuración
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import *

class LoginWindow:
    def __init__(self, master, supabase_client: Client, auth_service, app_state):
        self.master = master
        self.supabase_client = supabase_client
        self.auth_service = auth_service
        self.app_state = app_state
        
        # Conectamos el cierre de la ventana con nuestra función
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configuración ventana
        self.master.configure(bg=INDIGO_DYE)
        self.master.resizable(False, False)
        
        # Variables de estado
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_me_var = tk.BooleanVar()
        self.is_login_mode = True # Modo inicial: login

        # Frame principal
        # Usamos pack para un diseño más robusto y predecible
        main_frame = tk.Frame(self.master, bg=WHITE, relief='flat', 
                             highlightbackground=BLUE_MUNSELL, highlightthickness=2)
        main_frame.pack(padx=50, pady=50, fill=tk.BOTH, expand=True)

        # Usamos un frame interno para centrar los elementos
        content_frame = tk.Frame(main_frame, bg=WHITE)
        content_frame.pack(pady=20)
        
        # Cargar logo
        try:
            logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
            self.logo_img = Image.open(logo_path)
            self.logo_img = self.logo_img.resize((150, 150))
            self.logo_photo = ImageTk.PhotoImage(self.logo_img)
            
            logo_label = tk.Label(content_frame, image=self.logo_photo, bg=WHITE)
            logo_label.pack(pady=(20, 10))
        except FileNotFoundError:
            logging.error("No se encontró el archivo de logo. Asegúrate de que assets/logo.png existe.")
            
        # Título
        self.title_label = tk.Label(content_frame, text="Iniciar Sesión", font=(FONT_PRIMARY, FONT_SIZE_TITLE, "bold"), fg=INDIGO_DYE, bg=WHITE)
        self.title_label.pack(pady=(0, 10))

        # Subtítulo
        self.subtitle_label = tk.Label(content_frame, text="Bienvenido de nuevo.", font=(FONT_PRIMARY, FONT_SIZE_SUBTITLE), fg=DARK_GRAY, bg=WHITE)
        self.subtitle_label.pack(pady=(0, 20))

        # Campos de entrada
        self.email_entry = tk.Entry(content_frame, textvariable=self.email_var, **ENTRY_STYLE)
        self.email_entry.pack(fill=tk.X, padx=30, pady=(0, 10))
        self.email_entry.insert(0, "Email")
        self.email_entry.bind("<FocusIn>", self.on_entry_focus)
        self.email_entry.bind("<FocusOut>", self.on_entry_unfocus)
        
        self.password_entry = tk.Entry(content_frame, textvariable=self.password_var, show="", **ENTRY_STYLE)
        self.password_entry.pack(fill=tk.X, padx=30, pady=(0, 20))
        self.password_entry.insert(0, "Contraseña")
        self.password_entry.bind("<FocusIn>", self.on_entry_focus)
        self.password_entry.bind("<FocusOut>", self.on_entry_unfocus)

        # Botones
        self.login_btn = tk.Button(content_frame, text="Iniciar Sesión", command=self.login, **BUTTON_STYLE_PRIMARY)
        self.login_btn.pack(fill=tk.X, padx=30)
        
        self.toggle_btn = tk.Button(content_frame, text="¿No tienes cuenta? Regístrate aquí.", command=self.toggle_mode, **BUTTON_STYLE_SECONDARY)
        self.toggle_btn.pack(pady=(10, 0))

        # Checkbox "Recordar sesión"
        self.remember_me_check = tk.Checkbutton(content_frame, text="Recordar sesión", variable=self.remember_me_var,
                                               bg=WHITE, fg=DARK_GRAY, selectcolor=WHITE,
                                               font=(FONT_PRIMARY, FONT_SIZE_SMALL))
        self.remember_me_check.pack(pady=10)

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
                self.show_login_mode()
            else:
                messagebox.showerror("Error", "No se pudo crear la cuenta.")
        except Exception as e:
            messagebox.showerror("Error", f"Error de registro: {e}")

    def show_login_mode(self):
        self.is_login_mode = True
        self.toggle_mode()
