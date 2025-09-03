import tkinter as tk
from tkinter import ttk, messagebox
# --- BLOQUE DE IMPORTACIÓN (Asegúrate de tenerlo) ---
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))
from config import *
# ------------------------------------

class ProjectDetailPage(tk.Frame):
    def __init__(self, master, supabase_client, proyecto, on_back):
        super().__init__(master, bg=DARK_GRAY)
        self.supabase_client = supabase_client
        self.proyecto = proyecto
        self.on_back = on_back

        self.build_ui()

    def build_ui(self):
        # Header (sin cambios)
        header_frame = tk.Frame(self, bg=DARK_GRAY)
        header_frame.pack(fill=tk.X, padx=30, pady=(20,10))
        back_btn = tk.Button(header_frame, text="< Volver a la Lista", command=self.on_back, **BUTTON_STYLE_SECONDARY)
        back_btn.pack(side=tk.LEFT, ipady=4, ipadx=8)
        tk.Label(header_frame, text=self.proyecto['nombre_proyecto'], font=(FONT_PRIMARY, FONT_SIZE_TITLE, "bold"), fg=NEAR_WHITE, bg=DARK_GRAY).pack(side=tk.LEFT, padx=20)
        
        # Contenedor con Scrollbar (sin cambios)
        canvas_container = tk.Frame(self, bg=DARK_GRAY)
        canvas_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        canvas = tk.Canvas(canvas_container, bg=DARK_GRAY, highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        content_frame = tk.Frame(canvas, bg=DARK_GRAY)
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        try:
            # --- CONSULTA ÚNICA Y OPTIMIZADA ---
            # Pedimos las áreas, el nombre del área maestra relacionada,
            # y el CONTEO de puertas y ventanas relacionadas, todo en una sola llamada.
            project_areas = self.supabase_client.table("proyectos_areas").select(
                "*, areas_maestro(nombre_area), puertas(count), ventanas(count)"
            ).eq("proyecto_id", self.proyecto['id_proyecto']).execute().data
            
            self.create_header_row(content_frame)

            if not project_areas:
                tk.Label(content_frame, text="Este proyecto no tiene áreas asignadas.", fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(pady=20)
            else:
                for area_data in project_areas:
                    # Ahora area_data ya contiene los conteos, no hay que volver a consultar.
                    self.create_area_row(content_frame, area_data)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las áreas del proyecto: {e}")

    def create_header_row(self, parent):
        # ... (sin cambios)
        header_frame = tk.Frame(parent, bg=GRAPHITE, padx=10, pady=5)
        header_frame.pack(fill=tk.X, expand=True, pady=(0,5))
        headers = ["Área", "Ancho (m)", "Largo (m)", "Alto (m)", "Puertas", "Ventanas", "Acciones"]
        weights = [3, 1, 1, 1, 2, 2, 1]
        for i, header in enumerate(headers):
            header_frame.columnconfigure(i, weight=weights[i])
            lbl = tk.Label(header_frame, text=header, font=(FONT_PRIMARY, FONT_SIZE_SMALL, "bold"), fg=NEAR_WHITE, bg=GRAPHITE)
            lbl.grid(row=0, column=i, sticky="w")

    def create_area_row(self, parent, area_data):
        row_frame = tk.Frame(parent, bg=DARK_GRAY, padx=10, pady=10)
        row_frame.pack(fill=tk.X, expand=True)
        weights = [3, 1, 1, 1, 2, 2, 1]
        for i in range(len(weights)): row_frame.columnconfigure(i, weight=weights[i])

        tk.Label(row_frame, text=area_data['areas_maestro']['nombre_area'], fg=NEAR_WHITE, bg=DARK_GRAY).grid(row=0, column=0, sticky="w")

        ancho_var = tk.DoubleVar(value=area_data.get('ancho', 0)); largo_var = tk.DoubleVar(value=area_data.get('largo', 0)); alto_var = tk.DoubleVar(value=area_data.get('alto', 0))
        
        tk.Entry(row_frame, textvariable=ancho_var, **ENTRY_STYLE, width=10).grid(row=0, column=1, sticky="w")
        tk.Entry(row_frame, textvariable=largo_var, **ENTRY_STYLE, width=10).grid(row=0, column=2, sticky="w")
        tk.Entry(row_frame, textvariable=alto_var, **ENTRY_STYLE, width=10).grid(row=0, column=3, sticky="w")
        
        # --- LECTURA DE DATOS OPTIMIZADA ---
        # Leemos los conteos que ya vinieron en la consulta principal.
        # Supabase devuelve el conteo en una lista, por eso accedemos al primer elemento.
        num_puertas = area_data['puertas'][0]['count'] if area_data['puertas'] else 0
        num_ventanas = area_data['ventanas'][0]['count'] if area_data['ventanas'] else 0
        
        tk.Label(row_frame, text=f"{num_puertas} Uds.", fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).grid(row=0, column=4, sticky="w")
        tk.Label(row_frame, text=f"{num_ventanas} Uds.", fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).grid(row=0, column=5, sticky="w")

        save_btn = tk.Button(row_frame, text="Guardar", **BUTTON_STYLE_SECONDARY,
                             command=lambda: self.save_area_dimensions(area_data['id_proyectos_areas'], ancho_var, largo_var, alto_var))
        save_btn.grid(row=0, column=6, sticky="e", ipady=2, ipadx=5)

    def save_area_dimensions(self, area_id, ancho_var, largo_var, alto_var):
        # ... (sin cambios)
        try:
            update_data = {"ancho": ancho_var.get(), "largo": largo_var.get(), "alto": alto_var.get()}
            self.supabase_client.table("proyectos_areas").update(update_data).eq("id_proyectos_areas", area_id).execute()
            messagebox.showinfo("Éxito", "Dimensiones guardadas.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar las dimensiones: {e}")