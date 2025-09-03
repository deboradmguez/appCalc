import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, simpledialog

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))
from config import *

class AreasView(ctk.CTkFrame):
    def __init__(self, master, supabase_client):
        super().__init__(master, fg_color=DARK_GRAY)
        self.supabase_client = supabase_client
        self.master_areas_data = []
        self._build_ui()
        self.load_master_areas()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Administración de Áreas", font=(FONT_PRIMARY, FONT_SIZE_TITLE, "bold")).pack(pady=30, padx=30, anchor="w")
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=(0,20))
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        list_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        ctk.CTkLabel(list_frame, text="Áreas existentes:", font=(FONT_PRIMARY, FONT_SIZE_NORMAL), text_color=LIGHT_GRAY_TEXT).pack(anchor='w')
        self.master_areas_listbox = tk.Listbox(list_frame, **LISTBOX_STYLE)
        self.master_areas_listbox.pack(fill="both", expand=True, pady=(5,0))
        
        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        form_frame.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(form_frame, text="Nueva Área:", text_color=LIGHT_GRAY_TEXT).pack(anchor='w')
        self.new_area_entry = ctk.CTkEntry(form_frame, height=40)
        self.new_area_entry.pack(fill="x", pady=(5,0))
        ctk.CTkButton(form_frame, text="Añadir Área", command=self.add_area, height=40).pack(fill="x", pady=(10, 20))
        ctk.CTkButton(form_frame, text="Editar Seleccionada", command=self.update_selected_area, fg_color=DARK_GRAY, border_width=1, border_color=MEDIUM_GRAY).pack(fill="x")
        ctk.CTkButton(form_frame, text="Eliminar Seleccionada", command=self.delete_selected_area, fg_color=DARK_GRAY, hover_color=ERROR_COLOR, border_width=1, border_color=MEDIUM_GRAY).pack(fill="x", pady=5)
    
    def load_master_areas(self):
        # ... (La lógica no cambia)
        self.master_areas_listbox.delete(0, tk.END)
        try:
            self.master_areas_data = self.supabase_client.table("areas_maestro").select("*").order("nombre_area").execute().data
            for area in self.master_areas_data: self.master_areas_listbox.insert(tk.END, area['nombre_area'])
        except Exception as e: messagebox.showerror("Error", f"No se pudo cargar: {e}")
    def add_area(self):
        # ... (La lógica no cambia)
        new_name = self.new_area_entry.get().strip()
        if not new_name: return
        try:
            self.supabase_client.table("areas_maestro").insert({"nombre_area": new_name}).execute()
            self.new_area_entry.delete(0, tk.END); self.load_master_areas()
        except Exception as e: messagebox.showerror("Error", f"No se pudo añadir: {e}")
    def update_selected_area(self):
        # ... (La lógica no cambia, solo el 'parent' del simpledialog)
        selected_indices = self.master_areas_listbox.curselection()
        if not selected_indices: return
        area_id = self.master_areas_data[selected_indices[0]]['id_area_maestro']
        old_name = self.master_areas_data[selected_indices[0]]['nombre_area']
        dialog = ctk.CTkInputDialog(text="Nuevo nombre:", title="Editar Área")
        new_name = dialog.get_input()
        if new_name and new_name.strip() != old_name:
            try:
                self.supabase_client.table("areas_maestro").update({"nombre_area": new_name.strip()}).eq("id_area_maestro", area_id).execute()
                self.load_master_areas()
            except Exception as e: messagebox.showerror("Error", f"No se pudo actualizar: {e}")
    def delete_selected_area(self):
        # ... (La lógica no cambia)
        selected_indices = self.master_areas_listbox.curselection()
        if not selected_indices: return
        area_id = self.master_areas_data[selected_indices[0]]['id_area_maestro']
        area_name = self.master_areas_data[selected_indices[0]]['nombre_area']
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{area_name}'?"):
            try:
                self.supabase_client.table("areas_maestro").delete().eq("id_area_maestro", area_id).execute()
                self.load_master_areas()
            except Exception as e: messagebox.showerror("Error", f"No se pudo eliminar: {e}")
