import tkinter as tk
from tkinter import messagebox, ttk
from supabase import Client

# Importación de la configuración
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import *

class MainWindow:
    def __init__(self, master, supabase_client: Client):
        self.master = master
        self.supabase_client = supabase_client
        
        # Configuración de la ventana principal
        self.master.title("Administrador de Proyectos")
        self.master.configure(bg=INDIGO_DYE)
        self.master.geometry("1000x700")
        
        # Frame principal para contener todas las vistas
        self.main_frame = tk.Frame(self.master, bg=INDIGO_DYE)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Barra de navegación
        self.navbar = tk.Frame(self.main_frame, bg=BLUE_MUNSELL)
        self.navbar.pack(side=tk.TOP, fill=tk.X, ipady=5)
        
        self.btn_proyectos = tk.Button(self.navbar, text="Proyectos", command=self.show_proyectos_view, **NAVBAR_BUTTON_STYLE)
        self.btn_proyectos.pack(side=tk.LEFT, padx=10, pady=5)

        self.btn_materiales = tk.Button(self.navbar, text="Administrar Materiales", command=self.show_materiales_view, **NAVBAR_BUTTON_STYLE)
        self.btn_materiales.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.btn_areas = tk.Button(self.navbar, text="Administrar Áreas", command=self.show_areas_view, **NAVBAR_BUTTON_STYLE)
        self.btn_areas.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.btn_cerrar_sesion = tk.Button(self.navbar, text="Cerrar Sesión", command=self.logout, **NAVBAR_BUTTON_STYLE)
        self.btn_cerrar_sesion.pack(side=tk.RIGHT, padx=10, pady=5)

        # Contenedor para las vistas
        self.view_container = tk.Frame(self.main_frame, bg=WHITE)
        self.view_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Vistas de la aplicación
        self.proyectos_view = tk.Frame(self.view_container, bg=WHITE)
        self.materiales_view = tk.Frame(self.view_container, bg=WHITE)
        self.areas_view = tk.Frame(self.view_container, bg=WHITE)
        
        self.create_proyectos_view()
        self.create_materiales_view()
        self.create_areas_view()

        # Mostrar la vista por defecto
        self.show_proyectos_view()
        
    def _hide_all_views(self):
        """Oculta todos los frames de vista."""
        self.proyectos_view.pack_forget()
        self.materiales_view.pack_forget()
        self.areas_view.pack_forget()

    def show_proyectos_view(self):
        self._hide_all_views()
        self.proyectos_view.pack(fill=tk.BOTH, expand=True)
        self.load_proyectos()

    def show_materiales_view(self):
        self._hide_all_views()
        self.materiales_view.pack(fill=tk.BOTH, expand=True)

    def show_areas_view(self):
        self._hide_all_views()
        self.areas_view.pack(fill=tk.BOTH, expand=True)
        
    def logout(self):
        """Cierra la sesión del usuario."""
        if messagebox.askyesno("Cerrar Sesión", "¿Estás seguro que quieres cerrar la sesión?"):
            self.supabase_client.auth.sign_out()
            self.master.destroy()
            
            # TODO: Reiniciar la app a la ventana de login
            
            messagebox.showinfo("Sesión Cerrada", "Has cerrado la sesión con éxito.")

    def create_proyectos_view(self):
        """Crea los widgets para la vista de proyectos."""
        title_label = tk.Label(self.proyectos_view, text="Proyectos", font=(FONT_PRIMARY, FONT_SIZE_LARGE, "bold"), fg=INDIGO_DYE, bg=WHITE)
        title_label.pack(pady=(0, 20))
        
        btn_crear_proyecto = tk.Button(self.proyectos_view, text="Crear Nuevo Proyecto", command=self.create_new_proyecto, **BUTTON_STYLE_SECONDARY)
        btn_crear_proyecto.pack(pady=(0, 20))
        
        self.proyectos_list_frame = tk.Frame(self.proyectos_view, bg=WHITE)
        self.proyectos_list_frame.pack(fill=tk.BOTH, expand=True)

    def create_materiales_view(self):
        """Crea los widgets para la vista de materiales."""
        title_label = tk.Label(self.materiales_view, text="Administración de Materiales", font=(FONT_PRIMARY, FONT_SIZE_LARGE, "bold"), fg=INDIGO_DYE, bg=WHITE)
        title_label.pack(pady=20)
        # Aquí irán los widgets para administrar materiales
        
    def create_areas_view(self):
        """Crea los widgets para la vista de áreas."""
        title_label = tk.Label(self.areas_view, text="Administración de Áreas", font=(FONT_PRIMARY, FONT_SIZE_LARGE, "bold"), fg=INDIGO_DYE, bg=WHITE)
        title_label.pack(pady=20)
        # Aquí irán los widgets para administrar áreas
        
    def load_proyectos(self):
        """Carga la lista de proyectos desde Supabase y la muestra."""
        # Limpiar la lista actual
        for widget in self.proyectos_list_frame.winfo_children():
            widget.destroy()

        try:
            # Consultar todos los proyectos
            response = self.supabase_client.table("proyectos").select("*").execute()
            proyectos = response.data
            
            if not proyectos:
                no_projects_label = tk.Label(self.proyectos_list_frame, text="No hay proyectos todavía.", font=(FONT_PRIMARY, FONT_SIZE_SMALL), fg=DARK_GRAY, bg=WHITE)
                no_projects_label.pack(pady=50)
            else:
                for proyecto in proyectos:
                    proyecto_frame = tk.Frame(self.proyectos_list_frame, bg=LIGHT_GRAY, padx=10, pady=10)
                    proyecto_frame.pack(fill=tk.X, pady=5)
                    
                    nombre_label = tk.Label(proyecto_frame, text=f"Proyecto: {proyecto['nombre_proyecto']}", font=(FONT_PRIMARY, FONT_SIZE_SMALL, "bold"), bg=LIGHT_GRAY)
                    nombre_label.pack(anchor='w')
                    
                    direccion_label = tk.Label(proyecto_frame, text=f"Dirección: {proyecto['direccion_proyecto']}", font=(FONT_PRIMARY, FONT_SIZE_SMALL), bg=LIGHT_GRAY)
                    direccion_label.pack(anchor='w')
                    
                    btn_abrir = tk.Button(proyecto_frame, text="Ver Detalles", command=lambda p=proyecto: self.open_proyecto(p), **BUTTON_STYLE_PRIMARY)
                    btn_abrir.pack(side=tk.RIGHT)
                    
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proyectos: {e}")

    def create_new_proyecto(self):
        # Esta es una función de marcador de posición para el próximo paso
        messagebox.showinfo("Crear Proyecto", "Aquí se abrirá la ventana o vista para crear un nuevo proyecto.")
        
    def open_proyecto(self, proyecto):
        # Esta es una función de marcador de posición para el próximo paso
        messagebox.showinfo("Abrir Proyecto", f"Abriendo los detalles del proyecto: {proyecto['nombre_proyecto']}")
