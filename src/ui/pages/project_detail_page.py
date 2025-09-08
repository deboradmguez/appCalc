# src/ui/pages/project_detail_page.py

import customtkinter as ctk
from tkinter import messagebox
from src.ui.windows.doors_windows_manager import DoorsWindowsManager
from config import (
    FONT_SIZE_TITLE, FONT_SIZE_NORMAL, FONT_SIZE_SMALL,
    get_main_colors, BACKGROUND_CARD, ACCENT_PRIMARY,
    ACCENT_HOVER, TEXT_PRIMARY, TEXT_SECONDARY, BORDER_PRIMARY,
    SUCCESS_COLOR, ERROR_COLOR, WARNING_COLOR, TRANSPARENT_BG
)

class ProjectDetailPage(ctk.CTkFrame):
    def __init__(self, master, master_app, proyecto, on_back, **kwargs):
        colors = get_main_colors()
        super().__init__(master, fg_color=colors['bg_primary'], **kwargs)

        self.supabase_client = master_app.supabase_client
        self.proyecto = proyecto
        self.on_back = on_back
        self.colors = colors
        self.project_areas = []

        self.stat_total_areas_label = None
        self.stat_total_m2_label = None

        # Lista para guardar referencias a los widgets de cada fila
        self.area_widget_refs = []

        self.build_ui()

    def build_ui(self):
        """Construye la interfaz de usuario con la nueva estructura de pestañas."""
        self._create_header()

        tab_view = ctk.CTkTabview(
            self,
            fg_color=BACKGROUND_CARD,
            segmented_button_fg_color=self.colors['bg_primary'],
            segmented_button_selected_color=ACCENT_PRIMARY,
            segmented_button_selected_hover_color=ACCENT_HOVER,
            segmented_button_unselected_hover_color=self.colors['bg_secondary']
        )
        tab_view.pack(fill="both", expand=True, padx=0, pady=(15, 0))

        tab_view.add("Áreas del Proyecto")
        tab_view.add("Resumen")
        tab_view.add("Cálculo de Materiales")

        self._build_areas_tab(tab_view.tab("Áreas del Proyecto"))
        self._build_summary_tab(tab_view.tab("Resumen"))
        self._build_materials_tab(tab_view.tab("Cálculo de Materiales"))

        tab_view.set("Áreas del Proyecto")

    def _create_header(self):
        """Crea la sección del header."""
        header_frame = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        header_frame.pack(fill="x", padx=0, pady=(0, 0))

        back_btn = ctk.CTkButton(
            header_frame, text="← Volver a Proyectos", command=self.on_back, height=40, width=160,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"), fg_color=TRANSPARENT_BG,
            hover_color=BORDER_PRIMARY, text_color=self.colors['text_primary'], border_width=2,
            border_color=BORDER_PRIMARY, corner_radius=10
        )
        back_btn.pack(side="left", pady=10)

        title_frame = ctk.CTkFrame(header_frame, fg_color=TRANSPARENT_BG)
        title_frame.pack(side="left", fill="x", expand=True, padx=(20, 0))

        ctk.CTkLabel(
            title_frame, text=f"🏗️ {self.proyecto['nombre_proyecto']}",
            font=ctk.CTkFont(size=FONT_SIZE_TITLE + 2, weight="bold"),
            text_color=self.colors['text_primary'], anchor="w"
        ).pack(anchor="w")

        if self.proyecto.get('direccion_proyecto'):
            ctk.CTkLabel(
                title_frame, text=f"📍 {self.proyecto['direccion_proyecto']}",
                font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
                text_color=self.colors['text_secondary'], anchor="w"
            ).pack(anchor="w", pady=(5, 0))

    def _build_summary_tab(self, tab):
        """Crea el contenido de la pestaña 'Resumen'."""
        tab.grid_columnconfigure((0, 1, 2), weight=1)
        tab.grid_rowconfigure(0, weight=0)

        self.stat_total_areas_label = self._create_stat_item(tab, "📋", "Áreas Totales", "...", 0, 0)
        self.stat_total_m2_label = self._create_stat_item(tab, "📏", "Área Total (m²)", "...", 0, 1)
        self._create_stat_item(tab, "📅", "Fecha Creación", self._format_date(self.proyecto.get('fecha_creacion')), 0, 2)

    def _create_stat_item(self, parent, icon, label, value, row, col):
        """Crea un elemento de estadística y devuelve el label del valor para futuras actualizaciones."""
        stat_frame = ctk.CTkFrame(parent, fg_color="#F8FAFC", corner_radius=10)
        stat_frame.grid(row=row, column=col, padx=10, pady=20, sticky="ew")

        content = ctk.CTkFrame(stat_frame, fg_color=TRANSPARENT_BG)
        content.pack(fill="x", padx=15, pady=15)

        ctk.CTkLabel(content, text=icon, font=ctk.CTkFont(size=20)).pack(pady=(0, 5))

        value_label = ctk.CTkLabel(
            content, text=str(value), font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"),
            text_color=ACCENT_PRIMARY
        )
        value_label.pack()

        ctk.CTkLabel(
            content, text=label, font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary']
        ).pack(pady=(2, 0))

        return value_label

    def _build_areas_tab(self, tab):
        """Crea el contenido de la pestaña 'Áreas del Proyecto'."""
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        areas_header = ctk.CTkFrame(tab, fg_color=TRANSPARENT_BG)
        areas_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))

        ctk.CTkLabel(
            areas_header, text="Gestión de Áreas del Proyecto",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 3, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")

        ctk.CTkButton(
            areas_header, text="+ Agregar Área", height=35, width=130,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"),
            fg_color=ACCENT_PRIMARY, hover_color=ACCENT_HOVER, corner_radius=8,
            command=self._show_add_area_info
        ).pack(side="right")

        self.areas_container = ctk.CTkFrame(tab, fg_color=TRANSPARENT_BG)
        self.areas_container.grid(row=1, column=0, sticky="nsew", padx=20, pady=0)

        save_all_button = ctk.CTkButton(
            tab, text="💾 Guardar Todos los Cambios", height=40,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            fg_color=SUCCESS_COLOR, hover_color="#059669",
            command=self.save_all_changes
        )
        save_all_button.grid(row=2, column=0, sticky="e", padx=20, pady=15)

        self.load_project_areas()

    def _build_materials_tab(self, tab):
        """Crea el contenido de la pestaña 'Cálculo de Materiales'."""
        tab.pack_propagate(False)
        container = ctk.CTkFrame(tab, fg_color=TRANSPARENT_BG)
        container.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(
            container, text="Cálculo de Materiales por Tipo",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 3, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w")

        ctk.CTkLabel(
            container, text="Selecciona un tipo de material para comenzar el cálculo.",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL), text_color=TEXT_SECONDARY
        ).pack(anchor="w", pady=(5, 15))

        material_types = ["Pintura", "Techo", "Piso", "Muros", "Electricidad"]
        segmented_button = ctk.CTkSegmentedButton(
            container, values=material_types, height=40,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            selected_color=ACCENT_PRIMARY,
            selected_hover_color=ACCENT_HOVER
        )
        segmented_button.pack(fill="x", pady=10)

        ctk.CTkLabel(
            container, text="🚧 Esta sección está en desarrollo y mostrará los cálculos detallados para el tipo de material seleccionado.",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL), text_color=WARNING_COLOR, wraplength=600
        ).pack(pady=40)

    def load_project_areas(self):
        """Carga y muestra las áreas del proyecto en su contenedor."""
        if not hasattr(self, 'areas_container'): return

        self.area_widget_refs.clear()
        for widget in self.areas_container.winfo_children():
            widget.destroy()

        try:
            self.project_areas = self.supabase_client.table("proyectos_areas").select(
                "*, areas_maestro(nombre_area)"
            ).eq("proyecto_id", self.proyecto['id_proyecto']).execute().data

            self._update_project_stats()

            if not self.project_areas:
                self._create_empty_areas_state()
            else:
                scrollable_areas = ctk.CTkScrollableFrame(self.areas_container, fg_color=TRANSPARENT_BG)
                scrollable_areas.pack(fill="both", expand=True)

                self._create_areas_table_header(scrollable_areas)
                for area_data in self.project_areas:
                    self._create_area_row(scrollable_areas, area_data)

        except Exception as e:
            self._create_error_areas_state(str(e))
            messagebox.showerror("Error", f"No se pudieron cargar las áreas del proyecto: {e}")

    def _update_project_stats(self):
        """Actualiza las etiquetas de estadísticas en la pestaña Resumen."""
        total_areas = len(self.project_areas)
        total_area_m2 = sum(self._calculate_area(a.get('ancho', 0), a.get('largo', 0)) for a in self.project_areas)

        if self.stat_total_areas_label:
            self.stat_total_areas_label.configure(text=str(total_areas))
        if self.stat_total_m2_label:
            self.stat_total_m2_label.configure(text=f"{total_area_m2:.2f} m²")

    def _create_areas_table_header(self, container):
        header_frame = ctk.CTkFrame(container, fg_color="#F1F5F9", corner_radius=10, border_width=1, border_color=BORDER_PRIMARY)
        header_frame.pack(fill="x", pady=(5, 5), padx=0)

        header_frame.grid_columnconfigure(0, weight=3)
        header_frame.grid_columnconfigure((1, 2, 3, 4), weight=1)
        header_frame.grid_columnconfigure(5, weight=2)

        headers = ["🏠 Área", "Ancho (m)", "Largo (m)", "Alto (m)", "Área (m²)", "Opciones"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(
                header_frame, text=h, font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"),
                text_color=self.colors['text_primary']
            ).grid(row=0, column=i, sticky="w", padx=15, pady=12)

    def _create_area_row(self, container, area_data):
        row_frame = ctk.CTkFrame(container, fg_color="white", corner_radius=8, border_width=1, border_color="#E2E8F0")
        row_frame.pack(fill="x", pady=2, padx=0)
        row_frame.grid_columnconfigure(0, weight=3)
        row_frame.grid_columnconfigure((1, 2, 3, 4), weight=1)
        row_frame.grid_columnconfigure(5, weight=2)

        ctk.CTkLabel(
            row_frame, text=area_data['areas_maestro']['nombre_area'],
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"), anchor="w"
        ).grid(row=0, column=0, sticky="w", padx=15, pady=15)

        ancho_var = ctk.StringVar(value=str(area_data.get('ancho', '') or ''))
        largo_var = ctk.StringVar(value=str(area_data.get('largo', '') or ''))
        alto_var = ctk.StringVar(value=str(area_data.get('alto', '') or ''))

        entry_props = {'width': 80, 'height': 35, 'corner_radius': 6, 'border_width': 1, 'border_color': BORDER_PRIMARY, 'font': ctk.CTkFont(size=FONT_SIZE_SMALL + 1)}
        ancho_entry = ctk.CTkEntry(row_frame, textvariable=ancho_var, **entry_props)
        ancho_entry.grid(row=0, column=1, padx=10, pady=10)
        largo_entry = ctk.CTkEntry(row_frame, textvariable=largo_var, **entry_props)
        largo_entry.grid(row=0, column=2, padx=10, pady=10)
        alto_entry = ctk.CTkEntry(row_frame, textvariable=alto_var, **entry_props)
        alto_entry.grid(row=0, column=3, padx=10, pady=10)

        area_m2 = self._calculate_area(ancho_var.get(), largo_var.get())
        area_label = ctk.CTkLabel(row_frame, text=f"{area_m2:.2f}", font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"), text_color=ACCENT_PRIMARY)
        area_label.grid(row=0, column=4, padx=10, pady=10)

        def update_area(*args):
            new_area = self._calculate_area(ancho_var.get(), largo_var.get())
            area_label.configure(text=f"{new_area:.2f}")
            self._update_project_stats()

        ancho_var.trace('w', update_area)
        largo_var.trace('w', update_area)

        self.area_widget_refs.append({
            'id': area_data['id_proyectos_areas'],
            'ancho_var': ancho_var,
            'largo_var': largo_var,
            'alto_var': alto_var
        })

        doors_windows_btn = ctk.CTkButton(
            row_frame, text="Puertas y Ventanas", height=35,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL, weight="bold"),
            fg_color=TRANSPARENT_BG, border_color=BORDER_PRIMARY, border_width=1,
            text_color=TEXT_SECONDARY, hover_color=self.colors.get('bg_secondary'),
            command=lambda data=area_data: self._open_doors_windows_manager(data)
        )
        doors_windows_btn.grid(row=0, column=5, padx=15, pady=10, sticky="e")

    def save_all_changes(self):
        """Recopila los datos de todas las filas y los guarda en la base de datos."""
        try:
            data_to_update = []
            for ref in self.area_widget_refs:
                data_to_update.append({
                    'id_proyectos_areas': ref['id'],
                    'ancho': float(ref['ancho_var'].get() or 0),
                    'largo': float(ref['largo_var'].get() or 0),
                    'alto': float(ref['alto_var'].get() or 0)
                })

            if not data_to_update:
                messagebox.showinfo("Información", "No hay áreas para guardar.")
                return

            self.supabase_client.table("proyectos_areas").upsert(data_to_update).execute()
            messagebox.showinfo("Éxito", "Todos los cambios han sido guardados correctamente.")
            self.load_project_areas()

        except ValueError:
            messagebox.showerror("Error de Validación", "Por favor, asegúrate de que todas las dimensiones sean números válidos.")
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudieron guardar los cambios: {e}")

    def _open_doors_windows_manager(self, area_data):
        DoorsWindowsManager(self, self.supabase_client, area_data)

    def _calculate_area(self, ancho_str, largo_str):
        try: return float(ancho_str or 0) * float(largo_str or 0)
        except ValueError: return 0

    def _format_date(self, date_str):
        if not date_str: return "N/A"
        try:
            from datetime import datetime
            return datetime.fromisoformat(date_str.replace('Z', '+00:00')).strftime("%d/%m/%Y")
        except: return "N/A"

    def _create_empty_areas_state(self):
        empty_frame = ctk.CTkFrame(self.areas_container, fg_color=TRANSPARENT_BG)
        empty_frame.pack(fill="both", expand=True, pady=50)
        ctk.CTkLabel(empty_frame, text="🏠", font=ctk.CTkFont(size=80)).pack(pady=(0, 15))
        ctk.CTkLabel(empty_frame, text="Este proyecto no tiene áreas asignadas", font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"), text_color=self.colors['text_primary']).pack(pady=(0, 5))
        ctk.CTkLabel(empty_frame, text="Las áreas te permiten organizar y calcular materiales\npor espacios específicos de tu proyecto", font=ctk.CTkFont(size=FONT_SIZE_NORMAL), text_color=self.colors['text_secondary'], justify="center").pack(pady=(0, 20))

    def _create_error_areas_state(self, error_msg):
        error_frame = ctk.CTkFrame(self.areas_container, fg_color=TRANSPARENT_BG)
        error_frame.pack(fill="both", expand=True, pady=50)
        ctk.CTkLabel(error_frame, text="⚠️", font=ctk.CTkFont(size=60), text_color=ERROR_COLOR).pack(pady=(0, 15))
        ctk.CTkLabel(error_frame, text="Error al cargar las áreas", font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 1, weight="bold"), text_color=ERROR_COLOR).pack(pady=(0, 10))
        ctk.CTkLabel(error_frame, text=error_msg, font=ctk.CTkFont(size=FONT_SIZE_SMALL), text_color=self.colors['text_secondary']).pack(pady=(0, 20))
        ctk.CTkButton(error_frame, text="🔄 Reintentar", command=self.load_project_areas, height=40, fg_color=ERROR_COLOR, hover_color="#DC2626").pack()

    def _show_add_area_info(self):
        messagebox.showinfo(
            "Agregar Áreas",
            "La funcionalidad para agregar áreas directamente desde aquí estará disponible pronto.\n\n" +
            "Por ahora, puedes crear 'Áreas Maestras' en su sección correspondiente desde el menú principal."
        )