# src/ui/login_window.py

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import logging
from pathlib import Path
# CORREGIDO: Importamos TRANSPARENT_HOVER para usarlo en el botón.
from config import TRANSPARENT_BG, TRANSPARENT_HOVER, get_login_colors
    
colors = get_login_colors()

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, auth_service, **kwargs):
        super().__init__(
            master, 
            width=420,
            height=580, 
            corner_radius=20,
            fg_color=colors['frame_bg'],
            border_width=2,
            border_color=colors['frame_border'],
            **kwargs
        )
        
        self.auth_service = auth_service
        self.master = master 
        self.is_login_mode = True
        self.colors = colors

        self.email_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.remember_me_var = ctk.BooleanVar()

        self.grid_columnconfigure(0, weight=1)
        
        try:
            possible_paths = [
                Path(__file__).resolve().parents[2] / "assets" / "logoNuevo.png",
                Path(__file__).resolve().parents[1] / "assets" / "logoNuevo.png",
                Path("assets") / "logoNuevo.png",
            ]
            
            logo_path = None
            for path in possible_paths:
                if path.exists():
                    logo_path = path
                    break
            
            if logo_path:
                avatar_image = ctk.CTkImage(Image.open(logo_path), size=(120, 100))
                avatar_label = ctk.CTkLabel(
                    self, 
                    image=avatar_image, 
                    text=""
                )
                avatar_label.grid(row=0, column=0, pady=(25, 10))
            else:
                raise FileNotFoundError("Logo no encontrado")
                
        except Exception as e:
            logging.warning(f"No se pudo cargar el logo: {e}. Usando placeholder.")
            placeholder_avatar = ctk.CTkLabel(
                self, 
                text="🏗️", 
                font=ctk.CTkFont(size=80)
            )
            placeholder_avatar.grid(row=0, column=0, pady=(30, 15))
        
        welcome_label = ctk.CTkLabel(
            self, 
            text="¡Bienvenido a BuildMate!", 
            font=ctk.CTkFont(size=18, weight="bold"), 
            text_color=colors['text_primary']
        )
        welcome_label.grid(row=1, column=0, pady=(0, 5))

        subtitle_label = ctk.CTkLabel(
            self, 
            text="Inicia sesión para gestionar tus proyectos", 
            font=ctk.CTkFont(size=12), 
            text_color=colors['text_secondary']
        )
        subtitle_label.grid(row=2, column=0, pady=(0, 10))

        separator_bar = ctk.CTkFrame(
            self, 
            height=2, 
            fg_color=colors['accent_text'],
        )
        separator_bar.grid(row=3, column=0, padx=40, pady=(5, 20), sticky="ew")

        try:
            possible_icon_paths = [
                Path(__file__).resolve().parents[2] / "assets" / "icons",
                Path(__file__).resolve().parents[1] / "assets" / "icons",
                Path("assets") / "icons",
            ]
            
            icon_path = None
            for path in possible_icon_paths:
                if path.exists():
                    icon_path = path
                    break
            
            if icon_path:
                eye_open_path = icon_path / "eye_open.ico"
                eye_closed_path = icon_path / "eye_closed.ico"
                
                self.eye_open_icon = ctk.CTkImage(Image.open(eye_open_path), size=(18, 18))
                self.eye_closed_icon = ctk.CTkImage(Image.open(eye_closed_path), size=(18, 18))
            else:
                raise FileNotFoundError("Iconos no encontrados")
                
        except Exception as e:
            logging.warning(f"No se pudieron cargar los iconos: {e}")
            self.eye_open_icon = None
            self.eye_closed_icon = None

        self._create_form_fields()
        self._bind_focus_events()

    def _create_form_fields(self):
        """Crea los campos del formulario"""
        
        self.email_label = ctk.CTkLabel(
            self, 
            text="Correo electrónico", 
            anchor="w",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors['text_primary']
        )
        self.email_label.grid(row=4, column=0, padx=40, pady=(0, 5), sticky="w")
        
        self.email_entry = ctk.CTkEntry(
            self, 
            textvariable=self.email_var,
            height=45, 
            corner_radius=12,
            border_width=2,
            border_color=self.colors['input_border'],
            fg_color=TRANSPARENT_BG ,
            placeholder_text="ejemplo@correo.com",
            font=ctk.CTkFont(size=14)
        )
        self.email_entry.grid(row=5, column=0, padx=40, pady=(0, 15), sticky="ew")
        
        self.password_label = ctk.CTkLabel(
            self, 
            text="Contraseña", 
            anchor="w",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=self.colors['text_primary']
        )
        self.password_label.grid(row=6, column=0, padx=40, pady=(0, 5), sticky="w")

        password_container = ctk.CTkFrame(
            self,
            height=45,
            corner_radius=12, 
            border_width=2, 
            border_color=self.colors['input_border'],
            fg_color=TRANSPARENT_BG 
        )
        password_container.grid(row=7, column=0, padx=40, pady=(0, 20), sticky="ew")
        password_container.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(
            password_container, 
            textvariable=self.password_var,
            show="*", 
            corner_radius=0,
            border_width=0,
            fg_color=TRANSPARENT_BG ,
            placeholder_text="Ingresa tu contraseña",
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.grid(row=0, column=0, sticky="ew", padx=(15, 0), pady=5)

        if self.eye_closed_icon:
            self.show_password_btn = ctk.CTkButton(
                password_container,
                image=self.eye_closed_icon, 
                text="",
                width=30,
                height=30,
                command=self.toggle_password_visibility,
                fg_color=TRANSPARENT_BG ,
                hover_color=self.colors['input_border']
            )
            self.show_password_btn.grid(row=0, column=1, padx=(0, 10), pady=5)

        options_frame = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG )
        options_frame.grid(row=8, column=0, padx=40, pady=(0, 20), sticky="ew")
        options_frame.grid_columnconfigure(0, weight=1)
        
        self.remember_me_check = ctk.CTkCheckBox(
            options_frame, 
            text="Recordar sesión", 
            variable=self.remember_me_var, 
            border_color=self.colors['accent_text'],
            checkmark_color=self.colors['button_bg'],
            font=ctk.CTkFont(size=12),
            text_color=self.colors['text_secondary']
        )
        self.remember_me_check.grid(row=0, column=0, sticky="w")
        
        self.action_btn = ctk.CTkButton(
            self, 
            text="Iniciar Sesión", 
            command=self.login, 
            height=50, 
            corner_radius=12, 
            font=ctk.CTkFont(weight="bold", size=16),
            fg_color=self.colors['button_bg'],
            hover_color=self.colors['button_hover'],
            text_color="#FFFFFF"
        )
        self.action_btn.grid(row=9, column=0, padx=40, pady=(0, 15), sticky="ew")

        self.toggle_btn = ctk.CTkButton(
            self, 
            text="¿No tienes cuenta? Regístrate aquí.", 
            command=self.toggle_mode, 
            fg_color=TRANSPARENT_BG , 
            # CORREGIDO: Usamos TRANSPARENT_HOVER en lugar de TRANSPARENT_BG.
            hover_color=TRANSPARENT_HOVER,
            text_color=self.colors['accent_text'],
            font=ctk.CTkFont(underline=True, size=12)
        )
        self.toggle_btn.grid(row=10, column=0, padx=40, pady=(0, 25), sticky="ew")

    def _bind_focus_events(self):
        """Vincula eventos de foco para mejorar UX"""
        self.email_entry.bind("<FocusIn>", lambda e: self.email_entry.configure(border_color=self.colors['input_focus_border']))
        self.email_entry.bind("<FocusOut>", lambda e: self.email_entry.configure(border_color=self.colors['input_border']))
        
        self.email_entry.bind("<Return>", lambda e: self.password_entry.focus())
        self.password_entry.bind("<Return>", lambda e: self.login())

    def toggle_password_visibility(self):
        """Alterna la visibilidad de la contraseña"""
        if not hasattr(self, 'show_password_btn'):
            return
            
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
        """Maneja el proceso de login"""
        email = self.email_var.get().strip()
        password = self.password_var.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Por favor, ingresa tu email y contraseña.")
            return
            
        self.action_btn.configure(state="disabled", text="Iniciando...")
        
        try:
            auth_response = self.auth_service.login(email, password)
            if auth_response:
                if self.remember_me_var.get():
                    self.auth_service.save_session(auth_response.session.refresh_token)
                
                app_window = self.master
                while hasattr(app_window, 'master') and app_window.master:
                    app_window = app_window.master
                
                app_window.show_main_window()
                
        except Exception as e:
            messagebox.showerror("Error", f"Credenciales incorrectas o error de conexión: {e}")
        finally:
            self.action_btn.configure(state="normal", text="Iniciar Sesión")

    def signup(self):
        """Maneja el proceso de registro"""
        email = self.email_var.get().strip()
        password = self.password_var.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Por favor, ingresa un email y contraseña.")
            return
            
        if len(password) < 6:
            messagebox.showerror("Error", "La contraseña debe tener al menos 6 caracteres.")
            return
        
        self.action_btn.configure(state="disabled", text="Registrando...")
        
        try:
            self.auth_service.signup(email, password)
            messagebox.showinfo("Registro Exitoso", "¡Cuenta creada! Revisa tu email para confirmar.")
            self.toggle_mode()
        except Exception as e:
            messagebox.showerror("Error", f"Error de registro: {e}")
        finally:
            self.action_btn.configure(state="normal")
            
    def toggle_mode(self):
        """Alterna entre modo login y registro"""
        self.is_login_mode = not self.is_login_mode
        if self.is_login_mode:
            self.action_btn.configure(text="Iniciar Sesión", command=self.login)
            self.toggle_btn.configure(text="¿No tienes cuenta? Regístrate aquí.")
        else:
            self.action_btn.configure(text="Registrarse", command=self.signup)
            self.toggle_btn.configure(text="¿Ya tienes cuenta? Inicia sesión aquí.")