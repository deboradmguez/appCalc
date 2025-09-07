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
        # Obtenemos los colores principales
        self.colors = get_main_colors()
        
        super().__init__(master, fg_color=self.colors['bg_primary'], **kwargs)
        
        self.master = master
        self.supabase_client = master.supabase_client
        self.auth_service = master.auth_service
        self.page_wrapper = None 

        # --- Layout usando .place() para animación suave ---
        commands = {
            "Proyectos": self.show_proyectos_page,
            "Materiales": self.show_materiales_page,
            "Áreas": self.show_areas_page,
            "Configuración": self.show_configuracion_page
        }
        
        self.sidebar_frame = Sidebar(
            self, 
            commands=commands, 
            width_animation_callback=self.update_view_layout
        )
        self.sidebar_frame.place(x=0, y=0, relheight=1)

        # Contenedor principal con colores mejorados
        self.view_container = ctk.CTkFrame(
            self, 
            corner_radius=0, 
            fg_color=self.colors['bg_primary'],
            border_width=0
        )
        # Posicionamiento inicial, será actualizado por callbacks
        self.view_container.place(
            x=self.sidebar_frame.EXPANDED_WIDTH, 
            y=0, 
            relheight=1.0
        )
        
        # Agregar una sombra sutil entre el sidebar y el contenido
        self.shadow_separator = ctk.CTkFrame(
            self,
            width=1,
            fg_color=self.colors['border'],
            corner_radius=0
        )
        self.shadow_separator.place(
            x=self.sidebar_frame.EXPANDED_WIDTH - 1,
            y=0,
            relheight=1.0
        )
        
        # Vinculamos eventos para manejar redimensionamiento
        self.bind("<Configure>", self.on_main_resize)
        
        # Mostramos la página inicial
        self.show_proyectos_page()

    def on_main_resize(self, event=None):
        """Maneja el redimensionamiento de la ventana principal"""
        self.update_view_layout(self.sidebar_frame.winfo_width())

    def update_view_layout(self, sidebar_width):
        """Actualiza el layout del contenedor de vistas según el ancho del sidebar"""
        main_width = self.winfo_width()
        if main_width > sidebar_width:
            view_width = main_width - sidebar_width
            self.view_container.place_configure(x=sidebar_width, width=view_width)
            # Actualizar también la posición del separador
            self.shadow_separator.place_configure(x=sidebar_width - 1)
        self.update_idletasks()

    # DENTRO DE: src/ui/main_window.py -> class MainWindow

    def _switch_page(self, page_class, **kwargs):
        """
        Cambia entre páginas, asegurándose de limpiar la vista anterior correctamente.
        """
        # Si existe un contenedor de página anterior, lo destruimos por completo
        if self.page_wrapper:
            self.page_wrapper.destroy()
        
        # Creamos un nuevo contenedor que tendrá el padding correcto
        self.page_wrapper = ctk.CTkFrame(
            self.view_container,
            fg_color=self.colors['bg_primary'],
            corner_radius=0,
            border_width=0
        )
        self.page_wrapper.pack(fill="both", expand=True, padx=25, pady=25)
        
        # Creamos la nueva página dentro del nuevo contenedor
        current_page = page_class(
            self.page_wrapper, 
            master_app=self.master, 
            **kwargs
        )
        current_page.pack(fill="both", expand=True)

    def create_new_proyecto(self):
        """Abre el formulario para crear un nuevo proyecto"""
        form = ProyectoFormWindow(
            self.master, 
            callback=self.show_proyectos_page
        )
        form.grab_set()

    def logout(self):
        """Maneja el cierre de sesión del usuario"""
        result = messagebox.askyesno(
            "Cerrar Sesión", 
            "¿Estás seguro que deseas cerrar sesión?",
            icon="question"
        )
        if result:
            try:
                self.auth_service.logout()
                self.master.show_login_window()
                messagebox.showinfo("Sesión Cerrada", "Has cerrado sesión exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cerrar sesión: {e}")
            
    def show_proyectos_page(self):
        """Muestra la página de proyectos"""
        self.sidebar_frame.set_selected_button("Proyectos")
        self._switch_page(
            ProyectosPage, 
            on_create_new=self.create_new_proyecto, 
            on_view_details=self.show_project_detail_page
        )

    def show_project_detail_page(self, proyecto):
        """Muestra los detalles de un proyecto específico"""
        self.sidebar_frame.set_selected_button("Proyectos")
        self._switch_page(
            ProjectDetailPage, 
            proyecto=proyecto, 
            on_back=self.show_proyectos_page
        )

    def show_materiales_page(self):
        """Muestra la página de materiales"""
        self.sidebar_frame.set_selected_button("Materiales")
        self._switch_page(MaterialesView)

    def show_areas_page(self):
        """Muestra la página de áreas"""
        self.sidebar_frame.set_selected_button("Áreas")
        self._switch_page(AreasView)

    def show_configuracion_page(self):
        """Muestra la página de configuración"""
        self.sidebar_frame.set_selected_button("Configuración")
        self._switch_page(ConfiguracionView, on_logout=self.logout)