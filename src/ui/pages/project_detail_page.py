import customtkinter as ctk
from tkinter import messagebox

class ProjectDetailPage(ctk.CTkFrame):
    def __init__(self, master, master_app, proyecto, on_back, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.supabase_client = master_app.supabase_client
        self.proyecto = proyecto
        self.on_back = on_back

        self.build_ui()

    def build_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=10)
        ctk.CTkButton(header_frame, text="< Volver a la Lista", command=self.on_back, width=120).pack(side="left")
        ctk.CTkLabel(header_frame, text=self.proyecto['nombre_proyecto'], font=("", 22, "bold")).pack(side="left", padx=20)
        
        scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scrollable_frame.pack(fill="both", expand=True, padx=10, pady=10)

        try:
            project_areas = self.supabase_client.table("proyectos_areas").select(
                "*, areas_maestro(nombre_area)"
            ).eq("proyecto_id", self.proyecto['id_proyecto']).execute().data
            
            self.create_header_row(scrollable_frame)

            if not project_areas:
                ctk.CTkLabel(scrollable_frame, text="Este proyecto no tiene áreas asignadas.").pack(pady=20)
            else:
                for area_data in project_areas:
                    self.create_area_row(scrollable_frame, area_data)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las áreas del proyecto: {e}")

    def create_header_row(self, parent):
        header = ctk.CTkFrame(parent, fg_color=("#dbdbdb", "#2b2b2b"))
        header.pack(fill="x", expand=True, pady=(0,5))
        headers = ["Área", "Ancho (m)", "Largo (m)", "Alto (m)", "Acciones"]
        weights = [4, 1, 1, 1, 1]
        for i, h_text in enumerate(headers):
            header.grid_columnconfigure(i, weight=weights[i])
            ctk.CTkLabel(header, text=h_text, font=("", 12, "bold")).grid(row=0, column=i, sticky="w", padx=10, pady=5)

    def create_area_row(self, parent, area_data):
        row_frame = ctk.CTkFrame(parent)
        row_frame.pack(fill="x", expand=True, pady=3)
        weights = [4, 1, 1, 1, 1]
        for i in range(len(weights)): row_frame.grid_columnconfigure(i, weight=weights[i])

        ctk.CTkLabel(row_frame, text=area_data['areas_maestro']['nombre_area']).grid(row=0, column=0, sticky="w", padx=10)
        
        ancho_var = ctk.StringVar(value=str(area_data.get('ancho', 0)))
        largo_var = ctk.StringVar(value=str(area_data.get('largo', 0)))
        alto_var = ctk.StringVar(value=str(area_data.get('alto', 0)))
        
        ctk.CTkEntry(row_frame, textvariable=ancho_var, width=100).grid(row=0, column=1, sticky="w")
        ctk.CTkEntry(row_frame, textvariable=largo_var, width=100).grid(row=0, column=2, sticky="w")
        ctk.CTkEntry(row_frame, textvariable=alto_var, width=100).grid(row=0, column=3, sticky="w")
        
        save_btn = ctk.CTkButton(row_frame, text="Guardar", width=80,
                                command=lambda: self.save_area_dimensions(area_data['id_proyectos_areas'], ancho_var, largo_var, alto_var))
        save_btn.grid(row=0, column=4, sticky="e", padx=10)

    def save_area_dimensions(self, area_id, ancho_var, largo_var, alto_var):
        try:
            update_data = {"ancho": float(ancho_var.get()), "largo": float(largo_var.get()), "alto": float(alto_var.get())}
            self.supabase_client.table("proyectos_areas").update(update_data).eq("id_proyectos_areas", area_id).execute()
            messagebox.showinfo("Éxito", "Dimensiones guardadas.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar las dimensiones: {e}")