# src/ui/main_window.py

import customtkinter as ctk
from tkinter import messagebox

from src.ui.components.sidebar import Sidebar
from src.ui.pages.proyectos_page import ProyectosPage
from src.ui.pages.project_detail_page import ProjectDetailPage
from src.ui.pages.areas_view import AreasView
from src.ui.pages.materiales_view import MaterialesView
from src.ui.pages.configuracion_view import ConfiguracionView
from src.ui.windows.proyecto_form_window import ProyectoFormWindow

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.master = master # Guardamos una referencia a la ventana App principal
        self.supabase_client = master.supabase_client
        self.auth_service = master.auth_service
        self.current_page = None 
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)

        commands = {
            "Proyectos": self.show_proyectos_page,
            "Materiales": self.show_materiales_page,
            "Areas": self.show_areas_page,
            "Configuración": self.show_configuracion_page
        }
        
        self.sidebar_frame = Sidebar(self, commands=commands)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")

        self.view_container = ctk.CTkFrame(self, corner_radius=0)
        self.view_container.grid(row=0, column=1, sticky="nsew")
        
        self.show_proyectos_page()

    def _switch_page(self, page_class, **kwargs):
        if self.current_page:
            self.current_page.destroy()
        
        self.current_page = page_class(self.view_container, master_app=self.master, **kwargs)
        self.current_page.pack(fill="both", expand=True, padx=20, pady=20)

    def create_new_proyecto(self):
        # --- CAMBIO IMPORTANTE ---
        # Pasamos self.master (la ventana App) como padre de la ventana emergente.
        form = ProyectoFormWindow(self.master, callback=self.show_proyectos_page)
        form.grab_set()

    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro?"):
            self.auth_service.logout()
            self.master.show_login_window()

    # --- Métodos para cambiar de página (sin cambios) ---
    def show_proyectos_page(self):
        self._switch_page(ProyectosPage, on_create_new=self.create_new_proyecto, on_view_details=self.show_project_detail_page)
    def show_project_detail_page(self, proyecto):
        self._switch_page(ProjectDetailPage, proyecto=proyecto, on_back=self.show_proyectos_page)
    def show_materiales_page(self):
        self._switch_page(MaterialesView)
    def show_areas_page(self):
        self._switch_page(AreasView)
    def show_configuracion_page(self):
        self._switch_page(ConfiguracionView, on_logout=self.logout)