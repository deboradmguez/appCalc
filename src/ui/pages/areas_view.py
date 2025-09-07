# src/ui/pages/areas_view.py

import customtkinter as ctk
from tkinter import messagebox
from config import (
    FONT_SIZE_TITLE, FONT_SIZE_NORMAL, FONT_SIZE_SMALL, 
    get_main_colors, BACKGROUND_CARD, ACCENT_PRIMARY, 
    ACCENT_HOVER, TEXT_PRIMARY, TEXT_SECONDARY, BORDER_PRIMARY,
    SUCCESS_COLOR, ERROR_COLOR, TRANSPARENT_BG 
)

class AreasView(ctk.CTkFrame):
    def __init__(self, master, master_app, **kwargs):
        colors = get_main_colors()
        super().__init__(master, fg_color=colors['bg_primary'], **kwargs)
        
        self.supabase_client = master_app.supabase_client
        self.master_areas_data = []
        self.selected_area = None
        self.selected_card = None
        self.colors = colors
        
        self._build_ui()
        self.load_master_areas()

    def _build_ui(self):
        """Construye la interfaz de usuario mejorada"""
        
        # === HEADER SECTION ===
        header_frame = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG )
        header_frame.pack(fill="x", padx=0, pady=(0, 25))
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame, 
            text="🏗️ Administración de Áreas Maestras", 
            font=ctk.CTkFont(size=FONT_SIZE_TITLE, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title_label.pack(side="left", anchor="w", pady=15)
        
        # Descripción
        desc_label = ctk.CTkLabel(
            header_frame, 
            text="Gestiona las áreas que podrás asignar a tus proyectos", 
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1),
            text_color=self.colors['text_secondary']
        )
        desc_label.pack(side="left", anchor="w", padx=(20, 0))
        
        # === MAIN CONTENT CONTAINER ===
        main_container = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG )
        main_container.pack(fill="both", expand=True, padx=0)
        
        # Configurar grid
        main_container.grid_columnconfigure(0, weight=2)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=1)
        
        # === LEFT PANEL - AREAS LIST ===
        self._create_areas_list_panel(main_container)
        
        # === RIGHT PANEL - ACTIONS ===
        self._create_actions_panel(main_container)

    def _create_areas_list_panel(self, parent):
        """Crea el panel izquierdo con la lista de áreas"""
        
        list_container = ctk.CTkFrame(parent, fg_color=TRANSPARENT_BG )
        list_container.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        
        list_header = ctk.CTkFrame(list_container, fg_color=TRANSPARENT_BG )
        list_header.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            list_header,
            text="📋 Áreas Existentes",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")
        
        self.area_count_label = ctk.CTkLabel(
            list_header,
            text="",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary']
        )
        self.area_count_label.pack(side="right")
        
        self.areas_list_frame = ctk.CTkScrollableFrame(
            list_container,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        self.areas_list_frame.pack(fill="both", expand=True)

    def _create_actions_panel(self, parent):
        """Crea el panel derecho con las acciones"""
        
        actions_container = ctk.CTkFrame(
            parent,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        actions_container.grid(row=0, column=1, sticky="nsew", padx=(15, 0))
        
        actions_header = ctk.CTkLabel(
            actions_container,
            text="⚙️ Panel de Acciones",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 1, weight="bold"),
            text_color=self.colors['text_primary']
        )
        actions_header.pack(pady=(25, 20))
        
        new_area_frame = ctk.CTkFrame(actions_container, fg_color=TRANSPARENT_BG )
        new_area_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        ctk.CTkLabel(
            new_area_frame,
            text="➕ Nueva Área",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w", pady=(0, 10))
        
        self.new_area_entry = ctk.CTkEntry(
            new_area_frame,
            height=45,
            corner_radius=10,
            border_width=2,
            border_color=BORDER_PRIMARY,
            placeholder_text="Ej: Cocina, Baño, Dormitorio...",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL)
        )
        self.new_area_entry.pack(fill="x", pady=(0, 10))
        
        self.new_area_entry.bind("<Return>", lambda e: self.add_area())
        
        add_btn = ctk.CTkButton(
            new_area_frame,
            text="➕ Añadir Área",
            command=self.add_area,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_HOVER,
            corner_radius=10
        )
        add_btn.pack(fill="x")
        
        separator = ctk.CTkFrame(actions_container, height=2, fg_color=BORDER_PRIMARY)
        separator.pack(fill="x", padx=20, pady=20)
        
        selected_frame = ctk.CTkFrame(actions_container, fg_color=TRANSPARENT_BG )
        selected_frame.pack(fill="x", padx=20, pady=(0, 25))
        
        ctk.CTkLabel(
            selected_frame,
            text="✏️ Área Seleccionada",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w", pady=(0, 10))
        
        self.selected_area_label = ctk.CTkLabel(
            selected_frame,
            text="Ninguna área seleccionada",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary'],
            fg_color="#F3F4F6",
            corner_radius=8,
            padx=15,
            pady=10
        )
        self.selected_area_label.pack(fill="x", pady=(0, 10))
        
        self.edit_area_entry = ctk.CTkEntry(
            selected_frame,
            height=40,
            corner_radius=10,
            border_width=2,
            border_color=BORDER_PRIMARY,
            placeholder_text="Nuevo nombre del área",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
            state="disabled"
        )
        self.edit_area_entry.pack(fill="x", pady=(0, 10))
        
        buttons_frame = ctk.CTkFrame(selected_frame, fg_color=TRANSPARENT_BG )
        buttons_frame.pack(fill="x")
        
        self.edit_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Editar",
            command=self.update_selected_area,
            height=35,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"),
            fg_color=TRANSPARENT_BG ,
            hover_color=BORDER_PRIMARY,
            text_color=self.colors['text_secondary'],
            border_width=2,
            border_color=BORDER_PRIMARY,
            corner_radius=8,
            state="disabled"
        )
        self.edit_btn.pack(fill="x", pady=(0, 5))
        
        self.delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Eliminar",
            command=self.delete_selected_area,
            height=35,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"),
            fg_color=TRANSPARENT_BG ,
            hover_color="#FEE2E2",
            text_color=ERROR_COLOR,
            border_width=2,
            border_color=ERROR_COLOR,
            corner_radius=8,
            state="disabled"
        )
        self.delete_btn.pack(fill="x")
        
        info_frame = ctk.CTkFrame(actions_container, fg_color=TRANSPARENT_BG )
        info_frame.pack(fill="x", padx=20, pady=(25, 20), side="bottom")
        
        info_text = ctk.CTkLabel(
            info_frame,
            text="💡 Tip: Haz clic en un área de la lista\npara seleccionarla y poder editarla\no eliminarla.",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL - 1),
            text_color=self.colors['text_secondary'],
            justify="center"
        )
        info_text.pack()

    def load_master_areas(self):
        """Carga las áreas maestras desde la base de datos"""
        
        for widget in self.areas_list_frame.winfo_children():
            widget.destroy()
        
        try:
            self.master_areas_data = self.supabase_client.table("areas_maestro").select("*").order("nombre_area").execute().data
            
            self.area_count_label.configure(text=f"({len(self.master_areas_data)} áreas)")
            
            if not self.master_areas_data:
                self._create_empty_areas_state()
            else:
                for area in self.master_areas_data:
                    self._create_area_card(area)
                    
        except Exception as e:
            self._create_error_areas_state(str(e))
            messagebox.showerror("Error", f"No se pudieron cargar las áreas: {e}")

    def _create_empty_areas_state(self):
        """Crea el estado vacío cuando no hay áreas"""
        
        empty_frame = ctk.CTkFrame(self.areas_list_frame, fg_color=TRANSPARENT_BG )
        empty_frame.pack(fill="both", expand=True, pady=40)
        
        ctk.CTkLabel(empty_frame, text="📦", font=ctk.CTkFont(size=60)).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            empty_frame,
            text="No hay áreas creadas",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 1, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=(0, 5))
        
        ctk.CTkLabel(
            empty_frame,
            text="Crea tu primera área usando el panel de la derecha",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary']
        ).pack()

    def _create_error_areas_state(self, error_msg):
        """Crea el estado de error al cargar áreas"""
        
        error_frame = ctk.CTkFrame(self.areas_list_frame, fg_color=TRANSPARENT_BG )
        error_frame.pack(fill="both", expand=True, pady=40)
        
        ctk.CTkLabel(
            error_frame,
            text="⚠️ Error al cargar áreas",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            text_color=ERROR_COLOR
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            error_frame,
            text=error_msg,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary']
        ).pack()

    def _create_area_card(self, area):
        """Crea una tarjeta para cada área"""
        
        card_frame = ctk.CTkFrame(
            self.areas_list_frame,
            fg_color=TRANSPARENT_BG,
            corner_radius=8,
            border_width=2,
            # CORREGIDO: Usar el color del fondo para que el borde sea invisible por defecto
            border_color=BACKGROUND_CARD
        )
        card_frame.pack(fill="x", pady=3, padx=15)
        
        content_frame = ctk.CTkFrame(card_frame, fg_color=TRANSPARENT_BG )
        content_frame.pack(fill="x", padx=15, pady=12)
        
        name_label = ctk.CTkLabel(
            content_frame,
            text=f"🏠 {area['nombre_area']}",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        name_label.pack(side="left", fill="x", expand=True)
        
        selection_indicator = ctk.CTkLabel(
            content_frame,
            text="✓",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"),
            text_color=SUCCESS_COLOR,
            width=30
        )
        
        def select_area(event=None):
            self._select_area(area, card_frame, selection_indicator)
        
        card_frame.bind("<Button-1>", select_area)
        content_frame.bind("<Button-1>", select_area)
        name_label.bind("<Button-1>", select_area)
        
        def on_enter(event):
            if card_frame != self.selected_card:
                card_frame.configure(border_color=BORDER_PRIMARY, fg_color="#FAFAFA")
        
        def on_leave(event):
            if card_frame != self.selected_card:
                # CORREGIDO: Usar el color del fondo para que el borde sea invisible al salir
                card_frame.configure(border_color=BACKGROUND_CARD, fg_color=TRANSPARENT_BG)
        
        card_frame.bind("<Enter>", on_enter)
        card_frame.bind("<Leave>", on_leave)

    def _select_area(self, area, card_frame, selection_indicator):
        """Selecciona un área"""
        
        if self.selected_card:
            self.selected_card.configure(
                # CORREGIDO: Usar el color del fondo al deseleccionar
                border_color=BACKGROUND_CARD, 
                fg_color=TRANSPARENT_BG 
            )
            for widget in self.selected_card.winfo_children():
                for child in widget.winfo_children():
                    if isinstance(child, ctk.CTkFrame):
                        for grandchild in child.winfo_children():
                            if isinstance(grandchild, ctk.CTkLabel) and grandchild.cget("text") == "✓":
                                grandchild.pack_forget()
        
        self.selected_area = area
        self.selected_card = card_frame
        
        card_frame.configure(border_color=ACCENT_PRIMARY, fg_color="#FFF7ED")
        
        selection_indicator.pack(side="right")
        
        self._update_actions_panel()

    def _update_actions_panel(self):
        """Actualiza el panel de acciones con el área seleccionada"""
        
        if self.selected_area:
            self.selected_area_label.configure(text=f"📋 {self.selected_area['nombre_area']}", fg_color="#E6FFFA", text_color="#047857")
            
            self.edit_area_entry.configure(state="normal")
            self.edit_area_entry.delete(0, "end")
            self.edit_area_entry.insert(0, self.selected_area['nombre_area'])
            
            self.edit_btn.configure(state="normal")
            self.delete_btn.configure(state="normal")
        else:
            self.selected_area_label.configure(text="Ninguna área seleccionada", fg_color="#F3F4F6", text_color=self.colors['text_secondary'])
            
            self.edit_area_entry.configure(state="disabled")
            self.edit_area_entry.delete(0, "end")
            
            self.edit_btn.configure(state="disabled")
            self.delete_btn.configure(state="disabled")

    def add_area(self):
        """Añade una nueva área"""
        
        new_name = self.new_area_entry.get().strip()
        if not new_name:
            messagebox.showwarning("Advertencia", "Por favor, ingresa el nombre del área.")
            return
        
        existing_names = [area['nombre_area'].lower() for area in self.master_areas_data]
        if new_name.lower() in existing_names:
            messagebox.showwarning("Advertencia", "Ya existe un área con ese nombre.")
            return
        
        try:
            self.supabase_client.table("areas_maestro").insert({"nombre_area": new_name}).execute()
            
            self.new_area_entry.delete(0, "end")
            self.load_master_areas()
            
            messagebox.showinfo("Éxito", f"Área '{new_name}' añadida correctamente.")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo añadir el área: {e}")

    def update_selected_area(self):
        """Actualiza el área seleccionada"""
        
        if not self.selected_area:
            messagebox.showwarning("Advertencia", "Selecciona un área para editar.")
            return
        
        new_name = self.edit_area_entry.get().strip()
        if not new_name:
            messagebox.showwarning("Advertencia", "El nombre del área no puede estar vacío.")
            return
        
        existing_names = [area['nombre_area'].lower() for area in self.master_areas_data if area['id'] != self.selected_area['id']]
        if new_name.lower() in existing_names:
            messagebox.showwarning("Advertencia", "Ya existe un área con ese nombre.")
            return
        
        if not messagebox.askyesno("Confirmar Edición", f"¿Estás seguro de cambiar '{self.selected_area['nombre_area']}' a '{new_name}'?"):
            return
        
        try:
            self.supabase_client.table("areas_maestro").update({"nombre_area": new_name}).eq("id", self.selected_area['id']).execute()
            
            self.selected_area = None
            self.selected_card = None
            self.load_master_areas()
            self._update_actions_panel()
            
            messagebox.showinfo("Éxito", f"Área actualizada a '{new_name}'.")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el área: {e}")

    def delete_selected_area(self):
        """Elimina el área seleccionada"""
        
        if not self.selected_area:
            messagebox.showwarning("Advertencia", "Selecciona un área para eliminar.")
            return
        
        if not messagebox.askyesno("Confirmar Eliminación", f"¿Estás seguro de eliminar el área '{self.selected_area['nombre_area']}'?\n\nEsta acción no se puede deshacer."):
            return
        
        try:
            self.supabase_client.table("areas_maestro").delete().eq("id", self.selected_area['id']).execute()
            
            self.selected_area = None
            self.selected_card = None
            self.load_master_areas()
            self._update_actions_panel()
            
            messagebox.showinfo("Éxito", "Área eliminada correctamente.")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el área: {e}")