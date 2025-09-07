# src/ui/pages/project_detail_page.py

import customtkinter as ctk
from tkinter import messagebox
from config import (
    FONT_SIZE_TITLE, FONT_SIZE_NORMAL, FONT_SIZE_SMALL, 
    get_main_colors, BACKGROUND_CARD, ACCENT_PRIMARY, 
    ACCENT_HOVER, TEXT_PRIMARY, TEXT_SECONDARY, BORDER_PRIMARY,
    SUCCESS_COLOR, ERROR_COLOR, WARNING_COLOR,TRANSPARENT_BG
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

        self.build_ui()

    def build_ui(self):
        """Construye la interfaz de usuario principal"""
        
        # === HEADER SECTION ===
        self._create_header()
        
        # === PROJECT INFO SECTION ===
        self._create_project_info_section()
        
        # === AREAS SECTION ===
        self._create_areas_section()

    def _create_header(self):
        """Crea la sección del header"""
        
        header_frame = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        header_frame.pack(fill="x", padx=0, pady=(0, 25))
        
        # Botón volver
        back_btn = ctk.CTkButton(
            header_frame,
            text="← Volver a Proyectos",
            command=self.on_back,
            height=40,
            width=160,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            fg_color=TRANSPARENT_BG,
            hover_color=BORDER_PRIMARY,
            text_color=self.colors['text_primary'],
            border_width=2,
            border_color=BORDER_PRIMARY,
            corner_radius=10
        )
        back_btn.pack(side="left", pady=10)
        
        # Título del proyecto
        title_frame = ctk.CTkFrame(header_frame, fg_color=TRANSPARENT_BG)
        title_frame.pack(side="left", fill="x", expand=True, padx=(20, 0))
        
        project_title = ctk.CTkLabel(
            title_frame,
            text=f"🏗️ {self.proyecto['nombre_proyecto']}",
            font=ctk.CTkFont(size=FONT_SIZE_TITLE + 2, weight="bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        project_title.pack(anchor="w")
        
        # Dirección si existe
        if self.proyecto.get('direccion_proyecto'):
            address_label = ctk.CTkLabel(
                title_frame,
                text=f"📍 {self.proyecto['direccion_proyecto']}",
                font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
                text_color=self.colors['text_secondary'],
                anchor="w"
            )
            address_label.pack(anchor="w", pady=(5, 0))

    def _create_project_info_section(self):
        """Crea la sección de información del proyecto"""
        
        info_card = ctk.CTkFrame(
            self,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        info_card.pack(fill="x", padx=0, pady=(0, 25))
        
        # Header de la tarjeta
        card_header = ctk.CTkFrame(info_card, fg_color=TRANSPARENT_BG)
        card_header.pack(fill="x", padx=25, pady=(20, 15))
        
        ctk.CTkLabel(
            card_header,
            text="📊 Resumen del Proyecto",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(side="left")
        
        # Contenido de información
        info_content = ctk.CTkFrame(info_card, fg_color=TRANSPARENT_BG)
        info_content.pack(fill="x", padx=25, pady=(0, 20))
        
        # Grid layout para la información
        info_content.grid_columnconfigure(0, weight=1)
        info_content.grid_columnconfigure(1, weight=1)
        info_content.grid_columnconfigure(2, weight=1)
        
        # Estadísticas del proyecto
        self._create_stat_item(info_content, "📋", "Áreas Totales", "...", 0, 0)
        self._create_stat_item(info_content, "📏", "Área Total (m²)", "...", 0, 1)
        self._create_stat_item(info_content, "📅", "Fecha Creación", self._format_date(self.proyecto.get('fecha_creacion')), 0, 2)

    def _create_stat_item(self, parent, icon, label, value, row, col):
        """Crea un elemento de estadística"""
        
        stat_frame = ctk.CTkFrame(parent, fg_color="#F8FAFC", corner_radius=10)
        stat_frame.grid(row=row, column=col, padx=10, pady=5, sticky="ew")
        
        # Contenido
        content = ctk.CTkFrame(stat_frame, fg_color=TRANSPARENT_BG)
        content.pack(fill="x", padx=15, pady=15)
        
        # Icono
        icon_label = ctk.CTkLabel(
            content,
            text=icon,
            font=ctk.CTkFont(size=20)
        )
        icon_label.pack(pady=(0, 5))
        
        # Valor
        value_label = ctk.CTkLabel(
            content,
            text=str(value),
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"),
            text_color=ACCENT_PRIMARY
        )
        value_label.pack()
        
        # Etiqueta
        label_label = ctk.CTkLabel(
            content,
            text=label,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary']
        )
        label_label.pack(pady=(2, 0))
        
        return stat_frame

    def _create_areas_section(self):
        """Crea la sección de áreas del proyecto"""
        
        # Header de la sección
        areas_header = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        areas_header.pack(fill="x", padx=0, pady=(0, 15))
        
        title_label = ctk.CTkLabel(
            areas_header,
            text="🏠 Áreas del Proyecto",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 3, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title_label.pack(side="left")
        
        # Botón agregar área (para futuras implementaciones)
        add_area_btn = ctk.CTkButton(
            areas_header,
            text="+ Agregar Área",
            height=35,
            width=130,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"),
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_HOVER,
            corner_radius=8,
            command=self._show_add_area_info
        )
        add_area_btn.pack(side="right")
        
        # Container scrollable para las áreas
        self.areas_container = ctk.CTkScrollableFrame(
            self,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        self.areas_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Cargar las áreas
        self.load_project_areas()

    def load_project_areas(self):
        """Carga las áreas del proyecto"""
        
        # Limpiar contenedor
        for widget in self.areas_container.winfo_children():
            widget.destroy()
        
        try:
            # Obtener áreas del proyecto
            self.project_areas = self.supabase_client.table("proyectos_areas").select(
                "*, areas_maestro(nombre_area)"
            ).eq("proyecto_id", self.proyecto['id_proyecto']).execute().data
            
            # Actualizar estadísticas
            self._update_project_stats()
            
            if not self.project_areas:
                self._create_empty_areas_state()
            else:
                self._create_areas_table_header()
                for area_data in self.project_areas:
                    self._create_area_row(area_data)
                
        except Exception as e:
            self._create_error_areas_state(str(e))
            messagebox.showerror("Error", f"No se pudieron cargar las áreas del proyecto: {e}")

    def _update_project_stats(self):
        """Actualiza las estadísticas del proyecto"""
        
        total_areas = len(self.project_areas)
        total_area_m2 = 0
        
        for area in self.project_areas:
            ancho = float(area.get('ancho', 0) or 0)
            largo = float(area.get('largo', 0) or 0)
            total_area_m2 += ancho * largo
        
        # Actualizar los valores (necesitaríamos referencias a los widgets)
        # Por simplicidad, aquí podrías reconstruir la sección de info
        # o mantener referencias a los labels de estadísticas

    def _create_empty_areas_state(self):
        """Crea el estado vacío cuando no hay áreas"""
        
        empty_frame = ctk.CTkFrame(self.areas_container, fg_color=TRANSPARENT_BG)
        empty_frame.pack(fill="both", expand=True, pady=50)
        
        # Icono
        ctk.CTkLabel(
            empty_frame,
            text="🏠",
            font=ctk.CTkFont(size=80)
        ).pack(pady=(0, 15))
        
        # Mensaje principal
        ctk.CTkLabel(
            empty_frame,
            text="Este proyecto no tiene áreas asignadas",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=(0, 5))
        
        # Mensaje secundario
        ctk.CTkLabel(
            empty_frame,
            text="Las áreas te permiten organizar y calcular materiales\npor espacios específicos de tu proyecto",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
            text_color=self.colors['text_secondary'],
            justify="center"
        ).pack(pady=(0, 20))
        
        # Botón de acción
        ctk.CTkButton(
            empty_frame,
            text="📋 Administrar Áreas Maestras",
            command=self._go_to_areas_management,
            height=45,
            width=250,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_HOVER,
            corner_radius=10
        ).pack()

    def _create_error_areas_state(self, error_msg):
        """Crea el estado de error"""
        
        error_frame = ctk.CTkFrame(self.areas_container, fg_color=TRANSPARENT_BG)
        error_frame.pack(fill="both", expand=True, pady=50)
        
        ctk.CTkLabel(
            error_frame,
            text="⚠️",
            font=ctk.CTkFont(size=60),
            text_color=ERROR_COLOR
        ).pack(pady=(0, 15))
        
        ctk.CTkLabel(
            error_frame,
            text="Error al cargar las áreas",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 1, weight="bold"),
            text_color=ERROR_COLOR
        ).pack(pady=(0, 10))
        
        ctk.CTkLabel(
            error_frame,
            text=error_msg,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary']
        ).pack(pady=(0, 20))
        
        ctk.CTkButton(
            error_frame,
            text="🔄 Reintentar",
            command=self.load_project_areas,
            height=40,
            fg_color=ERROR_COLOR,
            hover_color="#DC2626"
        ).pack()

    def _create_areas_table_header(self):
        """Crea el header de la tabla de áreas"""
        
        header_frame = ctk.CTkFrame(
            self.areas_container,
            fg_color="#F1F5F9",
            corner_radius=10,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        header_frame.pack(fill="x", pady=(15, 5), padx=20)
        
        # Configurar grid
        header_frame.grid_columnconfigure(0, weight=3)  # Área
        header_frame.grid_columnconfigure(1, weight=1)  # Ancho
        header_frame.grid_columnconfigure(2, weight=1)  # Largo  
        header_frame.grid_columnconfigure(3, weight=1)  # Alto
        header_frame.grid_columnconfigure(4, weight=1)  # Área m²
        header_frame.grid_columnconfigure(5, weight=1)  # Acciones
        
        headers = ["🏠 Área", "📏 Ancho (m)", "📏 Largo (m)", "📏 Alto (m)", "📐 Área (m²)", "⚙️ Acciones"]
        
        for i, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(
                header_frame,
                text=header_text,
                font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"),
                text_color=self.colors['text_primary']
            )
            header_label.grid(row=0, column=i, sticky="w", padx=15, pady=12)

    def _create_area_row(self, area_data):
        """Crea una fila para cada área"""
        
        row_frame = ctk.CTkFrame(
            self.areas_container,
            fg_color="white",
            corner_radius=8,
            border_width=1,
            border_color="#E2E8F0"
        )
        row_frame.pack(fill="x", pady=2, padx=20)
        
        # Configurar grid con los mismos pesos que el header
        for i in range(6):
            if i == 0:
                row_frame.grid_columnconfigure(i, weight=3)
            else:
                row_frame.grid_columnconfigure(i, weight=1)
        
        # Nombre del área
        area_name = ctk.CTkLabel(
            row_frame,
            text=area_data['areas_maestro']['nombre_area'],
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        area_name.grid(row=0, column=0, sticky="w", padx=15, pady=15)
        
        # Variables para las dimensiones
        ancho_var = ctk.StringVar(value=str(area_data.get('ancho', '') or ''))
        largo_var = ctk.StringVar(value=str(area_data.get('largo', '') or ''))
        alto_var = ctk.StringVar(value=str(area_data.get('alto', '') or ''))
        
        # Campos de entrada para dimensiones
        ancho_entry = ctk.CTkEntry(
            row_frame,
            textvariable=ancho_var,
            width=80,
            height=35,
            corner_radius=6,
            border_width=1,
            border_color=BORDER_PRIMARY,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1)
        )
        ancho_entry.grid(row=0, column=1, padx=10, pady=10)
        
        largo_entry = ctk.CTkEntry(
            row_frame,
            textvariable=largo_var,
            width=80,
            height=35,
            corner_radius=6,
            border_width=1,
            border_color=BORDER_PRIMARY,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1)
        )
        largo_entry.grid(row=0, column=2, padx=10, pady=10)
        
        alto_entry = ctk.CTkEntry(
            row_frame,
            textvariable=alto_var,
            width=80,
            height=35,
            corner_radius=6,
            border_width=1,
            border_color=BORDER_PRIMARY,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1)
        )
        alto_entry.grid(row=0, column=3, padx=10, pady=10)
        
        # Área calculada
        area_m2 = self._calculate_area(ancho_var.get(), largo_var.get())
        area_label = ctk.CTkLabel(
            row_frame,
            text=f"{area_m2:.2f}",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"),
            text_color=ACCENT_PRIMARY
        )
        area_label.grid(row=0, column=4, padx=10, pady=10)
        
        # Actualizar área cuando cambien las dimensiones
        def update_area(*args):
            new_area = self._calculate_area(ancho_var.get(), largo_var.get())
            area_label.configure(text=f"{new_area:.2f}")
        
        ancho_var.trace('w', update_area)
        largo_var.trace('w', update_area)
        
        # Botón guardar
        save_btn = ctk.CTkButton(
            row_frame,
            text="💾 Guardar",
            width=90,
            height=35,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL, weight="bold"),
            fg_color=SUCCESS_COLOR,
            hover_color="#059669",
            corner_radius=6,
            command=lambda: self.save_area_dimensions(
                area_data['id_proyectos_areas'], 
                ancho_var, largo_var, alto_var,
                save_btn
            )
        )
        save_btn.grid(row=0, column=5, padx=10, pady=10)

    def _calculate_area(self, ancho_str, largo_str):
        """Calcula el área basada en ancho y largo"""
        try:
            ancho = float(ancho_str) if ancho_str else 0
            largo = float(largo_str) if largo_str else 0
            return ancho * largo
        except ValueError:
            return 0

    def save_area_dimensions(self, area_id, ancho_var, largo_var, alto_var, save_btn):
        """Guarda las dimensiones del área"""
        
        # Cambiar estado del botón
        save_btn.configure(text="💾 Guardando...", state="disabled")
        
        try:
            # Validar datos
            ancho = float(ancho_var.get()) if ancho_var.get() else 0
            largo = float(largo_var.get()) if largo_var.get() else 0  
            alto = float(alto_var.get()) if alto_var.get() else 0
            
            # Actualizar en la base de datos
            update_data = {
                "ancho": ancho,
                "largo": largo, 
                "alto": alto
            }
            
            self.supabase_client.table("proyectos_areas").update(update_data).eq(
                "id_proyectos_areas", area_id
            ).execute()
            
            # Feedback visual
            save_btn.configure(text="✅ Guardado", fg_color=SUCCESS_COLOR)
            
            # Restaurar botón después de 2 segundos
            self.after(2000, lambda: save_btn.configure(
                text="💾 Guardar", 
                state="normal",
                fg_color=SUCCESS_COLOR
            ))
            
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")
            save_btn.configure(text="💾 Guardar", state="normal")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron guardar las dimensiones: {e}")
            save_btn.configure(text="💾 Guardar", state="normal")

    def _format_date(self, date_str):
        """Formatea una fecha para mostrar"""
        if not date_str:
            return "No disponible"
        
        try:
            from datetime import datetime
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return date.strftime("%d/%m/%Y")
        except:
            return "No disponible"

    def _show_add_area_info(self):
        """Muestra información sobre cómo agregar áreas"""
        messagebox.showinfo(
            "Agregar Áreas",
            "Para agregar áreas a tu proyecto:\n\n" +
            "1. Ve a la sección 'Áreas' desde el menú principal\n" +
            "2. Crea las áreas maestras que necesites\n" +
            "3. Luego podrás asignarlas a tus proyectos\n\n" +
            "Esta funcionalidad será mejorada en próximas versiones."
        )

    def _go_to_areas_management(self):
        """Navega a la gestión de áreas (placeholder)"""
        # Aquí podrías implementar navegación directa a áreas
        messagebox.showinfo(
            "Navegación",
            "Usa el menú lateral para ir a la sección 'Áreas' y gestionar las áreas maestras."
        )