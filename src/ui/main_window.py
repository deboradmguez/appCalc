# src/ui/main_window.py (Corregido el layout del contenedor)

import customtkinter as ctk
from tkinter import messagebox

from src.ui.components.sidebar import Sidebar
from src.ui.pages.proyectos_page import ProyectosPage
from src.ui.pages.project_detail_page import ProjectDetailPage
from src.ui.pages.areas_view import AreasView
from src.ui.pages.materiales_view import MaterialesView
from src.ui.pages.configuracion_view import ConfiguracionView
from src.ui.windows.proyecto_form_window import ProyectoFormWindow
from config import get_main_colors

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        self.colors = get_main_colors()
        super().__init__(master, fg_color=self.colors['bg_primary'], **kwargs)
        
        self.master = master
        self.supabase_client = master.supabase_client
        self.auth_service = master.auth_service
        self.page_wrapper = None

        commands = {
            "Proyectos": self.show_proyectos_page,
            "Materiales": self.show_materiales_page,
            "Áreas": self.show_areas_page,
            "Configuración": self.show_configuracion_page
        }
        
        self.sidebar_frame = Sidebar(self, commands=commands, animation_callback=self.update_view_layout)
        self.sidebar_frame.place(x=0, y=0, relheight=1)

        self.view_container = ctk.CTkFrame(
            self, corner_radius=0, fg_color=self.colors['bg_primary'], border_width=0
        )
        
        # CORREGIDO: Se eliminó 'relwidth=1.0' que causaba el desbordamiento.
        # Ahora el ancho se gestionará explícitamente.
        self.view_container.place(
            x=self.sidebar_frame.EXPANDED_WIDTH, y=0, relheight=1.0
        )
        
        self.shadow_separator = ctk.CTkFrame(self, width=1, fg_color=self.colors['border'], corner_radius=0)
        self.shadow_separator.place(x=self.sidebar_frame.EXPANDED_WIDTH, y=0, relheight=1.0)
        
        self.bind("<Configure>", self.on_main_resize)
        self.show_proyectos_page()

    def on_main_resize(self, event=None):
        # Esta función ahora se encarga correctamente de ajustar el ancho al cambiar el tamaño de la ventana.
        sidebar_visible_width = self.sidebar_frame.winfo_x() + self.sidebar_frame.EXPANDED_WIDTH
        self.view_container.place_configure(width=self.winfo_width() - sidebar_visible_width)

    def update_view_layout(self, content_x_pos):
        """
        Mueve y redimensiona el contenedor de la vista durante la animación del sidebar.
        """
        content_width = self.winfo_width() - content_x_pos
        self.view_container.place_configure(x=content_x_pos, width=content_width)
        self.shadow_separator.place_configure(x=content_x_pos)
        self.update_idletasks()

    def _switch_page(self, page_class, **kwargs):
        if self.page_wrapper:
            self.page_wrapper.destroy()
        
        self.page_wrapper = ctk.CTkFrame(
            self.view_container, fg_color=self.colors['bg_primary'], corner_radius=0, border_width=0
        )
        self.page_wrapper.pack(fill="both", expand=True, padx=25, pady=25)
        
        current_page = page_class(
            self.page_wrapper, master_app=self.master, **kwargs
        )
        current_page.pack(fill="both", expand=True)

    def create_new_proyecto(self):
        form = ProyectoFormWindow(self.master, callback=self.show_proyectos_page)
        form.grab_set()

    def logout(self):
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que deseas cerrar sesión?", icon="question"):
            try:
                self.auth_service.logout()
                self.master.show_login_window()
                messagebox.showinfo("Sesión Cerrada", "Has cerrado sesión exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cerrar sesión: {e}")
            
    def show_proyectos_page(self):
        self.sidebar_frame.set_selected_button("Proyectos")
        self._switch_page(
            ProyectosPage, on_create_new=self.create_new_proyecto, on_view_details=self.show_project_detail_page
        )

    def show_project_detail_page(self, proyecto):
        self.sidebar_frame.set_selected_button("Proyectos")
        self._switch_page(
            ProjectDetailPage, proyecto=proyecto, on_back=self.show_proyectos_page
        )

    def show_materiales_page(self):
        self.sidebar_frame.set_selected_button("Materiales")
        self._switch_page(MaterialesView)

    def show_areas_page(self):
        self.sidebar_frame.set_selected_button("Áreas")
        self._switch_page(AreasView)

    def show_configuracion_page(self):
        self.sidebar_frame.set_selected_button("Configuración")
        self._switch_page(ConfiguracionView, on_logout=self.logout)