import tkinter as tk
from tkinter import messagebox
from supabase import Client
from PIL import Image, ImageTk
from pathlib import Path
import json

# Importación de la configuración
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import *

# Definir la ruta del archivo de sesión
SESSION_FILE = Path(__file__).parent.parent / "session.json"

class LoginWindow:
    def __init__(self, master, supabase_client: Client):
        self.master = master
        self.supabase_client = supabase_client
        
        # Configuración ventana
        self.master.configure(bg=INDIGO_DYE)
        self.master.resizable(False, False)
        
        # Variables de estado
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.remember_me_var = tk.BooleanVar()
        self.is_login_mode = True # Modo inicial: login

        # Frame principal
        main_frame = tk.Frame(self.master, bg=WHITE, relief='flat', 
                             highlightbackground=BLUE_MUNSELL, highlightthickness=2)
        main_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=500)
        
        # Sombra
        shadow_frame = tk.Frame(self.master, bg=MEDIUM_GRAY)
        shadow_frame.place(relx=0.5, rely=0.5, anchor='center', width=404, height=504)
        shadow_frame.lower(main_frame)

        # Logo: Se coloca el logo directamente en el main_frame
        image_path = Path(__file__).parent.parent / "assets" / "logoSinMarca.png"
        try:
            img = Image.open(image_path)
            img = img.resize((120, 120), Image.LANCZOS)
            self.logo_image = ImageTk.PhotoImage(img)

            logo_label = tk.Label(main_frame, image=self.logo_image, bg=WHITE)
            logo_label.image = self.logo_image
            logo_label.pack(pady=(20, 0)) # Se usa pack para que se posicione bien arriba
            
        except FileNotFoundError:
            logo_label = tk.Label(main_frame, text="🏗️", font=(FONT_PRIMARY, 48, "normal"), bg=WHITE)
            logo_label.pack(pady=(20, 0))

        # Frames para el formulario de login y registro
        self.login_frame = tk.Frame(main_frame, bg=WHITE)
        self.signup_frame = tk.Frame(main_frame, bg=WHITE)
        
        self.create_login_widgets(self.login_frame)
        self.create_signup_widgets(self.signup_frame)
        
        # Iniciar con el modo login
        self.show_login_mode()
        
        # Comprobar sesión guardada al iniciar
        self.check_saved_session()
        
    def create_login_widgets(self, parent_frame):
        # Email
        email_label = tk.Label(parent_frame, text="Email", font=(FONT_PRIMARY, FONT_SIZE_SMALL, "bold"), fg=INDIGO_DYE, bg=WHITE, anchor='w')
        email_label.pack(fill='x', pady=(0, 5))
        
        email_container = tk.Frame(parent_frame, bg=LIGHT_GRAY, height=40)
        email_container.pack(fill='x', pady=(0, 15))
        email_container.pack_propagate(False)
        
        self.email_entry_login = tk.Entry(email_container, textvariable=self.email_var, **ENTRY_STYLE)
        self.email_entry_login.pack(fill='both', expand=True, padx=12, pady=8)
        
        # Contraseña
        password_label = tk.Label(parent_frame, text="Contraseña", font=(FONT_PRIMARY, FONT_SIZE_SMALL, "bold"), fg=INDIGO_DYE, bg=WHITE, anchor='w')
        password_label.pack(fill='x', pady=(0, 5))
        
        password_container = tk.Frame(parent_frame, bg=LIGHT_GRAY, height=40)
        password_container.pack(fill='x', pady=(0, 15))
        password_container.pack_propagate(False)
        
        self.password_entry_login = tk.Entry(password_container, textvariable=self.password_var, show="•", **ENTRY_STYLE)
        self.password_entry_login.pack(fill='both', expand=True, padx=12, pady=8)

        # Mantener sesión iniciada
        remember_me_check = tk.Checkbutton(parent_frame, text="Mantener sesión iniciada", variable=self.remember_me_var,
                                            bg=WHITE, activebackground=WHITE, fg=DARK_GRAY,
                                            font=(FONT_PRIMARY, FONT_SIZE_SMALL), selectcolor=WHITE)
        remember_me_check.pack(pady=(0, 20))

        # Botón login
        login_btn = tk.Button(parent_frame, text="Iniciar Sesión", command=self.login, **BUTTON_STYLE_PRIMARY)
        login_btn.pack(fill='x', pady=(0, 10))
        
        # Separador para "o" y botón de registro
        separator_frame = tk.Frame(parent_frame, bg=WHITE)
        separator_frame.pack(fill='x', pady=5)
        
        tk.Frame(separator_frame, height=1, bg=MEDIUM_GRAY).place(relx=0, rely=0.5, relwidth=0.4, anchor='w')
        or_label = tk.Label(separator_frame, text="o", bg=WHITE, fg=MEDIUM_GRAY, font=(FONT_PRIMARY, FONT_SIZE_SMALL))
        or_label.place(relx=0.5, rely=0.5, anchor='center')
        tk.Frame(separator_frame, height=1, bg=MEDIUM_GRAY).place(relx=1, rely=0.5, relwidth=0.4, anchor='e')
        
        signup_btn = tk.Button(parent_frame, text="Crear una cuenta", command=self.toggle_mode, **BUTTON_STYLE_SECONDARY)
        signup_btn.pack(fill='x', pady=(5, 0))
        
        # Ligar la tecla Enter
        self.email_entry_login.bind('<Return>', lambda event: self.login())
        self.password_entry_login.bind('<Return>', lambda event: self.login())
        
        # Efectos hover
        login_btn.bind("<Enter>", lambda e: self.on_enter(e, login_btn, INDIGO_DYE, WHITE))
        login_btn.bind("<Leave>", lambda e: self.on_leave(e, login_btn, BLUE_MUNSELL, WHITE))
        signup_btn.bind("<Enter>", lambda e: self.on_enter(e, signup_btn, TEA_ROSE, BLUE_MUNSELL))
        signup_btn.bind("<Leave>", lambda e: self.on_leave(e, signup_btn, WHITE, BLUE_MUNSELL))

    def create_signup_widgets(self, parent_frame):
        # Email
        email_label = tk.Label(parent_frame, text="Email", font=(FONT_PRIMARY, FONT_SIZE_SMALL, "bold"), fg=INDIGO_DYE, bg=WHITE, anchor='w')
        email_label.pack(fill='x', pady=(0, 5))
        
        email_container = tk.Frame(parent_frame, bg=LIGHT_GRAY, height=40)
        email_container.pack(fill='x', pady=(0, 15))
        email_container.pack_propagate(False)
        
        self.email_entry_signup = tk.Entry(email_container, textvariable=self.email_var, **ENTRY_STYLE)
        self.email_entry_signup.pack(fill='both', expand=True, padx=12, pady=8)
        
        # Contraseña
        password_label = tk.Label(parent_frame, text="Contraseña", font=(FONT_PRIMARY, FONT_SIZE_SMALL, "bold"), fg=INDIGO_DYE, bg=WHITE, anchor='w')
        password_label.pack(fill='x', pady=(0, 5))
        
        password_container = tk.Frame(parent_frame, bg=LIGHT_GRAY, height=40)
        password_container.pack(fill='x', pady=(0, 20))
        password_container.pack_propagate(False)
        
        self.password_entry_signup = tk.Entry(password_container, textvariable=self.password_var, show="•", **ENTRY_STYLE)
        self.password_entry_signup.pack(fill='both', expand=True, padx=12, pady=8)

        # Botón de registro
        signup_btn = tk.Button(parent_frame, text="Registrarse", command=self.signup, **BUTTON_STYLE_PRIMARY)
        signup_btn.pack(fill='x', pady=(0, 10))

        # Separador para "o" y botón de login
        separator_frame = tk.Frame(parent_frame, bg=WHITE)
        separator_frame.pack(fill='x', pady=5)
        
        tk.Frame(separator_frame, height=1, bg=MEDIUM_GRAY).place(relx=0, rely=0.5, relwidth=0.4, anchor='w')
        or_label = tk.Label(separator_frame, text="o", bg=WHITE, fg=MEDIUM_GRAY, font=(FONT_PRIMARY, FONT_SIZE_SMALL))
        or_label.place(relx=0.5, rely=0.5, anchor='center')
        tk.Frame(separator_frame, height=1, bg=MEDIUM_GRAY).place(relx=1, rely=0.5, relwidth=0.4, anchor='e')
        
        login_btn = tk.Button(parent_frame, text="Ya tengo una cuenta", command=self.toggle_mode, **BUTTON_STYLE_SECONDARY)
        login_btn.pack(fill='x', pady=(5, 0))
        
        # Ligar la tecla Enter
        self.email_entry_signup.bind('<Return>', lambda event: self.signup())
        self.password_entry_signup.bind('<Return>', lambda event: self.signup())
        
        # Efectos hover
        signup_btn.bind("<Enter>", lambda e: self.on_enter(e, signup_btn, INDIGO_DYE, WHITE))
        signup_btn.bind("<Leave>", lambda e: self.on_leave(e, signup_btn, BLUE_MUNSELL, WHITE))
        login_btn.bind("<Enter>", lambda e: self.on_enter(e, login_btn, TEA_ROSE, BLUE_MUNSELL))
        login_btn.bind("<Leave>", lambda e: self.on_leave(e, login_btn, WHITE, BLUE_MUNSELL))

    def show_login_mode(self):
        self.is_login_mode = True
        self.signup_frame.pack_forget()
        self.login_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.master.title("Iniciar Sesión")
        self.email_entry_login.focus_set()
    
    def show_signup_mode(self):
        self.is_login_mode = False
        self.login_frame.pack_forget()
        self.signup_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.master.title("Registrarse")
        self.email_entry_signup.focus_set()

    def toggle_mode(self):
        if self.is_login_mode:
            self.show_signup_mode()
        else:
            self.show_login_mode()

    def check_saved_session(self):
        """Intenta cargar la sesión guardada y autenticar con el token."""
        if SESSION_FILE.exists():
            try:
                with open(SESSION_FILE, 'r') as f:
                    session_data = json.load(f)
                    access_token = session_data.get("access_token")
                    
                    if access_token:
                        # Si hay un token, intenta autenticar
                        self.supabase_client.auth.session = access_token
                        messagebox.showinfo("Sesión", "¡Sesión iniciada automáticamente!")
                        # Aquí puedes llamar a una función para abrir la ventana principal de la app
                        self.master.destroy() 
            except (IOError, json.JSONDecodeError) as e:
                print(f"Error al leer el archivo de sesión: {e}")

    def save_session(self, token):
        """Guarda el token de sesión en un archivo local."""
        if self.remember_me_var.get():
            session_data = {"access_token": token}
            try:
                with open(SESSION_FILE, 'w') as f:
                    json.dump(session_data, f)
            except IOError as e:
                print(f"Error al guardar el archivo de sesión: {e}")

    def on_enter(self, e, button, bg, fg):
        button.config(background=bg, foreground=fg)
            
    def on_leave(self, e, button, bg, fg):
        button.config(background=bg, foreground=fg)

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
                    self.save_session(auth_response.session.access_token)
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