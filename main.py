import tkinter as tk
import logging
from src.ui.login_window import LoginWindow
from src.ui.main_window import MainWindow
from src.services.auth_service import AuthService
from src.database.supabase_client import get_supabase_client

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    """
    Función principal para inicializar y ejecutar la aplicación.
    """
    # Usamos un diccionario para pasar el estado de la app de forma mutable
    app_state = {'is_closing': False}
    
    # Intenta conectarse a la base de datos de Supabase.
    try:
        supabase_client = get_supabase_client()
        auth_service = AuthService(supabase_client)
        logging.info("Conexión con Supabase establecida.")
        
    except ValueError as e:
        logging.error(f"Error de conexión: {e}")
        return
        
    # Bucle principal de la aplicación para manejar reinicios
    while not app_state['is_closing']:
        root = tk.Tk()
        root.state('zoomed')
        
        # Inicializamos la variable antes de los bloques try/except
        current_window = None
        
        # Cargar sesión si existe, de lo contrario mostrar la ventana de login
        try:
            session = auth_service.load_session()
            if session:
                current_window = MainWindow(root, supabase_client, auth_service, app_state)
                logging.info("Sesión restaurada. Mostrando ventana principal.")
            else:
                current_window = LoginWindow(root, supabase_client, auth_service, app_state)
                logging.info("No hay sesión guardada. Mostrando ventana de login.")
        except Exception as e:
            logging.error(f"Error al cargar la sesión: {e}")
            current_window = LoginWindow(root, supabase_client, auth_service, app_state)

        root.mainloop()
        
        if not app_state['is_closing']:
            # La ventana se cerró por logout, continuamos el bucle
            continue
        
        # Si se cerró por la 'X', salimos del bucle
        break

if __name__ == "__main__":
    main()
