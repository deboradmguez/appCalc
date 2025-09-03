import customtkinter as ctk
from tkinter import messagebox
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))
from config import *

class ProjectDetailPage(ctk.CTkFrame):
    def __init__(self, master, supabase_client, proyecto, on_back):
        super().__init__(master, fg_color=DARK_GRAY)
        self.supabase_client = supabase_client
        self.proyecto = proyecto
        self.on_back = on_back
        self.build_ui()

    def build_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=30, pady=(20,10))
        back_btn = ctk.CTkButton(header_frame, text="< Volver", command=self.on_back, width=100)
        back_btn.pack(side="left")
        ctk.CTkLabel(header_frame, text=self.proyecto['nombre_proyecto'], font=(FONT_PRIMARY, FONT_SIZE_TITLE, "bold")).pack(side="left", padx=20)
        
        container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=30, pady=10)

        try:
            project_areas = self.supabase_client.table("proyectos_areas").select("*, areas_maestro(nombre_area), puertas(count), ventanas(count)").eq("proyecto_id", self.proyecto['id_proyecto']).execute().data
            self.create_header_row(container)
            if not project_areas:
                ctk.CTkLabel(container, text="Este proyecto no tiene áreas asignadas.").pack(pady=20)
            else:
                for area_data in project_areas:
                    self.create_area_row(container, area_data)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las áreas: {e}")

    def create_header_row(self, parent):
        frame = ctk.CTkFrame(parent, fg_color=GRAPHITE, height=30)
        frame.pack(fill="x", expand=True, pady=(0,5))
        headers = ["Área", "Ancho (m)", "Largo (m)", "Alto (m)", "Puertas", "Ventanas", "Acciones"]
        weights = [3, 1, 1, 1, 1, 1, 2]
        for i, header in enumerate(headers):
            frame.columnconfigure(i, weight=weights[i])
            ctk.CTkLabel(frame, text=header, font=(FONT_PRIMARY, FONT_SIZE_SMALL, "bold"), text_color=LIGHT_GRAY_TEXT).grid(row=0, column=i, sticky="w", padx=10)

    def create_area_row(self, parent, area_data):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.pack(fill="x", expand=True, pady=4)
        weights = [3, 1, 1, 1, 1, 1, 2]
        for i in range(len(weights)): frame.columnconfigure(i, weight=weights[i])
        ctk.CTkLabel(frame, text=area_data['areas_maestro']['nombre_area']).grid(row=0, column=0, sticky="w", padx=10)
        ancho_var = ctk.StringVar(value=area_data.get('ancho', 0)); largo_var = ctk.StringVar(value=area_data.get('largo', 0)); alto_var = ctk.StringVar(value=area_data.get('alto', 0))
        ctk.CTkEntry(frame, textvariable=ancho_var, width=80).grid(row=0, column=1, sticky="w")
        ctk.CTkEntry(frame, textvariable=largo_var, width=80).grid(row=0, column=2, sticky="w")
        ctk.CTkEntry(frame, textvariable=alto_var, width=80).grid(row=0, column=3, sticky="w")
        num_puertas = area_data['puertas'][0]['count'] if area_data['puertas'] else 0
        num_ventanas = area_data['ventanas'][0]['count'] if area_data['ventanas'] else 0
        ctk.CTkLabel(frame, text=f"{num_puertas} Uds.").grid(row=0, column=4, sticky="w", padx=10)
        ctk.CTkLabel(frame, text=f"{num_ventanas} Uds.").grid(row=0, column=5, sticky="w", padx=10)
        save_btn = ctk.CTkButton(frame, text="Guardar", width=80, command=lambda: self.save_area_dimensions(area_data['id_proyectos_areas'], ancho_var, largo_var, alto_var))
        save_btn.grid(row=0, column=6, sticky="e", padx=10)

    def save_area_dimensions(self, area_id, ancho_var, largo_var, alto_var):
        try:
            update_data = {"ancho": float(ancho_var.get()), "largo": float(largo_var.get()), "alto": float(alto_var.get())}
            self.supabase_client.table("proyectos_areas").update(update_data).eq("id_proyectos_areas", area_id).execute()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar las dimensiones: {e}")