"""
Main.py - Punto de entrada de la aplicación
Soluciona el problema de inicialización de CustomTkinter
"""

import sys
import logging
from pathlib import Path

# Configurar el path para importaciones
sys.path.append(str(Path(__file__).resolve().parent))

# Configurar logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    """Función principal de la aplicación."""
    try:
        # 1. Primero inicializar CustomTkinter
        import customtkinter as ctk
        
        # Configurar CustomTkinter ANTES que nada
        ctk.set_appearance_mode("dark")  # "light", "dark", "system"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        # 2. Crear ventana temporal para inicializar el sistema
        temp_root = ctk.CTk()
        temp_root.withdraw()  # Ocultar inmediatamente
        
        # 3. Ahora es seguro importar módulos que usen CTkFont
        from src.ui.login_window import LoginWindow
        from src.ui.main_window import MainWindow
        from src.services.auth_service import AuthService
        from src.database.supabase_client import get_supabase_client
        
        # 4. Destruir ventana temporal
        temp_root.destroy()
        
        logging.info("Inicializando aplicación...")
        
        # 5. Estado de la aplicación
        app_state = {'is_closing': False}
        
        # 6. Conectar con Supabase
        try:
            supabase_client = get_supabase_client()
            auth_service = AuthService(supabase_client)
            logging.info("Conexión con Supabase establecida")
        except ValueError as e:
            logging.error(f"Error de conexión con Supabase: {e}")
            return 1
        except Exception as e:
            logging.error(f"Error inesperado al conectar: {e}")
            return 1
            
        # 7. Bucle principal de la aplicación
        while not app_state['is_closing']:
            try:
                # Crear ventana principal
                root = ctk.CTk()
                root.title("Administrador de Proyectos")
                
                # Configurar la ventana
                root.geometry("1200x800")
                root.minsize(800, 600)
                
                # Intentar maximizar
                try:
                    root.state('zoomed')  # Windows
                except:
                    try:
                        root.attributes('-zoomed', True)  # Linux
                    except:
                        pass  # macOS
                
                # Protocolo de cierre
                def on_closing():
                    app_state['is_closing'] = True
                    root.quit()
                    root.destroy()
                
                root.protocol("WM_DELETE_WINDOW", on_closing)
                
                # Determinar ventana a mostrar
                current_window = None
                
                try:
                    session = auth_service.load_session()
                    if session and auth_service.validate_session(session):
                        logging.info("Sesión válida, cargando ventana principal")
                        current_window = MainWindow(root, supabase_client, auth_service, app_state)
                    else:
                        logging.info("Sin sesión válida, mostrando login")
                        current_window = LoginWindow(root, supabase_client, auth_service, app_state)
                        
                except Exception as e:
                    logging.error(f"Error al validar sesión: {e}")
                    current_window = LoginWindow(root, supabase_client, auth_service, app_state)
                
                # Iniciar bucle de eventos
                logging.info("Iniciando interfaz gráfica")
                root.mainloop()
                
                # Si no estamos cerrando, reiniciar
                if not app_state['is_closing']:
                    logging.info("Reiniciando aplicación...")
                    continue
                else:
                    break
                    
            except KeyboardInterrupt:
                logging.info("Aplicación interrumpida por el usuario")
                app_state['is_closing'] = True
                break
                
            except Exception as e:
                logging.error(f"Error en el bucle principal: {e}")
                import traceback
                traceback.print_exc()
                
                # Preguntar si reiniciar
                try:
                    import tkinter.messagebox as msgbox
                    respuesta = msgbox.askyesno(
                        "Error",
                        f"Error inesperado: {e}\n\n¿Deseas reiniciar la aplicación?"
                    )
                    if not respuesta:
                        app_state['is_closing'] = True
                        break
                except:
                    # Si no podemos mostrar el diálogo, cerrar
                    app_state['is_closing'] = True
                    break
        
        logging.info("Aplicación cerrada correctamente")
        return 0
        
    except ImportError as e:
        logging.error(f"Error de importación: {e}")
        print("Error: No se pudieron importar los módulos necesarios.")
        print("Verifica que todas las dependencias estén instaladas.")
        return 1
        
    except Exception as e:
        logging.error(f"Error crítico: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)