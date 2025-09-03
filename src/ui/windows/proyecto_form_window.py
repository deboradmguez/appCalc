import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from config import *

class ProyectoFormWindow(ctk.CTkToplevel):
    def __init__(self, master, supabase_client, callback):
        super().__init__(master)
        self.supabase_client = supabase_client
        self.callback = callback
        self.areas_data = []

        self.title("Crear Nuevo Proyecto")
        self.geometry("450x550")
        self.transient(master)
        self.grab_set()

        ctk.CTkLabel(self, text="Detalles del Nuevo Proyecto", font=(FONT_PRIMARY, FONT_SIZE_LARGE, "bold")).pack(pady=20)
        
        ctk.CTkLabel(self, text="Nombre del Proyecto:").pack(anchor="w", padx=30)
        self.nombre_entry = ctk.CTkEntry(self, height=40); self.nombre_entry.pack(fill="x", padx=30, pady=(0, 10))
        ctk.CTkLabel(self, text="Dirección:").pack(anchor="w", padx=30)
        self.direccion_entry = ctk.CTkEntry(self, height=40); self.direccion_entry.pack(fill="x", padx=30, pady=(0, 20))
        ctk.CTkLabel(self, text="Seleccione las Áreas:").pack(anchor="w", padx=30)
        
        self.areas_listbox = tk.Listbox(self, selectmode="multiple", **LISTBOX_STYLE); self.areas_listbox.pack(fill="both", expand=True, padx=30, pady=(0,20))
        self.load_master_areas()

        btn_container = ctk.CTkFrame(self, fg_color="transparent"); btn_container.pack(fill="x", padx=30, pady=(0,20))
        ctk.CTkButton(btn_container, text="Cancelar", command=self.destroy).pack(side="left", expand=True, padx=(0,5))
        ctk.CTkButton(btn_container, text="Guardar Proyecto", command=self.save_proyecto).pack(side="left", expand=True, padx=(5,0))

    def load_master_areas(self):
        try:
            self.areas_data = self.supabase_client.table("areas_maestro").select("id_area_maestro, nombre_area").order("nombre_area").execute().data
            for area in self.areas_data: self.areas_listbox.insert(tk.END, area['nombre_area'])
        except Exception as e: messagebox.showerror("Error", f"No se pudieron cargar las áreas: {e}", parent=self)

    def save_proyecto(self):
        nombre=self.nombre_entry.get().strip(); direccion=self.direccion_entry.get().strip(); selected_indices = self.areas_listbox.curselection()
        if not nombre or not direccion or not selected_indices: messagebox.showwarning("Info", "Debe ingresar nombre, dirección y seleccionar al menos un área.", parent=self); return
        try:
            proyecto_response = self.supabase_client.table("proyectos").insert({"nombre_proyecto": nombre, "direccion_proyecto": direccion}).execute().data
            nuevo_proyecto_id = proyecto_response[0]['id_proyecto']
            areas_to_link = []
            for index in selected_indices:
                areas_to_link.append({"proyecto_id": nuevo_proyecto_id, "area_maestro_id": self.areas_data[index]['id_area_maestro']})
            self.supabase_client.table("proyectos_areas").insert(areas_to_link).execute()
            self.callback(); self.destroy()
        except Exception as e: messagebox.showerror("Error", f"No se pudo guardar: {e}", parent=self)