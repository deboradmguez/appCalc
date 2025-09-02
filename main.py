import tkinter as tk
from src.ui.login_window import LoginWindow
from src.database.supabase_client import get_supabase_client

def main():
    """Función principal para inicializar y ejecutar la aplicación."""
    
    # Intenta conectarse a la base de datos de Supabase.
    try:
        supabase_client = get_supabase_client()
        print("Conexión con Supabase establecida.")
        
    except ValueError as e:
        print(f"Error de conexión: {e}")
        return
        
    # Crea la ventana principal de la aplicación.
    root = tk.Tk()
    
    # Configura la ventana para que sea de pantalla completa
    root.state('zoomed') 
    
    # Inicializa la ventana de inicio de sesión.
    login_window = LoginWindow(root, supabase_client)
    
    # Inicia el bucle principal de la aplicación.
    root.mainloop()

if __name__ == "__main__":
    main()