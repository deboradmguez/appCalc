import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import logging
from pathlib import Path

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, auth_service, **kwargs):
        # --- APLICAMOS EL ESTILO DEL FRAME "GLASSMORPHISM" ---
        super().__init__(
            master, 
            width=360, 
            height=550, 
            corner_radius=15, 
            fg_color="#202342", 
            border_width=1, 
            border_color="#555",
            **kwargs
        )
        
        self.auth_service = auth_service
        self.master = master 
        self.is_login_mode = True

        self.email_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.remember_me_var = ctk.BooleanVar()

        # Usamos grid para una mejor organización
        self.grid_columnconfigure(0, weight=1)
        
        # --- AVATAR / LOGO ---
        try:
            base_path = Path(__file__).resolve().parents[1] 
            logo_path = base_path / "assets" / "logo.png"

            if logo_path.exists():
                avatar_image = ctk.CTkImage(Image.open(logo_path), size=(100, 100))
                avatar_label = ctk.CTkLabel(self, image=avatar_image, text="", bg_color="transparent")
                avatar_label.grid(row=0, column=0, pady=(30, 15))
            else:
                raise FileNotFoundError(f"No se encontró el logo en: {logo_path}")
        except Exception as e:
            logging.warning(f"No se pudo cargar el avatar/logo: {e}. Usando placeholder.")
            placeholder_avatar = ctk.CTkLabel(self, text="👤", font=ctk.CTkFont(size=80), bg_color="transparent")
            placeholder_avatar.grid(row=0, column=0, pady=(30, 15))
        
        # --- CARGAMOS LOS ICONOS DEL OJO DESDE ARCHIVOS ICO ---
        try:
            base_path = Path(__file__).resolve().parents[1]
            eye_open_path = base_path / "assets" / "icons" / "eye_open.ico"
            eye_closed_path = base_path / "assets" / "icons" / "eye_closed.ico"
            
            self.eye_open_icon = ctk.CTkImage(Image.open(eye_open_path), size=(20, 20))
            self.eye_closed_icon = ctk.CTkImage(Image.open(eye_closed_path), size=(20, 20))
        except FileNotFoundError as e:
            logging.error(f"Error: No se encontró el archivo de icono: {e}")
            self.eye_open_icon = None
            self.eye_closed_icon = None

        # --- WIDGETS CON ESTILO MODERNO ---
        
        # Etiqueta para el email
        self.email_label = ctk.CTkLabel(self, text="Email", anchor="w")
        self.email_label.grid(row=1, column=0, padx=30, pady=(15, 0), sticky="w")
        
        self.email_entry = ctk.CTkEntry(
            self, 
            textvariable=self.email_var,
            height=35, 
            corner_radius=10,
            border_width=1,
            border_color="#555",
            fg_color="transparent"
        )
        self.email_entry.grid(row=2, column=0, padx=30, pady=(0, 5), sticky="ew")
        
        # Etiqueta para la contraseña
        self.password_label = ctk.CTkLabel(self, text="Contraseña", anchor="w")
        self.password_label.grid(row=3, column=0, padx=30, pady=(5, 0), sticky="w")

        # Contenedor para la entrada de contraseña y el botón del "ojo"
        password_container = ctk.CTkFrame(self, fg_color="transparent")
        password_container.grid(row=4, column=0, padx=30, pady=(0, 10), sticky="ew")
        password_container.grid_columnconfigure(0, weight=1)
        password_container.grid_columnconfigure(1, weight=0)

        self.password_entry = ctk.CTkEntry(
            password_container, 
            textvariable=self.password_var,
            show="*", 
            height=35, 
            corner_radius=10,
            border_width=1,
            border_color="#555",
            fg_color="transparent"
        )
        self.password_entry.grid(row=0, column=0, sticky="ew")

        self.show_password_btn = ctk.CTkButton(
            password_container, 
            image=self.eye_closed_icon, 
            text="",
            width=35,
            height=35,
            command=self.toggle_password_visibility,
            fg_color="transparent",
            hover_color="#333333"
        )
        self.show_password_btn.grid(row=0, column=1, padx=(5, 0))

        options_frame = ctk.CTkFrame(self, fg_color="transparent")
        options_frame.grid(row=5, column=0, padx=30, pady=5, sticky="ew")
        options_frame.grid_columnconfigure(0, weight=1)
        
        self.remember_me_check = ctk.CTkCheckBox(options_frame, text="Recordar sesión", variable=self.remember_me_var, border_color="#555")
        self.remember_me_check.grid(row=0, column=0, sticky="w")
        
        self.action_btn = ctk.CTkButton(
            self, 
            text="Iniciar Sesión", 
            command=self.login, 
            height=40, 
            corner_radius=10, 
            font=ctk.CTkFont(weight="bold", size=14),
            fg_color="#1DB954",
            hover_color="#39FF7B"
        )
        self.action_btn.grid(row=6, column=0, padx=30, pady=(20, 10), sticky="ew")

        self.toggle_btn = ctk.CTkButton(
            self, 
            text="¿No tienes cuenta? Regístrate aquí.", 
            command=self.toggle_mode, 
            fg_color="transparent", 
            hover=False,
            text_color=("#1DB954", "#39FF7B"),
            font=ctk.CTkFont(underline=True)
        )
        self.toggle_btn.grid(row=7, column=0, padx=30, pady=(10, 20), sticky="ew") 

    def toggle_password_visibility(self):
        current_show_char = self.password_entry.cget("show")
        if current_show_char == "*":
            self.password_entry.configure(show="")
            if self.eye_open_icon:
                self.show_password_btn.configure(image=self.eye_open_icon)
        else:
            self.password_entry.configure(show="*")
            if self.eye_closed_icon:
                self.show_password_btn.configure(image=self.eye_closed_icon)

    def login(self):
        email = self.email_var.get().strip()
        password = self.password_var.get()
        if not email or not password:
            messagebox.showerror("Error", "Por favor, ingresa tu email y contraseña.")
            return
        try:
            auth_response = self.auth_service.login(email, password)
            if auth_response:
                if self.remember_me_var.get():
                    self.auth_service.save_session(auth_response.session.refresh_token)
                self.master.show_main_window()
        except Exception as e:
            messagebox.showerror("Error", f"Credenciales incorrectas o error de conexión: {e}")

    def signup(self):
        email = self.email_var.get().strip()
        password = self.password_var.get()
        if not email or not password:
            messagebox.showerror("Error", "Por favor, ingresa un email y contraseña.")
            return
        try:
            self.auth_service.signup(email, password)
            messagebox.showinfo("Registro Exitoso", "¡Cuenta creada! Revisa tu email para confirmar.")
            self.toggle_mode()
        except Exception as e:
            messagebox.showerror("Error", f"Error de registro: {e}")
            
    def toggle_mode(self):
        self.is_login_mode = not self.is_login_mode
        if self.is_login_mode:
            self.action_btn.configure(text="Iniciar Sesión", command=self.login)
            self.toggle_btn.configure(text="¿No tienes cuenta? Regístrate aquí.")
        else:
            self.action_btn.configure(text="Registrarse", command=self.signup)
            self.toggle_btn.configure(text="¿Ya tienes cuenta? Inicia sesión aquí.")