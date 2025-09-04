import customtkinter as ctk
from tkinter import messagebox
from config import * # Solo para los tamaños

class ProyectoFormWindow(ctk.CTkToplevel):
    def __init__(self, master, callback, **kwargs):
        super().__init__(master, **kwargs)
        
        self.supabase_client = master.supabase_client
        self.callback = callback
        self.areas_data = []
        self.area_checkboxes = []

        self.title("Crear Nuevo Proyecto")
        alto, ancho = 600, 500
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry(f"{ancho}x{alto}+{x}+{y}")
        self.transient(master)

        # --- CORRECCIÓN DE FUENTE ---
        title_label = ctk.CTkLabel(self, text="Detalles del Nuevo Proyecto", font=ctk.CTkFont(size=FONT_SIZE_LARGE, weight="bold"))
        title_label.pack(pady=20, padx=30)

        form_frame = ctk.CTkFrame(self, fg_color="transparent")
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        ctk.CTkLabel(form_frame, text="Nombre del Proyecto:").pack(anchor='w')
        self.nombre_entry = ctk.CTkEntry(form_frame, height=40)
        self.nombre_entry.pack(fill="x", pady=(0, 15))

        ctk.CTkLabel(form_frame, text="Dirección:").pack(anchor='w')
        self.direccion_entry = ctk.CTkEntry(form_frame, height=40)
        self.direccion_entry.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(form_frame, text="Seleccione las Áreas del Proyecto:").pack(anchor='w')
        
        self.areas_scrollable_frame = ctk.CTkScrollableFrame(form_frame, label_text="")
        self.areas_scrollable_frame.pack(fill="both", expand=True, pady=5)
        self.load_master_areas()

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack(pady=20, fill="x", padx=30)
        button_frame.grid_columnconfigure((0, 1), weight=1)

        btn_guardar = ctk.CTkButton(button_frame, text="Guardar Proyecto", command=self.save_proyecto, height=40)
        btn_guardar.grid(row=0, column=0, sticky="ew", padx=(0,5))

        btn_cancelar = ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy, fg_color="gray", height=40)
        btn_cancelar.grid(row=0, column=1, sticky="ew", padx=(5,0))

    def load_master_areas(self):
        try:
            response = self.supabase_client.table("areas_maestro").select("id_area_maestro, nombre_area").order("nombre_area").execute()
            self.areas_data = response.data
            
            for area in self.areas_data:
                checkbox = ctk.CTkCheckBox(self.areas_scrollable_frame, text=area['nombre_area'])
                checkbox.pack(anchor="w", padx=10, pady=5)
                self.area_checkboxes.append(checkbox)
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar las áreas: {e}", parent=self)

    def save_proyecto(self):
        nombre = self.nombre_entry.get().strip()
        direccion = self.direccion_entry.get().strip()
        selected_indices = [i for i, checkbox in enumerate(self.area_checkboxes) if checkbox.get() == 1]

        if not nombre or not direccion or not selected_indices:
            messagebox.showwarning("Campos Incompletos", "Debe ingresar nombre, dirección y seleccionar al menos un área.", parent=self)
            return

        try:
            proyecto_response = self.supabase_client.table("proyectos").insert({
                "nombre_proyecto": nombre,
                "direccion_proyecto": direccion
            }).execute()
            nuevo_proyecto_id = proyecto_response.data[0]['id_proyecto']
            areas_to_link = [{"proyecto_id": nuevo_proyecto_id, "area_maestro_id": self.areas_data[index]['id_area_maestro']} for index in selected_indices]
            
            if areas_to_link:
                self.supabase_client.table("proyectos_areas").insert(areas_to_link).execute()

            messagebox.showinfo("Éxito", "Proyecto creado correctamente.", parent=self)
            self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudo guardar el proyecto: {e}", parent=self)