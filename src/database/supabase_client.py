import os
from dotenv import load_dotenv
from supabase import create_client, Client
from urllib.parse import urlparse, parse_qs

# --- Configuración y Conexión ---
# Usa una ruta relativa para encontrar el archivo .env sin importar el directorio
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

# Obtiene las credenciales del entorno
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_API_KEY")

if not url or not key:
    raise ValueError("Las credenciales de Supabase no se encontraron. Asegúrate de que el archivo .env está en la raíz del proyecto y tiene las variables SUPABASE_URL y SUPABASE_API_KEY.")

# Crea una instancia del cliente de Supabase
supabase: Client = create_client(url, key)

def get_supabase_client() -> Client:
    """Devuelve la instancia del cliente de Supabase para ser usada en otras partes del código."""
    return supabase



def get_all_projects():
    """Obtiene todos los proyectos de la base de datos."""
    try:
        response = supabase.from_("proyectos").select("*").execute()
        return response.data
    except Exception as e:
        print(f"Error al obtener proyectos: {e}")
        return None

# --- Función para Confirmar Email (uso temporal) ---
def confirm_email_from_url(url_from_email):
    """
    Confirma el email de un usuario usando el enlace de su correo.
    Se puede llamar manualmente para confirmar un registro.
    """
    try:
        parsed_url = urlparse(url_from_email)
        query_params = parse_qs(parsed_url.query)
        access_token = query_params.get("access_token")
        refresh_token = query_params.get("refresh_token")
        
        if not access_token:
            print("Error: El enlace no contiene un access token.")
            return

        # Intenta iniciar la sesión con el token para verificarlo
        auth_response = supabase.auth.set_session(access_token[0], refresh_token[0])
        print("¡Email confirmado con éxito!")
        return auth_response

    except Exception as e:
        print(f"Error al confirmar el email: {e}")
        return None

# --- Bloque de Prueba para la Conexión ---
if __name__ == "__main__":
    print("Este script prueba la conexión con la base de datos de Supabase.")
    print("Si ves el mensaje de éxito, tu cliente de Python está listo para usarse.")
    

    # 2. Intenta obtener todos los proyectos
    print("\nIntentando obtener proyectos...")
    proyectos = get_all_projects()
    if proyectos:
        print("¡Conexión exitosa! Proyectos obtenidos:")
        print(proyectos)
    else:
        print("No se encontraron proyectos o la conexión falló.")
        print("Asegúrate de que la tabla 'proyectos' existe y el RLS está desactivado.")