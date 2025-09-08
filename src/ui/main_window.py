# src/ui/main_window.py (Versión final con "cerrar al hacer clic afuera")

import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
from pathlib import Path

from src.ui.components.sidebar import Sidebar
from src.ui.pages.proyectos_page import ProyectosPage
from src.ui.pages.project_detail_page import ProjectDetailPage
from src.ui.pages.areas_view import AreasView
from src.ui.pages.materiales_view import MaterialesView
from src.ui.pages.configuracion_view import ConfiguracionView
from src.ui.windows.proyecto_form_window import ProyectoFormWindow
from config import get_main_colors, get_sidebar_colors

class MainWindow(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        self.colors = get_main_colors()
        sidebar_colors = get_sidebar_colors()
        super().__init__(master, fg_color=self.colors['bg_primary'], **kwargs)
        
        self.master = master
        self.supabase_client = master.supabase_client
        self.auth_service = master.auth_service

        self.view_container = ctk.CTkFrame(
            self, corner_radius=0, fg_color=self.colors['bg_primary']
        )
        self.view_container.place(x=0, y=0, relwidth=1.0, relheight=1.0)

        commands = {
            "Proyectos": self.show_proyectos_page,
            "Materiales": self.show_materiales_page,
            "Áreas": self.show_areas_page,
            "Configuración": self.show_configuracion_page
        }
        
        self.sidebar_frame = Sidebar(self, commands=commands)
        self.sidebar_frame.place(x=-self.sidebar_frame.EXPANDED_WIDTH, y=0, relheight=1)

        try:
            icon_path = Path(__file__).resolve().parent.parent / "assets" / "icons" / "menu.png"
            menu_icon = ctk.CTkImage(Image.open(icon_path), size=(20, 20))
        except Exception as e:
            print(f"Error cargando ícono de menú: {e}")
            menu_icon = None

        self.menu_button = ctk.CTkButton(
            self, text="", image=menu_icon, width=40, height=40, corner_radius=0,
            fg_color=sidebar_colors['bg'], hover_color=sidebar_colors['hover'],
            command=self.sidebar_frame.toggle_slide
        )
        self.menu_button.place(x=15, y=15)
        
        self.menu_button.lift()
        
        self.show_proyectos_page()

    # NUEVO: Función recursiva para vincular el evento de clic a un widget y todos sus hijos.
    def _bind_click_outside(self, widget):
        """Vincula el evento de clic para cerrar el sidebar."""
        # Vinculamos el widget principal
        widget.bind("<Button-1>", lambda event: self.sidebar_frame.hide())

        # Vinculamos todos los widgets hijos recursivamente
        for child in widget.winfo_children():
            # Nos aseguramos de no sobreescribir la funcionalidad de botones, entradas, etc.
            if isinstance(child, (ctk.CTkButton, ctk.CTkEntry, ctk.CTkOptionMenu, ctk.CTkScrollableFrame, ctk.CTkTextbox, ctk.CTkSlider)):
                continue
            self._bind_click_outside(child)

    def _switch_page(self, page_class, **kwargs):
        for widget in self.view_container.winfo_children():
            widget.destroy()
        
        page_wrapper = ctk.CTkFrame(self.view_container, fg_color=self.colors['bg_primary'])
        page_wrapper.pack(fill="both", expand=True, padx=(70, 25), pady=(25,25))
        
        current_page = page_class(
            page_wrapper, master_app=self.master, **kwargs
        )
        current_page.pack(fill="both", expand=True)

        # NUEVO: Activamos la detección de clic en la nueva página cargada.
        self._bind_click_outside(page_wrapper)


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