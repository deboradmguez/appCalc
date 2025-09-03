import tkinter as tk
from tkinter import messagebox, Listbox
from config import *

class ProyectoFormWindow(tk.Toplevel):
    def __init__(self, master, supabase_client, callback):
        super().__init__(master)
        self.supabase_client = supabase_client
        self.callback = callback
        self.areas_data = []

        # --- ESTILOS ACTUALIZADOS ---
        self.title("Crear Nuevo Proyecto")
        self.geometry("450x550")
        self.configure(bg=DARK_GRAY)
        self.transient(master)
        self.grab_set()

        title_label = tk.Label(self, text="Detalles del Nuevo Proyecto", font=(FONT_PRIMARY, FONT_SIZE_LARGE, "bold"), fg=NEAR_WHITE, bg=DARK_GRAY)
        title_label.pack(pady=20)

        form_frame = tk.Frame(self, bg=DARK_GRAY)
        form_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)

        tk.Label(form_frame, text="Nombre del Proyecto:", font=(FONT_PRIMARY, FONT_SIZE_NORMAL), fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(anchor='w')
        self.nombre_entry = tk.Entry(form_frame, **ENTRY_STYLE)
        self.nombre_entry.pack(fill=tk.X, pady=(0, 10), ipady=5)

        tk.Label(form_frame, text="Dirección:", font=(FONT_PRIMARY, FONT_SIZE_NORMAL), fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(anchor='w')
        self.direccion_entry = tk.Entry(form_frame, **ENTRY_STYLE)
        self.direccion_entry.pack(fill=tk.X, pady=(0, 20), ipady=5)

        tk.Label(form_frame, text="Seleccione las Áreas del Proyecto:", font=(FONT_PRIMARY, FONT_SIZE_NORMAL), fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(anchor='w')
        
        self.areas_listbox = Listbox(form_frame, selectmode=tk.MULTIPLE, **LISTBOX_STYLE)
        self.areas_listbox.pack(fill=tk.BOTH, expand=True, pady=(5,0))
        self.load_master_areas()

        button_frame = tk.Frame(self, bg=DARK_GRAY)
        button_frame.pack(pady=20, fill=tk.X, padx=30)

        btn_guardar = tk.Button(button_frame, text="Guardar Proyecto", command=self.save_proyecto, **BUTTON_STYLE_PRIMARY)
        btn_guardar.pack(side=tk.LEFT, expand=True, ipady=8, padx=(0,5))

        btn_cancelar = tk.Button(button_frame, text="Cancelar", command=self.destroy, **BUTTON_STYLE_SECONDARY)
        btn_cancelar.pack(side=tk.RIGHT, expand=True, ipady=8, padx=(5,0))

    # El resto de la clase (load_master_areas y save_proyecto) no cambia...
    def load_master_areas(self):
        try:
            response = self.supabase_client.table("areas_maestro").select("id_area_maestro, nombre_area").order("nombre_area").execute()
            self.areas_data = response.data
            for area in self.areas_data:
                self.areas_listbox.insert(tk.END, area['nombre_area'])
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar las áreas: {e}", parent=self)

    def save_proyecto(self):
        nombre = self.nombre_entry.get().strip()
        direccion = self.direccion_entry.get().strip()
        selected_indices = self.areas_listbox.curselection()

        if not nombre or not direccion or not selected_indices:
            messagebox.showwarning("Campos Incompletos", "Debe ingresar nombre, dirección y seleccionar al menos un área.", parent=self)
            return

        try:
            proyecto_response = self.supabase_client.table("proyectos").insert({
                "nombre_proyecto": nombre,
                "direccion_proyecto": direccion
            }).execute()
            nuevo_proyecto_id = proyecto_response.data[0]['id_proyecto']

            areas_to_link = []
            for index in selected_indices:
                selected_area_id = self.areas_data[index]['id_area_maestro']
                areas_to_link.append({
                    "proyecto_id": nuevo_proyecto_id,
                    "area_maestro_id": selected_area_id
                })
            
            self.supabase_client.table("proyectos_areas").insert(areas_to_link).execute()

            messagebox.showinfo("Éxito", "Proyecto creado correctamente.", parent=self)
            self.callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudo guardar el proyecto: {e}", parent=self)