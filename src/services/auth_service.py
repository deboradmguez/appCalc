import json
import os
from pathlib import Path
from supabase import Client
import logging

class AuthService:
    """Servicio de autenticación mejorado con mejor manejo de sesiones."""
    
    def __init__(self, supabase_client: Client):
        self.supabase = supabase_client
        self.session_file = Path.home() / ".proyecto_manager" / "session.json"
        self.session_file.parent.mkdir(exist_ok=True)

    def login(self, email: str, password: str):
        """Inicia sesión con email y contraseña."""
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.session:
                logging.info(f"Login exitoso para: {email}")
                return response
            else:
                raise Exception("No se pudo iniciar sesión")
                
        except Exception as e:
            logging.error(f"Error en login: {e}")
            raise

    def signup(self, email: str, password: str):
        """Registra un nuevo usuario."""
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                logging.info(f"Registro exitoso para: {email}")
                return response
            else:
                raise Exception("No se pudo registrar el usuario")
                
        except Exception as e:
            logging.error(f"Error en registro: {e}")
            raise

    def logout(self):
        """Cierra la sesión actual."""
        try:
            self.supabase.auth.sign_out()
            self.clear_session()
            logging.info("Sesión cerrada correctamente")
        except Exception as e:
            logging.error(f"Error al cerrar sesión: {e}")
            # Aún así limpiamos la sesión local
            self.clear_session()

    def save_session(self, refresh_token: str):
        """Guarda el token de sesión localmente."""
        try:
            session_data = {
                "refresh_token": refresh_token
            }
            
            with open(self.session_file, 'w') as f:
                json.dump(session_data, f)
            
            logging.info("Sesión guardada localmente")
        except Exception as e:
            logging.error(f"Error al guardar sesión: {e}")

    def load_session(self):
        """Carga la sesión desde el archivo local."""
        try:
            if not self.session_file.exists():
                return None
            
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
            
            refresh_token = session_data.get("refresh_token")
            if not refresh_token:
                return None
            
            # Intentar refrescar la sesión
            response = self.supabase.auth.refresh_session(refresh_token)
            
            if response.session:
                logging.info("Sesión cargada y refrescada correctamente")
                return response.session
            else:
                logging.warning("No se pudo refrescar la sesión")
                self.clear_session()
                return None
                
        except Exception as e:
            logging.error(f"Error al cargar sesión: {e}")
            self.clear_session()
            return None

    def validate_session(self, session):
        """Valida si una sesión sigue siendo válida."""
        try:
            if not session:
                return False
            
            # Verificar si tenemos un usuario válido
            user = self.supabase.auth.get_user()
            if not user or not user.user:
                logging.warning("No hay usuario válido en la sesión")
                return False
                
            return True
            
        except Exception as e:
            logging.error(f"Error al validar sesión: {e}")
            return False

    def clear_session(self):
        """Elimina la sesión guardada localmente."""
        try:
            if self.session_file.exists():
                self.session_file.unlink()
            logging.info("Sesión local eliminada")
        except Exception as e:
            logging.error(f"Error al eliminar sesión local: {e}")

    def get_current_user(self):
        """Obtiene el usuario actual si hay una sesión activa."""
        try:
            user = self.supabase.auth.get_user()
            return user.user if user else None
        except Exception as e:
            logging.error(f"Error al obtener usuario actual: {e}")
            return None