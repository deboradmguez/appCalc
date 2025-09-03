import tkinter as tk
import customtkinter as ctk
from supabase import Client
import logging

from src.services.auth_service import AuthService
from src.ui.widgets.notification_system import NotificationSystem
from src.ui.windows.proyecto_form_window import ProyectoFormWindow
from src.ui.components.sidebar import Sidebar

# --- Importamos nuestras páginas ---
from src.ui.pages.proyectos_page import ProyectosPage
from src.ui.pages.project_detail_page import ProjectDetailPage 
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
        self.current_page = None 
        
        # Configuración de la ventana
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.title("Administrador de Proyectos")
        self.master.geometry("1200x750")
        self.master.minsize(800, 600)
        
        # --- Configuración del grid principal ---
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)
        # La columna 0 (sidebar) NO debe expandirse
        self.master.grid_columnconfigure(0, weight=0, minsize=70)
        
        # --- Crear comandos para el sidebar ---
        commands = {
            "Proyectos": self.show_proyectos_page,
            "Materiales": self.show_materiales_page,
            "Áreas": self.show_areas_page,
            "Configuración": self.show_configuracion_page
        }
        
        # --- Crear sidebar ---
        self.sidebar = Sidebar(self.master, commands=commands)
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        
        # --- Contenedor de vistas ---
        self.view_container = ctk.CTkFrame(
            self.master, 
            corner_radius=0,
            fg_color=("gray92", "gray14")
        )
        self.view_container.grid(row=0, column=1, sticky="nsew")
        
        # --- Sistema de notificaciones ---
        self.notification_system = NotificationSystem(self.view_container)
        
        # Mostrar página inicial
        self.show_proyectos_page()

    def _switch_page(self, page_class, *args, **kwargs):
        """Función genérica para limpiar y mostrar una nueva página."""
        # Limpiar página actual
        if self.current_page:
            self.current_page.destroy()
        
        try:
            # Crear nueva página
            self.current_page = page_class(self.view_container, *args, **kwargs)
            self.current_page.pack(fill="both", expand=True, padx=20, pady=20)
        except Exception as e:
            logging.error(f"Error al cambiar página: {e}")
            self.notification_system.show_error(f"Error al cargar la página: {str(e)}")

    def show_proyectos_page(self):
        """Muestra la página de proyectos."""
        self.sidebar.set_active_button("Proyectos")
        self._switch_page(
            ProyectosPage, 
            supabase_client=self.supabase_client,
            on_create_new=self.create_new_proyecto,
            on_view_details=self.show_project_detail_page,
            notification_system=self.notification_system
        )

    def show_project_detail_page(self, proyecto):
        """Muestra la página de detalles de un proyecto."""
        self._switch_page(
            ProjectDetailPage,
            supabase_client=self.supabase_client,
            proyecto=proyecto,
            on_back=self.show_proyectos_page,
            notification_system=self.notification_system
        )

    def show_materiales_page(self):
        """Muestra la página de materiales."""
        self.sidebar.set_active_button("Materiales")
        self._switch_page(
            MaterialesView, 
            supabase_client=self.supabase_client,
            notification_system=self.notification_system
        )

    def show_areas_page(self):
        """Muestra la página de áreas."""
        self.sidebar.set_active_button("Áreas")
        self._switch_page(
            AreasView, 
            supabase_client=self.supabase_client,
            notification_system=self.notification_system
        )

    def show_configuracion_page(self):
        """Muestra la página de configuración."""
        self.sidebar.set_active_button("Configuración")
        self._switch_page(
            ConfiguracionView, 
            on_logout=self.logout,
            notification_system=self.notification_system
        )

    def create_new_proyecto(self):
        """Abre el formulario para crear un nuevo proyecto."""
        try:
            ProyectoFormWindow(
                self.master, 
                self.supabase_client, 
                callback=self.on_proyecto_created
            )
        except Exception as e:
            logging.error(f"Error al abrir formulario de proyecto: {e}")
            self.notification_system.show_error("Error al abrir el formulario")

    def on_proyecto_created(self):
        """Callback ejecutado cuando se crea un nuevo proyecto."""
        self.notification_system.show_success("Proyecto creado exitosamente")
        self.show_proyectos_page()

    def on_closing(self):
        """Maneja el cierre de la aplicación."""
        self.app_state['is_closing'] = True
        self.master.destroy()
    
    def logout(self):
        """Maneja el cierre de sesión."""
        result = tk.messagebox.askyesno(
            "Cerrar Sesión", 
            "¿Estás seguro que deseas cerrar sesión?",
            parent=self.master
        )
        
        if result:
            try:
                self.auth_service.logout()
                self.notification_system.show_success("Sesión cerrada correctamente")
                # Esperar un momento antes de cerrar para que se vea la notificación
                self.master.after(1000, self.master.destroy)
            except Exception as e:
                logging.error(f"Error al cerrar sesión: {e}")
                self.notification_system.show_error("Error al cerrar sesión")
                self.master.destroy()