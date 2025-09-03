# src/ui/login_window.py (Corregido)

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from pathlib import Path
import logging

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.auth_service = master.auth_service
        self.is_login_mode = True

        self.email_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.remember_me_var = ctk.BooleanVar()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        main_frame = ctk.CTkFrame(self, width=400, height=550)
        main_frame.grid(row=0, column=0, sticky="ns")
        main_frame.grid_propagate(False)

        # --- Logo ---
        try:
            # --- CORRECCIÓN DE RUTA ---
            # parents[1] apunta a la carpeta 'src'
            base_path = Path(__file__).resolve().parents[1] 
            logo_path = base_path / "assets" / "logo.png"
            
            self.logo_image = ctk.CTkImage(Image.open(logo_path), size=(150, 150))
            logo_label = ctk.CTkLabel(main_frame, image=self.logo_image, text="")
            logo_label.pack(pady=(50, 10))
        except Exception as e:
            logging.error(f"No se pudo cargar el logo: {e}")

        # --- El resto del archivo no cambia ---
        self.title_label = ctk.CTkLabel(main_frame, text="Iniciar Sesión", font=ctk.CTkFont(size=24, weight="bold"))
        self.title_label.pack(pady=(0, 10))
        self.subtitle_label = ctk.CTkLabel(main_frame, text="Bienvenido de nuevo.", text_color="gray")
        self.subtitle_label.pack(pady=(0, 20))
        self.email_entry = ctk.CTkEntry(main_frame, textvariable=self.email_var, placeholder_text="Email", width=280, height=40)
        self.email_entry.pack(pady=(0, 10))
        self.password_entry = ctk.CTkEntry(main_frame, textvariable=self.password_var, placeholder_text="Contraseña", show="*", width=280, height=40)
        self.password_entry.pack(pady=(0, 20))
        self.remember_me_check = ctk.CTkCheckBox(main_frame, text="Recordar sesión", variable=self.remember_me_var)
        self.remember_me_check.pack(padx=60, anchor="w")
        self.action_btn = ctk.CTkButton(main_frame, text="Iniciar Sesión", command=self.login, height=40, font=ctk.CTkFont(weight="bold"))
        self.action_btn.pack(fill="x", padx=60, pady=(15, 10))
        self.toggle_btn = ctk.CTkButton(main_frame, text="¿No tienes cuenta? Regístrate aquí.", command=self.toggle_mode, fg_color="transparent", hover=False)
        self.toggle_btn.pack(fill="x", padx=60)

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
            self.title_label.configure(text="Iniciar Sesión")
            self.subtitle_label.configure(text="Bienvenido de nuevo.")
            self.action_btn.configure(text="Iniciar Sesión", command=self.login)
            self.toggle_btn.configure(text="¿No tienes cuenta? Regístrate aquí.")
        else:
            self.title_label.configure(text="Registrarse")
            self.subtitle_label.configure(text="Crea tu cuenta.")
            self.action_btn.configure(text="Registrarse", command=self.signup)
            self.toggle_btn.configure(text="¿Ya tienes cuenta? Inicia sesión aquí.")