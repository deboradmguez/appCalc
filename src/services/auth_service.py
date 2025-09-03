import keyring
import logging
from supabase import Client
from supabase import AuthApiError

# Nombre de la aplicación para keyring
APP_NAME = "appCalc_supabase"

class AuthService:
    """
    Clase de servicio para manejar la autenticación con Supabase
    usando keyring para persistencia.
    """

    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        logging.info("Servicio de autenticación inicializado.")

    def login(self, email, password):
        try:
            auth_response = self.supabase.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            logging.info(f"Inicio de sesión exitoso para {email}.")
            return auth_response
        except Exception as e:
            logging.error(f"Error de inicio de sesión para {email}: {e}")
            raise e

    def signup(self, email, password):
        try:
            auth_response = self.supabase.auth.sign_up(
                {"email": email, "password": password}
            )
            logging.info(f"Registro exitoso para {email}.")
            return auth_response
        except Exception as e:
            logging.error(f"Error de registro para {email}: {e}")
            raise e

    def logout(self):
        try:
            self.supabase.auth.sign_out()
            self.delete_session()
            logging.info("Sesión de usuario cerrada con éxito.")
        except Exception as e:
            logging.error(f"Error al cerrar la sesión: {e}")
            raise e

    def save_session(self, refresh_token):
        try:
            keyring.set_password(APP_NAME, "refresh_token", refresh_token)
            logging.info("Refresh token guardado en keyring.")
        except Exception as e:
            logging.error(f"Error al guardar la sesión en keyring: {e}")

    def load_session(self):
        try:
            refresh_token = keyring.get_password(APP_NAME, "refresh_token")
            if refresh_token:
                self.supabase.auth.refresh_session(refresh_token)
                user_session = self.supabase.auth.get_session()
                if user_session:
                    logging.info("Sesión restaurada con éxito.")
                    return user_session
            return None
        except AuthApiError as e:
            logging.error(f"Error de autenticación al restaurar la sesión: {e}")
            self.delete_session()
            raise e
        except Exception as e:
            logging.error(f"Error inesperado al cargar la sesión guardada: {e}")
            return None

    def delete_session(self):
        try:
            keyring.delete_password(APP_NAME, "refresh_token")
            logging.info("Sesión eliminada de keyring.")
        except Exception as e:
            logging.error(f"Error al eliminar la sesión de keyring: {e}")
