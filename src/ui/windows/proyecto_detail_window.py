# proyecto_detail_window.py (Refactored for CustomTkinter)

import customtkinter as ctk
from tkinter import messagebox
# Ya no necesitamos la configuración de colores manual
# from config import *

class ProyectoDetailWindow(ctk.CTkToplevel):
    def __init__(self, master, supabase_client, proyecto):
        super().__init__(master)
        self.supabase_client = supabase_client
        self.proyecto = proyecto

        self.title(f"Detalles de: {proyecto['nombre_proyecto']}")
        self.geometry("800x600")
        self.transient(master)
        self.grab_set()

        # --- Contenedor principal con grid para mejor distribución ---
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # --- Frame de Información Superior (CTkFrame) ---
        info_frame = ctk.CTkFrame(self, corner_radius=0)
        info_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 0))

        ctk.CTkLabel(info_frame, text=f"Proyecto: {proyecto['nombre_proyecto']}", 
                     font=ctk.CTkFont(size=20, weight="bold")).pack(anchor='w', padx=10, pady=(5,0))
        ctk.CTkLabel(info_frame, text=f"Dirección: {proyecto['direccion_proyecto']}",
                     font=ctk.CTkFont(size=14)).pack(anchor='w', padx=10, pady=(0,5))

        # --- Reemplazo de ttk.Notebook con ctk.CTkTabview ---
        self.tab_view = ctk.CTkTabview(self, corner_radius=8)
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        self.load_project_areas()

    def load_project_areas(self):
        try:
            response = self.supabase_client.table("proyectos_areas").select(
                "*, areas_maestro(nombre_area)"
            ).eq("proyecto_id", self.proyecto['id_proyecto']).execute()
            
            project_areas = response.data
            if not project_areas:
                # Añadir una pestaña de información si no hay áreas
                info_tab = self.tab_view.add("Info")
                ctk.CTkLabel(info_tab, text="Este proyecto no tiene áreas asignadas.").pack(expand=True)
                return

            for area_data in project_areas:
                area_name = area_data['areas_maestro']['nombre_area']
                
                # --- Crear una nueva pestaña para cada área ---
                tab = self.tab_view.add(area_name.upper())
                
                # --- Configurar grid para la pestaña ---
                tab.grid_columnconfigure(0, weight=1)
                
                # --- Campos de entrada (CTkEntry) ---
                ctk.CTkLabel(tab, text="Ancho (m):").grid(row=0, column=0, sticky="w", padx=10, pady=(10,0))
                ancho_var = ctk.StringVar(value=str(area_data.get('ancho', 0.0)))
                ctk.CTkEntry(tab, textvariable=ancho_var).grid(row=1, column=0, sticky="ew", padx=10, pady=(0,10))
                
                ctk.CTkLabel(tab, text="Largo (m):").grid(row=2, column=0, sticky="w", padx=10)
                largo_var = ctk.StringVar(value=str(area_data.get('largo', 0.0)))
                ctk.CTkEntry(tab, textvariable=largo_var).grid(row=3, column=0, sticky="ew", padx=10, pady=(0,10))

                ctk.CTkLabel(tab, text="Alto (m):").grid(row=4, column=0, sticky="w", padx=10)
                alto_var = ctk.StringVar(value=str(area_data.get('alto', 0.0)))
                ctk.CTkEntry(tab, textvariable=alto_var).grid(row=5, column=0, sticky="ew", padx=10, pady=(0,20))
                
                # --- Frame para botones (CTkFrame) ---
                button_frame = ctk.CTkFrame(tab, fg_color="transparent")
                button_frame.grid(row=6, column=0, sticky="ew", padx=10)
                button_frame.grid_columnconfigure((0, 1), weight=1)

                # --- Botones (CTkButton) ---
                ctk.CTkButton(button_frame, text="Guardar Medidas", fg_color="gray").grid(row=0, column=0, padx=(0,5))
                ctk.CTkButton(button_frame, text="Calcular Materiales").grid(row=0, column=1, padx=(5,0))

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las áreas del proyecto: {e}", parent=self)