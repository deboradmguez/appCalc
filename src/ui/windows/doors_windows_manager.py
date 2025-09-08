# src/ui/windows/doors_windows_manager.py (Corregido)

import customtkinter as ctk
from tkinter import messagebox
from config import FONT_SIZE_NORMAL, FONT_SIZE_SMALL, ACCENT_PRIMARY, ACCENT_HOVER, BORDER_PRIMARY, ERROR_COLOR, SUCCESS_COLOR, TRANSPARENT_BG

class DoorsWindowsManager(ctk.CTkToplevel):
    def __init__(self, master, supabase_client, area_data):
        super().__init__(master)
        self.supabase_client = supabase_client
        self.area_data = area_data
        
        self.area_name = area_data['areas_maestro']['nombre_area']
        self.area_id = area_data['id_proyectos_areas']

        self.title(f"Puertas y Ventanas de: {self.area_name}")
        window_width = 600
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.transient(master)
        self.grab_set()

        self.door_entries = []
        self.window_entries = []
        self.initial_doors = []
        self.initial_windows = []

        self._build_ui()
        self._load_initial_data()

    def _build_ui(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- TÍTULO ---
        title_label = ctk.CTkLabel(self, text=f"Gestionar para: {self.area_name}", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # --- CONTENEDOR PRINCIPAL ---
        container = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        container.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1) # Fila para Puertas
        container.grid_rowconfigure(1, weight=1) # Fila para Ventanas

        # --- SECCIÓN DE PUERTAS ---
        doors_container = ctk.CTkFrame(container, border_width=1, border_color=BORDER_PRIMARY)
        doors_container.grid(row=0, column=0, sticky="nsew", pady=(0, 10))
        doors_container.grid_columnconfigure(0, weight=1)
        doors_container.grid_rowconfigure(1, weight=1)

        doors_header = ctk.CTkFrame(doors_container)
        doors_header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ctk.CTkLabel(doors_header, text="🚪 Puertas", font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold")).pack(side="left")
        ctk.CTkButton(doors_header, text="+ Añadir", width=80, command=self._add_door_entry).pack(side="right")

        doors_content = ctk.CTkFrame(doors_container)
        doors_content.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.doors_scroll_frame = ctk.CTkScrollableFrame(doors_content, fg_color=TRANSPARENT_BG, border_width=0)
        self.doors_scroll_frame.pack(fill="both", expand=True)

        # --- SECCIÓN DE VENTANAS ---
        windows_container = ctk.CTkFrame(container, border_width=1, border_color=BORDER_PRIMARY)
        windows_container.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        windows_container.grid_columnconfigure(0, weight=1)
        windows_container.grid_rowconfigure(1, weight=1)

        windows_header = ctk.CTkFrame(windows_container)
        windows_header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        ctk.CTkLabel(windows_header, text="🪟 Ventanas", font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold")).pack(side="left")
        ctk.CTkButton(windows_header, text="+ Añadir", width=80, command=self._add_window_entry).pack(side="right")

        windows_content = ctk.CTkFrame(windows_container)
        windows_content.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.windows_scroll_frame = ctk.CTkScrollableFrame(windows_content, fg_color=TRANSPARENT_BG, border_width=0)
        self.windows_scroll_frame.pack(fill="both", expand=True)
        
        # --- BOTONES DE ACCIÓN ---
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=2, column=0, padx=20, pady=20, sticky="e")

        save_button = ctk.CTkButton(button_frame, text="Guardar y Cerrar", command=self._save_changes, fg_color=SUCCESS_COLOR, hover_color="#059669")
        save_button.pack(side="right")
        
        cancel_button = ctk.CTkButton(button_frame, text="Cancelar", command=self.destroy, fg_color="gray", text_color="black", border_color=BORDER_PRIMARY, border_width=2)
        cancel_button.pack(side="right", padx=10)

    def _load_initial_data(self):
        try:
            self.initial_doors = self.supabase_client.table("puertas").select("*").eq("proyectos_areas_id", self.area_id).execute().data
            for door in self.initial_doors: self._add_door_entry(door)

            self.initial_windows = self.supabase_client.table("ventanas").select("*").eq("proyectos_areas_id", self.area_id).execute().data
            for window in self.initial_windows: self._add_window_entry(window)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los datos existentes: {e}", parent=self)

    def _add_door_entry(self, data=None):
        self._add_item_entry(self.doors_scroll_frame, self.door_entries, "puertas", data)

    def _add_window_entry(self, data=None):
        self._add_item_entry(self.windows_scroll_frame, self.window_entries, "ventanas", data)

    def _add_item_entry(self, parent, entry_list, item_type, data=None):
        item_id = data.get(f'id_{"puertas" if "puerta" in item_type else "ventanas"}') if data else None
        ancho = data.get('ancho', '') if data else ''
        alto = data.get('alto', '') if data else ''

        row_frame = ctk.CTkFrame(parent, fg_color=("gray90", "gray20"))
        row_frame.pack(fill="x", pady=2, padx=2)

        ctk.CTkLabel(row_frame, text="Ancho (m):", font=ctk.CTkFont(size=FONT_SIZE_SMALL)).pack(side="left", padx=10)
        ancho_entry = ctk.CTkEntry(row_frame, width=80)
        ancho_entry.insert(0, str(ancho))
        ancho_entry.pack(side="left")

        ctk.CTkLabel(row_frame, text="Alto (m):", font=ctk.CTkFont(size=FONT_SIZE_SMALL)).pack(side="left", padx=10)
        alto_entry = ctk.CTkEntry(row_frame, width=80)
        alto_entry.insert(0, str(alto))
        alto_entry.pack(side="left")
        
        entry_data = {'id': item_id, 'ancho_var': ancho_entry, 'alto_var': alto_entry, 'frame': row_frame}
        entry_list.append(entry_data)
        
        delete_button = ctk.CTkButton(row_frame, text="🗑️", width=30, fg_color="transparent", text_color=ERROR_COLOR, hover_color="#FEE2E2", command=lambda e=entry_data: self._mark_for_deletion(e))
        delete_button.pack(side="right", padx=10)
        entry_data['delete_button'] = delete_button

    def _mark_for_deletion(self, entry_data):
        entry_data['deleted'] = True
        entry_data['frame'].configure(fg_color=("gray70", "gray10"))
        entry_data['ancho_var'].configure(state="disabled")
        entry_data['alto_var'].configure(state="disabled")
        entry_data['delete_button'].configure(text="↩️", fg_color="transparent", text_color=None, hover_color="gray80", command=lambda e=entry_data: self._unmark_for_deletion(e))

    def _unmark_for_deletion(self, entry_data):
        entry_data['deleted'] = False
        entry_data['frame'].configure(fg_color=("gray90", "gray20"))
        entry_data['ancho_var'].configure(state="normal")
        entry_data['alto_var'].configure(state="normal")
        entry_data['delete_button'].configure(text="🗑️", fg_color="transparent", text_color=ERROR_COLOR, hover_color="#FEE2E2", command=lambda e=entry_data: self._mark_for_deletion(e))
    
    def _save_changes(self):
        try:
            self._process_items("puertas", self.door_entries, self.initial_doors)
            self._process_items("ventanas", self.window_entries, self.initial_windows)
            messagebox.showinfo("Éxito", "Los cambios se guardaron correctamente.", parent=self)
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar los cambios: {e}", parent=self)

    def _process_items(self, table_name, entries, initial_data):
        pk_name = f'id_{"puertas" if "puerta" in table_name else "ventanas"}'
        initial_ids = {item.get(pk_name) for item in initial_data}
        for entry in entries:
            entry_id = entry.get('id')
            is_marked_for_deletion = entry.get('deleted', False)
            ancho = float(entry['ancho_var'].get() or 0)
            alto = float(entry['alto_var'].get() or 0)
            
            if entry_id and is_marked_for_deletion:
                self.supabase_client.table(table_name).delete().eq(pk_name, entry_id).execute()
            elif is_marked_for_deletion:
                continue
            elif entry_id in initial_ids:
                self.supabase_client.table(table_name).update({"ancho": ancho, "alto": alto}).eq(pk_name, entry_id).execute()
            elif not entry_id:
                self.supabase_client.table(table_name).insert({"ancho": ancho, "alto": alto, "proyectos_areas_id": self.area_id}).execute()