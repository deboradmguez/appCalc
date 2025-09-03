import tkinter as tk
from supabase import Client
import logging

from src.services.auth_service import AuthService
from src.ui.widgets.notification_system import NotificationSystem
from config import *
from src.ui.windows.proyecto_form_window import ProyectoFormWindow
from src.ui.components.sidebar import Sidebar

# --- Importamos nuestras nuevas clases de página ---
from src.ui.pages.proyectos_page import ProyectosPage
from src.ui.pages.project_detail_page import ProjectDetailPage

# Las vistas simples pueden permanecer aquí por ahora
from src.ui.pages.areas_view import AreasView 
from src.ui.pages.materiales_view import MaterialesView
from src.ui.pages.configuracion_view import ConfiguracionView

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MainWindow:
    def __init__(self, master, supabase_client: Client, auth_service: AuthService, app_state):
        self.master = master
        self.supabase_client = supabase_client
        self.auth_service = auth_service
        self.app_state = app_state
        self.current_page = None # Para mantener una referencia a la página actual
        
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.title("Administrador de Proyectos")
        self.master.configure(bg=GRAPHITE)
        self.master.geometry("1200x750")
        
        commands = {
            "Proyectos": self.show_proyectos_page,
            "Materiales": self.show_materiales_page,
            "Areas": self.show_areas_page,
            "Configuración": self.show_configuracion_page
        }
        self.sidebar = Sidebar(self.master, commands=commands)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        self.view_container = tk.Frame(self.master, bg=DARK_GRAY)
        self.view_container.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.show_proyectos_page() # Página inicial

    def _switch_page(self, page_class, *args, **kwargs):
        """Función genérica para limpiar y mostrar una nueva página."""
        if self.current_page:
            self.current_page.destroy()
        
        self.current_page = page_class(self.view_container, *args, **kwargs)
        self.current_page.pack(fill=tk.BOTH, expand=True)

    def show_proyectos_page(self):
        self._switch_page(ProyectosPage, 
                          supabase_client=self.supabase_client,
                          on_create_new=self.create_new_proyecto,
                          on_view_details=self.show_project_detail_page)

    def show_project_detail_page(self, proyecto):
        self._switch_page(ProjectDetailPage,
                          supabase_client=self.supabase_client,
                          proyecto=proyecto,
                          on_back=self.show_proyectos_page)

    def show_materiales_page(self):
        self._switch_page(MaterialesView, supabase_client=self.supabase_client)

    def show_areas_page(self):
        # Pasamos el cliente de supabase a la vista de áreas
        self._switch_page(AreasView, supabase_client=self.supabase_client)

    def show_configuracion_page(self):
        # Pasamos el callback de logout
        self._switch_page(ConfiguracionView, on_logout=self.logout)

    def create_new_proyecto(self):
        # La ventana de creación sigue siendo un Toplevel (pop-up)
        # El callback ahora es show_proyectos_page para refrescar la lista
        ProyectoFormWindow(self.master, self.supabase_client, callback=self.show_proyectos_page)

    def on_closing(self):
        self.app_state['is_closing'] = True
        self.master.destroy()
    
    def logout(self):
        if tk.messagebox.askyesno("Cerrar Sesión", "¿Estás seguro?"):
            self.auth_service.logout()
            self.master.destroy()