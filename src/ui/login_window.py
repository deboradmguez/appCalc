import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from pathlib import Path
import logging
import threading

class LoginWindow:
    """Ventana de login mejorada usando CustomTkinter."""
    
    def __init__(self, master, supabase_client, auth_service, app_state):
        self.master = master
        self.supabase_client = supabase_client
        self.auth_service = auth_service
        self.app_state = app_state
        self.is_login_mode = True

        # Configurar la ventana principal como ventana de login
        self.master.title("Iniciar Sesión - Administrador de Proyectos")
        self.master.geometry("500x700")
        self.master.resizable(False, False)
        
        # Centrar la ventana
        self.center_window()
        
        # Variables
        self.email_var = ctk.StringVar()
        self.password_var = ctk.StringVar()
        self.remember_me_var = ctk.BooleanVar()

        # Crear la interfaz
        self.create_ui()
        
        # Configurar el protocolo de cierre
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def center_window(self):
        """Centra la ventana en la pantalla."""
        self.master.update_idletasks()
        width = 500
        height = 700
        x = (self.master.winfo_screenwidth() // 2) - (width // 2)
        y = (self.master.winfo_screenheight() // 2) - (height // 2)
        self.master.geometry(f"{width}x{height}+{x}+{y}")

    def create_ui(self):
        """Crea la interfaz de usuario."""
        # Frame principal con padding
        main_frame = ctk.CTkFrame(self.master, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=40, pady=40)
        
        # Logo/Imagen
        self.add_logo(main_frame)
        
        # Título y subtítulo
        self.title_label = ctk.CTkLabel(
            main_frame, 
            text="Iniciar Sesión", 
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.title_label.pack(pady=(20, 5))

        self.subtitle_label = ctk.CTkLabel(
            main_frame, 
            text="Bienvenido de nuevo", 
            font=ctk.CTkFont(size=16),
            text_color=("gray40", "gray60")
        )
        self.subtitle_label.pack(pady=(0, 30))
        
        # Campos de entrada
        self.create_form_fields(main_frame)
        
        # Botones
        self.create_buttons(main_frame)

    def add_logo(self, parent):
        """Agrega el logo si existe."""
        try:
            logo_path = Path(__file__).parent.parent / "assets" / "logo.png"
            if logo_path.exists():
                logo_image = ctk.CTkImage(
                    Image.open(logo_path), 
                    size=(120, 120)
                )
                logo_label = ctk.CTkLabel(parent, image=logo_image, text="")
                logo_label.pack(pady=(10, 0))
            else:
                # Logo placeholder si no existe el archivo
                logo_placeholder = ctk.CTkLabel(
                    parent,
                    text="📊",
                    font=ctk.CTkFont(size=48)
                )
                logo_placeholder.pack(pady=(10, 0))
        except Exception as e:
            logging.warning(f"No se pudo cargar el logo: {e}")

    def create_form_fields(self, parent):
        """Crea los campos del formulario."""
        # Campo email
        self.email_entry = ctk.CTkEntry(
            parent,
            textvariable=self.email_var,
            placeholder_text="📧 Correo electrónico",
            height=50,
            font=ctk.CTkFont(size=14)
        )
        self.email_entry.pack(fill="x", pady=(0, 15))
        
        # Campo contraseña
        self.password_entry = ctk.CTkEntry(
            parent,
            textvariable=self.password_var,
            placeholder_text="🔒 Contraseña",
            show="*",
            height=50,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.pack(fill="x", pady=(0, 20))

        # Checkbox recordar sesión
        self.remember_me_check = ctk.CTkCheckBox(
            parent,
            text="Recordar mi sesión",
            variable=self.remember_me_var,
            font=ctk.CTkFont(size=12)
        )
        self.remember_me_check.pack(pady=(0, 20))

    def create_buttons(self, parent):
        """Crea los botones de acción."""
        # Botón principal de acción
        self.action_btn = ctk.CTkButton(
            parent,
            text="Iniciar Sesión",
            command=self.handle_action,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.action_btn.pack(fill="x", pady=(0, 15))
        
        # Botón para alternar modo
        self.toggle_btn = ctk.CTkButton(
            parent,
            text="¿No tienes cuenta? Regístrate aquí",
            command=self.toggle_mode,
            fg_color="transparent",
            text_color=("gray40", "gray60"),
            hover_color=("gray90", "gray20"),
            font=ctk.CTkFont(size=12)
        )
        self.toggle_btn.pack(fill="x")

        # Eventos de teclado
        self.master.bind('<Return>', lambda e: self.handle_action())
        self.email_entry.bind('<Return>', lambda e: self.password_entry.focus())

    def toggle_mode(self):
        """Alterna entre modo login y registro."""
        self.is_login_mode = not self.is_login_mode
        
        if self.is_login_mode:
            self.title_label.configure(text="Iniciar Sesión")
            self.subtitle_label.configure(text="Bienvenido de nuevo")
            self.action_btn.configure(text="Iniciar Sesión")
            self.toggle_btn.configure(text="¿No tienes cuenta? Regístrate aquí")
            self.remember_me_check.pack(pady=(0, 20))
        else:
            self.title_label.configure(text="Crear Cuenta")
            self.subtitle_label.configure(text="Únete a nosotros")
            self.action_btn.configure(text="Crear Cuenta")
            self.toggle_btn.configure(text="¿Ya tienes cuenta? Inicia sesión aquí")
            self.remember_me_check.pack_forget()

    def handle_action(self):
        """Maneja la acción principal (login o registro)."""
        if self.is_login_mode:
            self.login()
        else:
            self.signup()

    def login(self):
        """Maneja el proceso de login."""
        email = self.email_var.get().strip()
        password = self.password_var.get()

        # Validación básica
        if not email or not password:
            messagebox.showerror(
                "Error", 
                "Por favor, ingresa tu email y contraseña.",
                parent=self.master
            )
            return

        # Validar formato de email básico
        if "@" not in email or "." not in email:
            messagebox.showerror(
                "Error", 
                "Por favor, ingresa un email válido.",
                parent=self.master
            )
            return

        # Deshabilitar botón durante el proceso
        self.action_btn.configure(state="disabled", text="Iniciando sesión...")
        
        # Ejecutar login en un hilo separado para no bloquear la UI
        def login_thread():
            try:
                auth_response = self.auth_service.login(email, password)
                
                # Volver al hilo principal para actualizar la UI
                self.master.after(0, lambda: self.on_login_success(auth_response))
                
            except Exception as e:
                self.master.after(0, lambda: self.on_login_error(str(e)))
        
        threading.Thread(target=login_thread, daemon=True).start()

    def on_login_success(self, auth_response):
        """Callback ejecutado cuando el login es exitoso."""
        self.action_btn.configure(state="normal", text="Iniciar Sesión")
        
        if auth_response and auth_response.session:
            # Guardar sesión si se solicitó
            if self.remember_me_var.get():
                self.auth_service.save_session(auth_response.session.refresh_token)
            
            messagebox.showinfo(
                "Éxito", 
                "¡Inicio de sesión exitoso!",
                parent=self.master
            )
            
            # Cerrar ventana de login para que main.py cargue la ventana principal
            self.master.quit()
        else:
            messagebox.showerror(
                "Error", 
                "No se pudo completar el inicio de sesión.",
                parent=self.master
            )

    def on_login_error(self, error_message):
        """Callback ejecutado cuando hay un error en el login."""
        self.action_btn.configure(state="normal", text="Iniciar Sesión")
        
        # Mensajes de error más amigables
        if "invalid" in error_message.lower() or "credentials" in error_message.lower():
            error_msg = "Email o contraseña incorrectos."
        elif "network" in error_message.lower() or "connection" in error_message.lower():
            error_msg = "Error de conexión. Verifica tu internet."
        else:
            error_msg = "Error al iniciar sesión. Inténtalo de nuevo."
        
        messagebox.showerror("Error", error_msg, parent=self.master)

    def signup(self):
        """Maneja el proceso de registro."""
        email = self.email_var.get().strip()
        password = self.password_var.get()

        # Validación básica
        if not email or not password:
            messagebox.showerror(
                "Error", 
                "Por favor, ingresa un email y contraseña.",
                parent=self.master
            )
            return

        if len(password) < 6:
            messagebox.showerror(
                "Error", 
                "La contraseña debe tener al menos 6 caracteres.",
                parent=self.master
            )
            return

        # Deshabilitar botón durante el proceso
        self.action_btn.configure(state="disabled", text="Creando cuenta...")
        
        def signup_thread():
            try:
                auth_response = self.auth_service.signup(email, password)
                self.master.after(0, lambda: self.on_signup_success(auth_response))
            except Exception as e:
                self.master.after(0, lambda: self.on_signup_error(str(e)))
        
        threading.Thread(target=signup_thread, daemon=True).start()

    def on_signup_success(self, auth_response):
        """Callback ejecutado cuando el registro es exitoso."""
        self.action_btn.configure(state="normal", text="Crear Cuenta")
        
        messagebox.showinfo(
            "Registro Exitoso", 
            "¡Cuenta creada exitosamente!\n\nRevisa tu email para confirmar tu cuenta.",
            parent=self.master
        )
        
        # Cambiar a modo login
        self.toggle_mode()

    def on_signup_error(self, error_message):
        """Callback ejecutado cuando hay un error en el registro."""
        self.action_btn.configure(state="normal", text="Crear Cuenta")
        
        if "already" in error_message.lower():
            error_msg = "Este email ya está registrado."
        else:
            error_msg = f"Error al crear la cuenta: {error_message}"
        
        messagebox.showerror("Error", error_msg, parent=self.master)

    def on_closing(self):
        """Maneja el cierre de la ventana."""
        self.app_state['is_closing'] = True
        self.master.quit()