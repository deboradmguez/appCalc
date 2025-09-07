import customtkinter as ctk
import logging
from src.ui.login_window import LoginWindow
from src.ui.main_window import MainWindow 
from src.services.auth_service import AuthService
from src.database.supabase_client import get_supabase_client
from config import BACKGROUND_PRIMARY, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT, START_MAXIMIZED, TRANSPARENT_BG

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class App(ctk.CTk):
    def __init__(self, supabase_client, auth_service):
        super().__init__()
        self.supabase_client = supabase_client
        self.auth_service = auth_service
        self.current_frame = None

        # === CONFIGURACIÓN DE VENTANA MEJORADA ===
        self.title("BuildMate - Administrador de Proyectos de Construcción")
        
        # Aplicar el nuevo color de fondo
        self.configure(fg_color=BACKGROUND_PRIMARY)
        
        # Configurar tamaño mínimo
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        
        # === CAMBIO DE PANTALLA COMPLETA A MAXIMIZADA ===
        if START_MAXIMIZED:
            # Maximizar la ventana manteniendo la barra de título y controles
            self.state('zoomed')  # Para Windows
            # Para Linux/Mac usar: self.attributes('-zoomed', True)
        else:
            # Tamaño normal centrado
            self.geometry(f"{WINDOW_MIN_WIDTH}x{WINDOW_MIN_HEIGHT}")
            self.center_window()
        
       
        ctk.set_appearance_mode("light")
        
        # === CONFIGURACIÓN DE EVENTOS ===
        # Cambiar Escape para minimizar en lugar de cerrar (mejor UX)
        self.bind("<Escape>", self.minimize_window)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # === CONFIGURACIÓN DE ICONO ===
        try:
            from pathlib import Path
            icon_path = Path(__file__).parent / "assets" / "app_icon.ico"
            if icon_path.exists():
                self.iconbitmap(str(icon_path))
        except:
            pass

        # === VERIFICAR SESIÓN AL INICIAR ===
        self.check_session()

    def center_window(self):
        """Centra la ventana en la pantalla cuando no está maximizada"""
        self.update_idletasks()
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def check_session(self):
        """Verifica si hay una sesión activa guardada"""
        try:
            session = self.auth_service.load_session()
            if session:
                logging.info("Sesión activa encontrada, iniciando aplicación principal")
                self.show_main_window()
            else:
                logging.info("No hay sesión activa, mostrando login")
                self.show_login_window()
        except Exception as e:
            logging.error(f"Error al cargar la sesión: {e}")
            self.show_login_window()

    def _cleanup_current_frame(self):
        """Limpia el frame actual antes de mostrar uno nuevo"""
        if self.current_frame:
            self.current_frame.destroy()
            self.current_frame = None

    def show_login_window(self):
        """Muestra la ventana de login centrada"""
        self._cleanup_current_frame()
        
        logging.info("Mostrando ventana de login")
        
        # Crear contenedor para centrar el login
        login_container = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        login_container.pack(fill="both", expand=True)
        
        # Crear la ventana de login
        self.current_frame = LoginWindow(login_container, auth_service=self.auth_service)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Agregar efecto de entrada suave
        self.current_frame.configure(fg_color=self.current_frame.cget("fg_color"))
        
        logging.info("Ventana de login configurada correctamente")

    def show_main_window(self):
        """Muestra la ventana principal de la aplicación"""
        self._cleanup_current_frame()
        
        logging.info("Mostrando ventana principal")
        
        # Crear la ventana principal
        self.current_frame = MainWindow(self)
        self.current_frame.pack(fill="both", expand=True)
        
        logging.info("Ventana principal configurada correctamente")
        
    def minimize_window(self, event=None):
        """Minimiza la ventana (mejor UX que cerrar con Escape)"""
        self.iconify()
        
    def on_closing(self, event=None):
        """Maneja el cierre de la aplicación con confirmación"""
        try:
            # Opcional: Agregar confirmación antes de cerrar
            import tkinter.messagebox as msgbox
            
            # Solo mostrar confirmación si hay sesión activa
            if hasattr(self, 'current_frame') and isinstance(self.current_frame, MainWindow):
                result = msgbox.askyesno(
                    "Cerrar Aplicación", 
                    "¿Estás seguro que deseas cerrar BuildMate?",
                    icon="question"
                )
                if not result:
                    return
            
            # Limpiar recursos
            logging.info("Cerrando aplicación...")
            
            # Cerrar sesión si está activa
            if hasattr(self.auth_service, 'current_session') and self.auth_service.current_session:
                try:
                    # Solo limpiar la sesión local, no cerrar sesión en servidor
                    pass
                except Exception as e:
                    logging.error(f"Error al limpiar sesión: {e}")
            
        except Exception as e:
            logging.error(f"Error al cerrar aplicación: {e}")
        finally:
            self.quit()
            self.destroy()

def configure_app_theme():
    """Configura el tema global de la aplicación"""
    # Configurar tema claro para trabajar mejor con los nuevos colores
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Configuración para pantallas de alta resolución (Windows)
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

def main():
    """Función principal de la aplicación"""
    
    # Configurar tema antes de crear ventanas
    configure_app_theme()
    
    try:
        # Inicializar servicios
        logging.info("Inicializando servicios...")
        supabase_client = get_supabase_client()
        auth_service = AuthService(supabase_client)
        logging.info("Servicios inicializados correctamente")
        
        # Crear y ejecutar aplicación
        logging.info("Iniciando aplicación BuildMate...")
        app = App(supabase_client, auth_service)
        
        # Agregar información de versión en el log
        logging.info("BuildMate v1.0.0 - Sistema de Gestión de Proyectos de Construcción")
        
        app.mainloop()
        
    except ValueError as e:
        logging.error(f"Error de conexión con la base de datos: {e}")
        # Mostrar mensaje de error al usuario
        try:
            import tkinter as tk
            import tkinter.messagebox as msgbox
            
            root = tk.Tk()
            root.withdraw()  # Ocultar ventana principal
            
            msgbox.showerror(
                "Error de Conexión",
                f"No se pudo conectar con la base de datos:\n{e}\n\nVerifica tu conexión a internet y la configuración."
            )
            
            root.destroy()
        except:
            print(f"Error crítico: {e}")
        
        return
        
    except Exception as e:
        logging.error(f"Error crítico al iniciar la aplicación: {e}")
        return
    
    finally:
        logging.info("Aplicación cerrada correctamente")

if __name__ == "__main__":
    main()