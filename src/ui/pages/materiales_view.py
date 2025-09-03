import tkinter as tk
from tkinter import ttk, messagebox, Text
import json

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))
from config import *

class MaterialesView(tk.Frame):
    def __init__(self, master, supabase_client):
        super().__init__(master, bg=DARK_GRAY)
        self.supabase_client = supabase_client
        self.materials_data = []
        self.material_types = []
        self.selected_material_id = None
        self.dynamic_entries = {}

        self._build_ui()
        self.load_materials()
        self.load_material_types()

    def _build_ui(self):
        title_label = tk.Label(self, text="Administración de Materiales", font=(FONT_PRIMARY, FONT_SIZE_TITLE, "bold"), fg=NEAR_WHITE, bg=DARK_GRAY)
        title_label.pack(pady=30, padx=30, anchor="w")

        main_frame = tk.Frame(self, bg=DARK_GRAY)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=30)

        # --- Columna Izquierda: Lista de Materiales ---
        list_frame = tk.Frame(main_frame, bg=DARK_GRAY)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 20))
        
        tk.Label(list_frame, text="Materiales existentes:", font=(FONT_PRIMARY, FONT_SIZE_NORMAL), fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(anchor='w')
        self.materials_listbox = tk.Listbox(list_frame, **LISTBOX_STYLE)
        self.materials_listbox.pack(fill=tk.BOTH, expand=True)
        self.materials_listbox.bind("<<ListboxSelect>>", self._on_material_select)

        # --- Columna Derecha: Formulario de Edición ---
        form_frame = tk.Frame(main_frame, bg=DARK_GRAY)
        form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(20, 0))

        # --- Campos Fijos ---
        tk.Label(form_frame, text="Tipo de Material:", fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(anchor='w')
        self.type_var = tk.StringVar()
        self.type_combobox = ttk.Combobox(form_frame, textvariable=self.type_var, state="readonly", font=(FONT_PRIMARY, FONT_SIZE_NORMAL))
        self.type_combobox.pack(fill=tk.X, pady=(0,10))
        self.type_combobox.bind("<<ComboboxSelected>>", self._on_type_select)

        tk.Label(form_frame, text="Nombre del Material:", fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(anchor='w')
        self.name_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.name_var, **ENTRY_STYLE).pack(fill=tk.X, ipady=5, pady=(0,10))

        tk.Label(form_frame, text="Unidad de Medida (ej: m², L, kg):", fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(anchor='w')
        self.unit_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.unit_var, **ENTRY_STYLE).pack(fill=tk.X, ipady=5, pady=(0,10))
        
        # --- Frame para los campos dinámicos ---
        self.dynamic_fields_frame = tk.Frame(form_frame, bg=DARK_GRAY)
        self.dynamic_fields_frame.pack(fill=tk.BOTH, expand=True)
        
        button_container = tk.Frame(form_frame, bg=DARK_GRAY)
        button_container.pack(fill=tk.X)
        tk.Button(button_container, text="Nuevo", command=self._clear_form, **BUTTON_STYLE_SECONDARY).pack(side=tk.LEFT, ipady=8, ipadx=10)
        tk.Button(button_container, text="Eliminar", command=self.delete_material, fg=ERROR_COLOR, bg=DARK_GRAY, activeforeground=WHITE, activebackground=ERROR_COLOR, font=(FONT_PRIMARY, FONT_SIZE_NORMAL), relief='flat', cursor="hand2").pack(side=tk.LEFT, padx=10, ipady=8, ipadx=10)
        tk.Button(button_container, text="Guardar", command=self.save_material, **BUTTON_STYLE_PRIMARY).pack(side=tk.RIGHT, ipady=8, ipadx=10)

    def load_material_types(self):
        """Carga los tipos de material para poblar el menú desplegable."""
        try:
            self.material_types = self.supabase_client.table("tipos_materiales").select("*").execute().data
            type_names = [t['nombre_tipo'] for t in self.material_types]
            self.type_combobox['values'] = type_names
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los tipos de materiales: {e}")

    def _on_type_select(self, event):
        """Cuando se selecciona un tipo, genera el formulario dinámico."""
        selected_type_name = self.type_var.get()
        selected_type = next((t for t in self.material_types if t['nombre_tipo'] == selected_type_name), None)
        
        if selected_type:
            self.generate_dynamic_fields(selected_type.get('campos_definidos', []))

    def generate_dynamic_fields(self, fields_definition, current_values=None):
        """Limpia y crea los campos de entrada basados en la definición."""
        if current_values is None:
            current_values = {}
            
        for widget in self.dynamic_fields_frame.winfo_children():
            widget.destroy()
        self.dynamic_entries = {}

        for field in fields_definition:
            field_name = field['nombre']
            field_label = field['etiqueta']
            
            tk.Label(self.dynamic_fields_frame, text=f"{field_label}:", fg=LIGHT_GRAY_TEXT, bg=DARK_GRAY).pack(anchor='w', pady=(5,0))
            entry_var = tk.StringVar(value=current_values.get(field_name, ''))
            entry = tk.Entry(self.dynamic_fields_frame, textvariable=entry_var, **ENTRY_STYLE)
            entry.pack(fill=tk.X, ipady=5)
            self.dynamic_entries[field_name] = entry_var

    def load_materials(self):
        # ... (código sin cambios)
        self.materials_listbox.delete(0, tk.END)
        try:
            self.materials_data = self.supabase_client.table("materiales_maestro").select("*, tipo:tipos_materiales(nombre_tipo)").order("nombre_material").execute().data
            for material in self.materials_data:
                self.materials_listbox.insert(tk.END, material['nombre_material'])
        except Exception as e:
            messagebox.showerror("Error de Carga", f"No se pudieron cargar los materiales: {e}")

    def _on_material_select(self, event):
        selected_indices = self.materials_listbox.curselection()
        if not selected_indices: return
        
        material = self.materials_data[selected_indices[0]]
        self.selected_material_id = material['id_materiales']

        # Rellenar campos fijos
        self.name_var.set(material.get('nombre_material', ''))
        self.unit_var.set(material.get('unidad_medida_base', ''))
        
        # Seleccionar el tipo correcto en el combobox y generar los campos
        if material.get('tipo'):
            type_name = material['tipo']['nombre_tipo']
            self.type_var.set(type_name)
            
            selected_type = next((t for t in self.material_types if t['nombre_tipo'] == type_name), None)
            if selected_type:
                self.generate_dynamic_fields(selected_type.get('campos_definidos', []), material.get('parametros_entrada', {}))

    def _clear_form(self):
        self.selected_material_id = None
        self.name_var.set("")
        self.unit_var.set("")
        self.type_var.set("")
        self.materials_listbox.selection_clear(0, tk.END)
        for widget in self.dynamic_fields_frame.winfo_children():
            widget.destroy()
        self.dynamic_entries = {}

    def save_material(self):
        # ... (Lógica de guardado actualizada)
        name = self.name_var.get().strip()
        unit = self.unit_var.get().strip()
        type_name = self.type_var.get()

        if not name or not unit or not type_name:
            messagebox.showwarning("Campos Requeridos", "El tipo, nombre y unidad son obligatorios.")
            return

        selected_type = next((t for t in self.material_types if t['nombre_tipo'] == type_name), None)
        if not selected_type:
            messagebox.showerror("Error", "Tipo de material no válido.")
            return

        # Construir el JSON a partir de los campos dinámicos
        params_json = {}
        try:
            for name, var in self.dynamic_entries.items():
                # Asumimos que todos los campos son numéricos por ahora
                params_json[name] = float(var.get() or 0.0)
        except ValueError:
            messagebox.showerror("Error de Entrada", "Todos los parámetros deben ser números.")
            return

        material_data = {
            "nombre_material": name,
            "unidad_medida_base": unit,
            "parametros_entrada": params_json,
            "tipo_material_id": selected_type['id_tipo_material']
        }

        try:
            if self.selected_material_id:
                self.supabase_client.table("materiales_maestro").update(material_data).eq("id_materiales", self.selected_material_id).execute()
            else:
                self.supabase_client.table("materiales_maestro").insert(material_data).execute()
            
            messagebox.showinfo("Éxito", "Material guardado.")
            self.load_materials()
            self._clear_form()
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudo guardar: {e}")
            
    def delete_material(self):
        # ... (código sin cambios)
        if not self.selected_material_id:
            messagebox.showwarning("Sin Selección", "Por favor, selecciona un material para eliminar.")
            return
        if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres eliminar este material?"):
            try:
                self.supabase_client.table("materiales_maestro").delete().eq("id_materiales", self.selected_material_id).execute()
                messagebox.showinfo("Éxito", "Material eliminado.")
                self.load_materials()
                self._clear_form()
            except Exception as e:
                messagebox.showerror("Error al Eliminar", f"No se pudo eliminar: {e}")