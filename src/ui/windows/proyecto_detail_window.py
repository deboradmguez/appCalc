import tkinter as tk
from tkinter import ttk, messagebox
from config import *

class ProyectoDetailWindow(tk.Toplevel):
    def __init__(self, master, supabase_client, proyecto):
        super().__init__(master)
        self.supabase_client = supabase_client
        self.proyecto = proyecto

        # --- ESTILOS ACTUALIZADOS ---
        self.title(f"Detalles de: {proyecto['nombre_proyecto']}")
        self.geometry("800x600")
        self.configure(bg=DARK_GRAY)
        self.transient(master)
        self.grab_set()
        
        info_frame = tk.Frame(self, bg=GRAPHITE, padx=20, pady=15)
        info_frame.pack(fill=tk.X, side=tk.TOP)
        tk.Label(info_frame, text=f"Proyecto: {proyecto['nombre_proyecto']}", font=(FONT_PRIMARY, FONT_SIZE_LARGE, "bold"), bg=GRAPHITE, fg=NEAR_WHITE).pack(anchor='w')
        tk.Label(info_frame, text=f"Dirección: {proyecto['direccion_proyecto']}", font=(FONT_PRIMARY, FONT_SIZE_NORMAL), bg=GRAPHITE, fg=LIGHT_GRAY_TEXT).pack(anchor='w')

        # --- Estilo personalizado para las pestañas (ttk.Notebook) ---
        style = ttk.Style(self)
        style.theme_use('default')
        style.configure('TNotebook', background=DARK_GRAY, borderwidth=0)
        style.configure('TNotebook.Tab', background=GRAPHITE, foreground=LIGHT_GRAY_TEXT, padding=[10, 8], borderwidth=0, font=(FONT_PRIMARY, FONT_SIZE_SMALL, 'bold'))
        style.map('TNotebook.Tab', background=[('selected', DARK_GRAY)], foreground=[('selected', ACCENT_CYAN)])

        self.notebook = ttk.Notebook(self, style='TNotebook')
        self.notebook.pack(pady=20, padx=20, fill="both", expand=True)

        self.load_project_areas()

    def load_project_areas(self):
        try:
            response = self.supabase_client.table("proyectos_areas").select(
                "*, areas_maestro(nombre_area)"
            ).eq("proyecto_id", self.proyecto['id_proyecto']).execute()
            
            project_areas = response.data
            if not project_areas:
                # Frame para el mensaje para poder centrarlo y estilizarlo
                msg_frame = tk.Frame(self.notebook, bg=DARK_GRAY)
                tk.Label(msg_frame, text="Este proyecto no tiene áreas asignadas.", fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(pady=50)
                self.notebook.add(msg_frame, text="Info")
                return

            for area_data in project_areas:
                area_name = area_data['areas_maestro']['nombre_area']
                
                tab_frame = tk.Frame(self.notebook, bg=DARK_GRAY, padx=20, pady=20)
                self.notebook.add(tab_frame, text=area_name.upper())
                
                tk.Label(tab_frame, text=f"Datos para el área: {area_name}", font=(FONT_PRIMARY, FONT_SIZE_NORMAL, "bold"), fg=NEAR_WHITE, bg=DARK_GRAY).pack(anchor='w', pady=(0,20))
                
                ancho_var = tk.DoubleVar(value=area_data.get('ancho', 0.0))
                largo_var = tk.DoubleVar(value=area_data.get('largo', 0.0))
                alto_var = tk.DoubleVar(value=area_data.get('alto', 0.0))
                
                # Campos de entrada
                tk.Label(tab_frame, text="Ancho (m):", fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(anchor='w')
                tk.Entry(tab_frame, textvariable=ancho_var, **ENTRY_STYLE).pack(fill=tk.X, pady=(0,10), ipady=5)
                
                tk.Label(tab_frame, text="Largo (m):", fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(anchor='w')
                tk.Entry(tab_frame, textvariable=largo_var, **ENTRY_STYLE).pack(fill=tk.X, pady=(0,10), ipady=5)

                tk.Label(tab_frame, text="Alto (m):", fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(anchor='w')
                tk.Entry(tab_frame, textvariable=alto_var, **ENTRY_STYLE).pack(fill=tk.X, pady=(0,10), ipady=5)
                
                # Frame para botones
                button_frame_details = tk.Frame(tab_frame, bg=DARK_GRAY)
                button_frame_details.pack(fill=tk.X, pady=20)

                tk.Button(button_frame_details, text="Guardar Medidas", **BUTTON_STYLE_SECONDARY).pack(side=tk.LEFT, ipady=8, ipadx=10)
                tk.Button(button_frame_details, text="Calcular Materiales", **BUTTON_STYLE_PRIMARY).pack(side=tk.RIGHT, ipady=8, ipadx=10)

        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las áreas del proyecto: {e}", parent=self)