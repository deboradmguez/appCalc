# src/ui/pages/proyectos_page.py

import customtkinter as ctk
import logging
from config import (
    FONT_SIZE_TITLE, FONT_SIZE_NORMAL, FONT_SIZE_SMALL, 
    get_main_colors, BACKGROUND_CARD, ACCENT_PRIMARY, 
    ACCENT_HOVER, TEXT_PRIMARY, TEXT_SECONDARY, BORDER_PRIMARY, TRANSPARENT_BG 
)

class ProyectosPage(ctk.CTkFrame):
    def __init__(self, master, master_app, on_create_new, on_view_details, **kwargs):
        colors = get_main_colors()
        
        super().__init__(master, fg_color=colors['bg_primary'], **kwargs)
        
        self.supabase_client = master_app.supabase_client
        self.on_create_new = on_create_new
        self.on_view_details = on_view_details
        self.colors = colors
        
        self._build_ui()
        self.load_proyectos_list()

    def _build_ui(self):
        """Construye la interfaz de usuario con el nuevo diseño"""
        
        # === HEADER SECTION ===
        header_container = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG )
        header_container.pack(fill="x", padx=0, pady=(0, 20))
        
        # Título principal con estilo mejorado
        title_frame = ctk.CTkFrame(header_container, fg_color=TRANSPARENT_BG )
        title_frame.pack(fill="x", padx=0, pady=10)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="📁 Mis Proyectos de Construcción", 
            font=ctk.CTkFont(size=FONT_SIZE_TITLE + 2, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title_label.pack(side="left", anchor="w")
        
        # Subtitle con información adicional
        subtitle_label = ctk.CTkLabel(
            title_frame, 
            text="Gestiona y administra todos tus proyectos de construcción", 
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1),
            text_color=self.colors['text_secondary']
        )
        subtitle_label.pack(side="left", anchor="w", padx=(20, 0))
        
        # Botón crear proyecto con estilo mejorado
        btn_crear_proyecto = ctk.CTkButton(
            title_frame, 
            text="+ Crear Nuevo Proyecto", 
            command=self.on_create_new, 
            height=45,
            width=200,
            corner_radius=10,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_HOVER,
            text_color="white"
        )
        btn_crear_proyecto.pack(side="right", padx=10)
        
        # Separador visual
        separator = ctk.CTkFrame(
            header_container, 
            height=2, 
            fg_color=BORDER_PRIMARY
        )
        separator.pack(fill="x", padx=0, pady=(10, 0))
        
        # === STATS SECTION (Opcional - información rápida) ===
        self.stats_frame = ctk.CTkFrame(
            self, 
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        self.stats_frame.pack(fill="x", padx=0, pady=(0, 20))
        
        # === CONTENT SECTION ===
        content_label = ctk.CTkLabel(
            self,
            text="Lista de Proyectos",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"),
            text_color=self.colors['text_primary']
        )
        content_label.pack(anchor="w", padx=5, pady=(0, 10))
        
        # Container principal para la lista con scroll
        self.proyectos_list_frame = ctk.CTkScrollableFrame(
            self, 
            fg_color=TRANSPARENT_BG ,
            corner_radius=0
        )
        self.proyectos_list_frame.pack(fill="both", expand=True, padx=0, pady=0)

    def _create_stats_section(self, total_proyectos):
        """Crea una sección de estadísticas rápidas"""
        
        # Limpiar stats frame
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
            
        stats_content = ctk.CTkFrame(self.stats_frame, fg_color=TRANSPARENT_BG )
        stats_content.pack(fill="x", padx=20, pady=15)
        
        # Total de proyectos
        total_frame = ctk.CTkFrame(stats_content, fg_color=TRANSPARENT_BG )
        total_frame.pack(side="left", padx=(0, 30))
        
        ctk.CTkLabel(
            total_frame,
            text=str(total_proyectos),
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=ACCENT_PRIMARY
        ).pack()
        
        ctk.CTkLabel(
            total_frame,
            text="Proyectos Totales",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary']
        ).pack()
        
        # Proyectos activos (placeholder - podrías implementar un campo de estado)
        active_frame = ctk.CTkFrame(stats_content, fg_color=TRANSPARENT_BG )
        active_frame.pack(side="left", padx=(0, 30))
        
        ctk.CTkLabel(
            active_frame,
            text=str(total_proyectos),  # Por ahora, todos son "activos"
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#10B981"  # Verde para activos
        ).pack()
        
        ctk.CTkLabel(
            active_frame,
            text="Proyectos Activos",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary']
        ).pack()

    def load_proyectos_list(self):
        """Carga la lista de proyectos con diseño mejorado"""
        
        # Limpiar lista actual
        for widget in self.proyectos_list_frame.winfo_children(): 
            widget.destroy()
            
        try:
            proyectos = self.supabase_client.table("proyectos").select("*").order("fecha_creacion", desc=True).execute().data
            
            # Actualizar stats
            self._create_stats_section(len(proyectos))
            
            if not proyectos:
                self._create_empty_state()
            else:
                for i, proyecto in enumerate(proyectos):
                    self._create_project_card(proyecto, i)
                    
        except Exception as e:
            logging.error(f"Error al cargar proyectos: {e}")
            self._create_error_state(str(e))

    def _create_empty_state(self):
        """Crea el estado vacío cuando no hay proyectos"""
        
        empty_frame = ctk.CTkFrame(
            self.proyectos_list_frame,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        empty_frame.pack(fill="x", pady=20, padx=10)
        
        # Icono grande
        icon_label = ctk.CTkLabel(
            empty_frame,
            text="🏗️",
            font=ctk.CTkFont(size=80)
        )
        icon_label.pack(pady=(40, 10))
        
        # Mensaje principal
        ctk.CTkLabel(
            empty_frame,
            text="¡Comienza tu primer proyecto!",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 4, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=(0, 5))
        
        # Mensaje secundario
        ctk.CTkLabel(
            empty_frame,
            text="No tienes proyectos todavía. Crea tu primer proyecto de construcción\npara comenzar a gestionar materiales y áreas.",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
            text_color=self.colors['text_secondary'],
            justify="center"
        ).pack(pady=(0, 20))
        
        # Botón de acción
        btn_crear = ctk.CTkButton(
            empty_frame,
            text="+ Crear Mi Primer Proyecto",
            command=self.on_create_new,
            height=45,
            width=250,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_HOVER,
            corner_radius=10
        )
        btn_crear.pack(pady=(0, 40))

    def _create_error_state(self, error_message):
        """Crea el estado de error"""
        
        error_frame = ctk.CTkFrame(
            self.proyectos_list_frame,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=2,
            border_color="#EF4444"
        )
        error_frame.pack(fill="x", pady=20, padx=10)
        
        ctk.CTkLabel(
            error_frame,
            text="⚠️ Error al cargar proyectos",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"),
            text_color="#EF4444"
        ).pack(pady=(20, 5))
        
        ctk.CTkLabel(
            error_frame,
            text=f"Error: {error_message}",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary']
        ).pack(pady=(0, 10))
        
        ctk.CTkButton(
            error_frame,
            text="🔄 Reintentar",
            command=self.load_proyectos_list,
            height=35,
            fg_color="#EF4444",
            hover_color="#DC2626"
        ).pack(pady=(0, 20))

    def _create_project_card(self, proyecto, index):
        """Crea una tarjeta individual para cada proyecto"""
        
        # Card container con efecto hover
        card_frame = ctk.CTkFrame(
            self.proyectos_list_frame,
            fg_color=BACKGROUND_CARD,
            corner_radius=12,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        card_frame.pack(fill="x", pady=8, padx=5)
        
        # Content container
        content_frame = ctk.CTkFrame(card_frame, fg_color=TRANSPARENT_BG )
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Left side - Project info
        info_frame = ctk.CTkFrame(content_frame, fg_color=TRANSPARENT_BG )
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Project title
        title_label = ctk.CTkLabel(
            info_frame,
            text=proyecto['nombre_proyecto'],
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"),
            text_color=self.colors['text_primary'],
            anchor="w"
        )
        title_label.pack(anchor="w", pady=(0, 5))
        
        # Project address
        if proyecto.get('direccion_proyecto'):
            address_label = ctk.CTkLabel(
                info_frame,
                text=f"📍 {proyecto['direccion_proyecto']}",
                font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1),
                text_color=self.colors['text_secondary'],
                anchor="w"
            )
            address_label.pack(anchor="w", pady=(0, 5))
        
        # Project metadata
        metadata_frame = ctk.CTkFrame(info_frame, fg_color=TRANSPARENT_BG )
        metadata_frame.pack(anchor="w", pady=(5, 0))
        
        # Fecha de creación
        if proyecto.get('fecha_creacion'):
            try:
                from datetime import datetime
                fecha = datetime.fromisoformat(proyecto['fecha_creacion'].replace('Z', '+00:00'))
                fecha_str = fecha.strftime("%d/%m/%Y")
                
                fecha_label = ctk.CTkLabel(
                    metadata_frame,
                    text=f"📅 Creado: {fecha_str}",
                    font=ctk.CTkFont(size=FONT_SIZE_SMALL),
                    text_color=self.colors['text_secondary']
                )
                fecha_label.pack(side="left", padx=(0, 20))
            except:
                pass
        
        # Status badge (placeholder - puedes implementar estados)
        status_badge = ctk.CTkLabel(
            metadata_frame,
            text="🟢 Activo",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color="#10B981",
            fg_color="#F0FDF4",
            corner_radius=12,
            padx=10,
            pady=4
        )
        status_badge.pack(side="left")
        
        # Right side - Actions
        actions_frame = ctk.CTkFrame(content_frame, fg_color=TRANSPARENT_BG )
        actions_frame.pack(side="right", padx=(20, 0))
        
        # Primary action button
        btn_administrar = ctk.CTkButton(
            actions_frame,
            text="📋 Administrar",
            command=lambda p=proyecto: self.on_view_details(p),
            height=40,
            width=140,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_HOVER,
            corner_radius=8
        )
        btn_administrar.pack(pady=(0, 8))
        
        # Secondary action button
        btn_editar = ctk.CTkButton(
            actions_frame,
            text="✏️ Editar",
            command=lambda p=proyecto: self._edit_project(p),
            height=35,
            width=140,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1),
            fg_color=TRANSPARENT_BG ,
            hover_color=BORDER_PRIMARY,
            text_color=self.colors['text_secondary'],
            border_width=1,
            border_color=BORDER_PRIMARY,
            corner_radius=8
        )
        btn_editar.pack()
        
        # Hover effect (placeholder - puedes implementar con eventos)
        self._add_hover_effect(card_frame)

    def _add_hover_effect(self, card_frame):
        """Agrega efecto hover a las tarjetas (placeholder)"""
        # Puedes implementar efectos de hover aquí
        # Por ejemplo, cambiar el color del borde o agregar sombra
        pass
    
    def _edit_project(self, proyecto):
        """Maneja la edición de proyectos (placeholder)"""
        # Aquí podrías abrir un diálogo de edición
        logging.info(f"Editar proyecto: {proyecto['nombre_proyecto']}")
        # Por ahora, solo mostrar un mensaje
        from tkinter import messagebox
        messagebox.showinfo("Info", f"Edición de '{proyecto['nombre_proyecto']}' próximamente disponible.")