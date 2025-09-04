import customtkinter as ctk
import logging
from src.ui.login_window import LoginWindow
from src.ui.main_window import MainWindow 
from src.services.auth_service import AuthService
from src.database.supabase_client import get_supabase_client

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class App(ctk.CTk):
    def __init__(self, supabase_client, auth_service):
        super().__init__()
        self.supabase_client = supabase_client
        self.auth_service = auth_service
        self.current_frame = None
        self.close_button = None

        self.title("BuildMate - Administrador de Proyectos")
        self.attributes('-fullscreen', True)
        self.configure(fg_color="#33375A") 

        self.bind("<Escape>", self.on_closing)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.check_session()

    def check_session(self):
        try:
            session = self.auth_service.load_session()
            if session:
                self.show_main_window()
            else:
                self.show_login_window()
        except Exception as e:
            logging.error(f"Error al cargar la sesión: {e}")
            self.show_login_window()

    def setup_close_button(self):
        """Configura y muestra el botón de cerrar."""
        if self.close_button: return

        self.close_button = ctk.CTkButton(
            self, text="X", width=30, height=30, corner_radius=15,
            fg_color=("gray75", "#2b2b2b"), hover_color=("gray65", "#3c3c3c"),
            text_color=("#2b2b2b", "white"), font=ctk.CTkFont(weight="bold"),
            command=self.on_closing
        )
        self.close_button.place(relx=0.98, rely=0.03, anchor="ne")

    def _cleanup_login_ui(self):
        """Limpia los widgets de la pantalla de login."""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None
        if self.close_button:
            self.close_button.destroy()
            self.close_button = None

    def show_login_window(self):
        self._cleanup_login_ui()
        self.setup_close_button()
        
        self.current_frame = LoginWindow(self, auth_service=self.auth_service)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")

    def show_main_window(self):
        self._cleanup_login_ui()
        
        self.current_frame = MainWindow(self)
        self.current_frame.pack(fill="both", expand=True)
        
    def on_closing(self, event=None):
        self.destroy()

def main():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
    
    try:
        supabase_client = get_supabase_client()
        auth_service = AuthService(supabase_client)
    except ValueError as e:
        logging.error(f"Error de conexión: {e}")
        return
    
    app = App(supabase_client, auth_service)
    app.mainloop()

if __name__ == "__main__":
    main()

