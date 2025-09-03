import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import json
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))
from config import *

class MaterialesView(ctk.CTkFrame):
    def __init__(self, master, supabase_client):
        super().__init__(master, fg_color=DARK_GRAY)
        self.supabase_client = supabase_client
        self.materials_data = []; self.material_types = []; self.selected_material_id = None; self.dynamic_entries = {}
        self._build_ui()
        self.load_materials(); self.load_material_types()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Administración de Materiales", font=(FONT_PRIMARY, FONT_SIZE_TITLE, "bold")).pack(pady=30, padx=30, anchor="w")
        main_frame = ctk.CTkFrame(self, fg_color="transparent"); main_frame.pack(fill="both", expand=True, padx=30, pady=(0,20))
        main_frame.grid_columnconfigure(0, weight=1); main_frame.grid_columnconfigure(1, weight=2); main_frame.grid_rowconfigure(0, weight=1)
        
        list_frame = ctk.CTkFrame(main_frame, fg_color="transparent"); list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 20))
        ctk.CTkLabel(list_frame, text="Materiales:", text_color=LIGHT_GRAY_TEXT).pack(anchor='w')
        self.materials_listbox = tk.Listbox(list_frame, **LISTBOX_STYLE); self.materials_listbox.pack(fill="both", expand=True, pady=(5,0))
        self.materials_listbox.bind("<<ListboxSelect>>", self._on_material_select)

        form_frame = ctk.CTkFrame(main_frame, fg_color="transparent"); form_frame.grid(row=0, column=1, sticky="nsew")
        ctk.CTkLabel(form_frame, text="Tipo de Material:", text_color=LIGHT_GRAY_TEXT).pack(anchor='w')
        self.type_var = ctk.StringVar(); self.type_combobox = ctk.CTkComboBox(form_frame, variable=self.type_var, state="readonly", height=40, command=self._on_type_select); self.type_combobox.pack(fill="x", pady=(0,10))
        ctk.CTkLabel(form_frame, text="Nombre:", text_color=LIGHT_GRAY_TEXT).pack(anchor='w')
        self.name_var = ctk.StringVar(); ctk.CTkEntry(form_frame, textvariable=self.name_var, height=40).pack(fill="x", pady=(0,10))
        ctk.CTkLabel(form_frame, text="Unidad de Medida:", text_color=LIGHT_GRAY_TEXT).pack(anchor='w')
        self.unit_var = ctk.StringVar(); ctk.CTkEntry(form_frame, textvariable=self.unit_var, height=40).pack(fill="x", pady=(0,10))
        
        self.dynamic_fields_frame = ctk.CTkScrollableFrame(form_frame, fg_color="transparent"); self.dynamic_fields_frame.pack(fill="both", expand=True)
        
        btn_container = ctk.CTkFrame(form_frame, fg_color="transparent"); btn_container.pack(fill="x")
        ctk.CTkButton(btn_container, text="Nuevo", command=self._clear_form, height=40, fg_color=DARK_GRAY, border_width=1).pack(side="left", expand=True, padx=(0,5))
        ctk.CTkButton(btn_container, text="Eliminar", command=self.delete_material, height=40, fg_color=DARK_GRAY, hover_color=ERROR_COLOR, border_width=1).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(btn_container, text="Guardar", command=self.save_material, height=40).pack(side="left", expand=True, padx=(5,0))

    def load_material_types(self):
        try:
            self.material_types = self.supabase_client.table("tipos_materiales").select("*").execute().data
            self.type_combobox.configure(values=[t['nombre_tipo'] for t in self.material_types])
        except Exception as e: messagebox.showerror("Error", f"No se cargaron los tipos: {e}")
    def _on_type_select(self, choice):
        selected_type = next((t for t in self.material_types if t['nombre_tipo'] == choice), None)
        if selected_type: self.generate_dynamic_fields(selected_type.get('campos_definidos', []))
    def generate_dynamic_fields(self, fields_definition, current_values={}):
        for widget in self.dynamic_fields_frame.winfo_children(): widget.destroy()
        self.dynamic_entries = {}
        for field in fields_definition:
            ctk.CTkLabel(self.dynamic_fields_frame, text=f"{field['etiqueta']}:", text_color=LIGHT_GRAY_TEXT).pack(anchor='w', pady=(5,0))
            entry_var = ctk.StringVar(value=current_values.get(field['nombre'], ''))
            ctk.CTkEntry(self.dynamic_fields_frame, textvariable=entry_var, height=40).pack(fill="x")
            self.dynamic_entries[field['nombre']] = entry_var
    def load_materials(self):
        self.materials_listbox.delete(0, tk.END)
        try:
            self.materials_data = self.supabase_client.table("materiales_maestro").select("*, tipo:tipos_materiales(nombre_tipo)").order("nombre_material").execute().data
            for material in self.materials_data: self.materials_listbox.insert(tk.END, material['nombre_material'])
        except Exception as e: messagebox.showerror("Error", f"No se cargaron los materiales: {e}")
    def _on_material_select(self, event):
        selected_indices = self.materials_listbox.curselection();
        if not selected_indices: return
        material = self.materials_data[selected_indices[0]]; self.selected_material_id = material['id_materiales']
        self.name_var.set(material.get('nombre_material', '')); self.unit_var.set(material.get('unidad_medida_base', ''))
        if material.get('tipo'):
            type_name = material['tipo']['nombre_tipo']; self.type_var.set(type_name)
            selected_type = next((t for t in self.material_types if t['nombre_tipo'] == type_name), None)
            if selected_type: self.generate_dynamic_fields(selected_type.get('campos_definidos', []), material.get('parametros_entrada', {}))
    def _clear_form(self):
        self.selected_material_id = None; self.name_var.set(""); self.unit_var.set(""); self.type_var.set("")
        self.materials_listbox.selection_clear(0, tk.END);
        for widget in self.dynamic_fields_frame.winfo_children(): widget.destroy()
        self.dynamic_entries = {}
    def save_material(self):
        name=self.name_var.get().strip(); unit=self.unit_var.get().strip(); type_name=self.type_var.get()
        if not name or not unit or not type_name: messagebox.showwarning("Info", "Tipo, nombre y unidad son obligatorios."); return
        selected_type = next((t for t in self.material_types if t['nombre_tipo'] == type_name), None)
        if not selected_type: messagebox.showerror("Error", "Tipo no válido."); return
        params_json = {}
        try:
            for n, v in self.dynamic_entries.items(): params_json[n] = float(v.get() or 0.0)
        except ValueError: messagebox.showerror("Error", "Los parámetros deben ser números."); return
        material_data = {"nombre_material": name, "unidad_medida_base": unit, "parametros_entrada": params_json, "tipo_material_id": selected_type['id_tipo_material']}
        try:
            if self.selected_material_id: self.supabase_client.table("materiales_maestro").update(material_data).eq("id_materiales", self.selected_material_id).execute()
            else: self.supabase_client.table("materiales_maestro").insert(material_data).execute()
            messagebox.showinfo("Éxito", "Material guardado."); self.load_materials(); self._clear_form()
        except Exception as e: messagebox.showerror("Error", f"No se pudo guardar: {e}")
    def delete_material(self):
        if not self.selected_material_id: messagebox.showwarning("Info", "Selecciona un material para eliminar."); return
        if messagebox.askyesno("Confirmar", "¿Eliminar este material?"):
            try:
                self.supabase_client.table("materiales_maestro").delete().eq("id_materiales", self.selected_material_id).execute()
                messagebox.showinfo("Éxito", "Material eliminado."); self.load_materials(); self._clear_form()
            except Exception as e: messagebox.showerror("Error", f"No se pudo eliminar: {e}")