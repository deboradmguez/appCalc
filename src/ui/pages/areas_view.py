import customtkinter as ctk
from tkinter import messagebox

class AreasView(ctk.CTkFrame):
    def __init__(self, master, master_app, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.supabase_client = master_app.supabase_client
        self.master_areas_data = []
        
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self, text="Administración de Áreas Maestras", font=("", 22, "bold")).grid(row=0, column=0, columnspan=2, pady=20, padx=10, sticky="w")
        
        # Columna Izquierda: Lista
        list_frame = ctk.CTkFrame(self, fg_color="transparent")
        list_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5))
        self.areas_list = ctk.CTkScrollableFrame(list_frame, label_text="Áreas existentes")
        self.areas_list.pack(fill="both", expand=True)
        
        # Columna Derecha: Formulario
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10))
        ctk.CTkLabel(form_frame, text="Nueva Área:").pack(anchor='w', padx=15, pady=(15,5))
        self.new_area_entry = ctk.CTkEntry(form_frame, height=40)
        self.new_area_entry.pack(fill="x", padx=15, pady=(0,10))
        ctk.CTkButton(form_frame, text="Añadir Área", command=self.add_area, height=40).pack(fill="x", padx=15)
        ctk.CTkButton(form_frame, text="Editar Seleccionada", command=self.update_selected_area, fg_color="transparent", border_width=1).pack(fill="x", padx=15, pady=(20, 5))
        ctk.CTkButton(form_frame, text="Eliminar Seleccionada", command=self.delete_selected_area, fg_color="transparent", hover_color="#C11B17", border_width=1).pack(fill="x", padx=15)

        self.load_master_areas()

    def load_master_areas(self):
        for widget in self.areas_list.winfo_children(): widget.destroy()
        try:
            self.master_areas_data = self.supabase_client.table("areas_maestro").select("*").order("nombre_area").execute().data
            for area in self.master_areas_data: 
                ctk.CTkLabel(self.areas_list, text=area['nombre_area'], padx=10).pack(anchor="w", fill="x")
        except Exception as e: messagebox.showerror("Error", f"No se pudo cargar: {e}")

    def add_area(self):
        new_name = self.new_area_entry.get().strip()
        if not new_name: return
        try:
            self.supabase_client.table("areas_maestro").insert({"nombre_area": new_name}).execute()
            self.new_area_entry.delete(0, "end"); self.load_master_areas()
        except Exception as e: messagebox.showerror("Error", f"No se pudo añadir: {e}")

    def delete_selected_area(self):
        # Esta funcionalidad requiere seleccionar un item, lo cual es más complejo
        # con labels. Se recomienda un widget de lista personalizado para esto.
        messagebox.showinfo("Info", "La edición y eliminación requieren un componente de lista más avanzado.")
    
    def update_selected_area(self):
        messagebox.showinfo("Info", "La edición y eliminación requieren un componente de lista más avanzado.")