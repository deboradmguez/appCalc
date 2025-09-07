# src/ui/pages/materiales_view.py

import customtkinter as ctk
from tkinter import messagebox
from config import (
    FONT_SIZE_TITLE, FONT_SIZE_NORMAL, FONT_SIZE_SMALL, 
    get_main_colors, BACKGROUND_CARD, ACCENT_PRIMARY, 
    ACCENT_HOVER, TEXT_PRIMARY, TEXT_SECONDARY, BORDER_PRIMARY,
    SUCCESS_COLOR, WARNING_COLOR, INFO_COLOR,TRANSPARENT_BG
)

class MaterialesView(ctk.CTkFrame):
    def __init__(self, master, master_app, **kwargs):
        colors = get_main_colors()
        super().__init__(master, fg_color=colors['bg_primary'], **kwargs)
        
        self.supabase_client = master_app.supabase_client
        self.materials_data = []
        self.colors = colors
        
        self._build_ui()
        self._load_materials_data()

    def _build_ui(self):
        """Construye la interfaz de usuario"""
        
        # === HEADER SECTION ===
        header_frame = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        header_frame.pack(fill="x", padx=0, pady=(0, 25))
        
        # Título con icono
        title_frame = ctk.CTkFrame(header_frame, fg_color=TRANSPARENT_BG)
        title_frame.pack(fill="x", pady=15)
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="🧱 Gestión de Materiales", 
            font=ctk.CTkFont(size=FONT_SIZE_TITLE, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title_label.pack(side="left", anchor="w")
        
        # Descripción
        desc_label = ctk.CTkLabel(
            title_frame, 
            text="Administra el catálogo de materiales de construcción", 
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1),
            text_color=self.colors['text_secondary']
        )
        desc_label.pack(side="left", anchor="w", padx=(20, 0))
        
        # === STATUS BANNER ===
        status_frame = ctk.CTkFrame(
            self,
            fg_color=INFO_COLOR,
            corner_radius=12,
            border_width=0
        )
        status_frame.pack(fill="x", padx=0, pady=(0, 25))
        
        status_content = ctk.CTkFrame(status_frame, fg_color=TRANSPARENT_BG)
        status_content.pack(fill="x", padx=20, pady=15)
        
        # Icono de construcción
        ctk.CTkLabel(
            status_content,
            text="🚧",
            font=ctk.CTkFont(size=24)
        ).pack(side="left", padx=(0, 15))
        
        # Mensaje de estado
        status_text_frame = ctk.CTkFrame(status_content, fg_color=TRANSPARENT_BG)
        status_text_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            status_text_frame,
            text="Módulo en Desarrollo",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"),
            text_color="white"
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            status_text_frame,
            text="Este módulo está siendo desarrollado y estará disponible próximamente",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
            text_color="white"
        ).pack(anchor="w")
        
        # === PREVIEW CONTENT ===
        self._create_preview_content()
        
        # === FOOTER INFO ===
        self._create_footer_info()

    def _create_preview_content(self):
        """Crea contenido de vista previa del módulo"""
        
        # Container principal
        preview_container = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        preview_container.pack(fill="both", expand=True, padx=0)
        
        # Grid layout
        preview_container.grid_columnconfigure(0, weight=1)
        preview_container.grid_columnconfigure(1, weight=1)
        preview_container.grid_rowconfigure(0, weight=1)
        preview_container.grid_rowconfigure(1, weight=1)
        
        # === TARJETA 1: CATÁLOGO DE MATERIALES ===
        catalog_card = self._create_feature_card(
            preview_container,
            title="📦 Catálogo de Materiales",
            description="Administra una base de datos completa de materiales de construcción con precios, proveedores y especificaciones técnicas.",
            features=[
                "• Gestión de categorías (Cemento, Acero, Madera, etc.)",
                "• Control de precios y proveedores",
                "• Especificaciones técnicas detalladas",
                "• Historial de precios y tendencias"
            ],
            color=ACCENT_PRIMARY
        )
        catalog_card.grid(row=0, column=0, padx=(0, 15), pady=(0, 15), sticky="nsew")
        
        # === TARJETA 2: CALCULADORA DE MATERIALES ===
        calculator_card = self._create_feature_card(
            preview_container,
            title="📊 Calculadora de Materiales",
            description="Calcula automáticamente las cantidades necesarias de materiales basado en las dimensiones de las áreas del proyecto.",
            features=[
                "• Cálculos automáticos por área",
                "• Fórmulas personalizables por tipo de construcción",
                "• Consideración de desperdicios y mermas",
                "• Reportes de cantidades y costos"
            ],
            color=SUCCESS_COLOR
        )
        calculator_card.grid(row=0, column=1, padx=(15, 0), pady=(0, 15), sticky="nsew")
        
        # === TARJETA 3: COTIZACIONES ===
        quotes_card = self._create_feature_card(
            preview_container,
            title="💰 Sistema de Cotizaciones",
            description="Genera cotizaciones automáticas basadas en los materiales calculados y los precios actualizados del catálogo.",
            features=[
                "• Generación automática de cotizaciones",
                "• Comparación de proveedores",
                "• Exportación a PDF y Excel",
                "• Seguimiento de cotizaciones enviadas"
            ],
            color=WARNING_COLOR
        )
        quotes_card.grid(row=1, column=0, padx=(0, 15), pady=(15, 0), sticky="nsew")
        
        # === TARJETA 4: CONTROL DE INVENTARIO ===
        inventory_card = self._create_feature_card(
            preview_container,
            title="📋 Control de Inventario",
            description="Lleva un control detallado del inventario de materiales, compras realizadas y materiales utilizados por proyecto.",
            features=[
                "• Registro de entradas y salidas",
                "• Control de stock mínimo",
                "• Alertas de reabastecimiento",
                "• Reportes de consumo por proyecto"
            ],
            color="#8B5CF6"  # Purple
        )
        inventory_card.grid(row=1, column=1, padx=(15, 0), pady=(15, 0), sticky="nsew")

    def _create_feature_card(self, parent, title, description, features, color):
        """Crea una tarjeta de característica"""
        
        card = ctk.CTkFrame(
            parent,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=2,
            border_color=color
        )
        
        # Header de la tarjeta
        header_frame = ctk.CTkFrame(card, fg_color=color, corner_radius=12)
        header_frame.pack(fill="x", padx=2, pady=2)
        
        # Título
        title_label = ctk.CTkLabel(
            header_frame,
            text=title,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 1, weight="bold"),
            text_color="white"
        )
        title_label.pack(pady=15)
        
        # Contenido
        content_frame = ctk.CTkFrame(card, fg_color=TRANSPARENT_BG)
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Descripción
        desc_label = ctk.CTkLabel(
            content_frame,
            text=description,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1),
            text_color=self.colors['text_primary'],
            wraplength=250,
            justify="left"
        )
        desc_label.pack(anchor="w", pady=(0, 15))
        
        # Características
        for feature in features:
            feature_label = ctk.CTkLabel(
                content_frame,
                text=feature,
                font=ctk.CTkFont(size=FONT_SIZE_SMALL),
                text_color=self.colors['text_secondary'],
                anchor="w",
                justify="left"
            )
            feature_label.pack(anchor="w", pady=2, fill="x")
        
        # Estado
        status_frame = ctk.CTkFrame(content_frame, fg_color="#FEF3C7", corner_radius=8)
        status_frame.pack(fill="x", pady=(15, 0))
        
        ctk.CTkLabel(
            status_frame,
            text="⏳ Próximamente disponible",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL, weight="bold"),
            text_color="#92400E"
        ).pack(pady=8)
        
        return card

    def _create_footer_info(self):
        """Crea la información del pie de página"""
        
        footer_frame = ctk.CTkFrame(
            self,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        footer_frame.pack(fill="x", padx=0, pady=(25, 0))
        
        footer_content = ctk.CTkFrame(footer_frame, fg_color=TRANSPARENT_BG)
        footer_content.pack(fill="x", padx=30, pady=20)
        
        # Icono de información
        info_frame = ctk.CTkFrame(footer_content, fg_color=TRANSPARENT_BG)
        info_frame.pack(anchor="w")
        
        ctk.CTkLabel(
            info_frame,
            text="💡",
            font=ctk.CTkFont(size=20)
        ).pack(side="left", padx=(0, 10))
        
        # Texto informativo
        info_text_frame = ctk.CTkFrame(info_frame, fg_color=TRANSPARENT_BG)
        info_text_frame.pack(side="left", fill="x", expand=True)
        
        ctk.CTkLabel(
            info_text_frame,
            text="¿Tienes sugerencias para el módulo de materiales?",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            info_text_frame,
            text="Tu feedback es importante para nosotros. Comparte tus ideas sobre qué funcionalidades te gustaría ver en este módulo.",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary']
        ).pack(anchor="w", pady=(5, 0))
        
        # Botón de feedback
        feedback_btn = ctk.CTkButton(
            footer_content,
            text="📝 Enviar Sugerencias",
            command=self._show_feedback_dialog,
            height=40,
            width=180,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"),
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_HOVER,
            corner_radius=10
        )
        feedback_btn.pack(side="right", padx=(20, 0))

    def _load_materials_data(self):
        """Carga los datos de materiales (placeholder)"""
        # Por ahora, esto es solo un placeholder
        # En el futuro aquí se cargarían los datos reales
        pass

    def _show_feedback_dialog(self):
        """Muestra un diálogo para enviar feedback"""
        
        # Crear ventana de diálogo
        dialog = ctk.CTkToplevel(self)
        dialog.title("Enviar Sugerencias - Módulo de Materiales")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        # Título
        title_label = ctk.CTkLabel(
            dialog,
            text="💡 Comparte tus Ideas",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 4, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title_label.pack(pady=(20, 10))
        
        # Descripción
        desc_label = ctk.CTkLabel(
            dialog,
            text="¿Qué funcionalidades te gustaría ver en el módulo de materiales?",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
            text_color=self.colors['text_secondary']
        )
        desc_label.pack(pady=(0, 20))
        
        # Área de texto
        feedback_text = ctk.CTkTextbox(
            dialog,
            height=200,
            corner_radius=10,
            border_width=2,
            border_color=BORDER_PRIMARY,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL)
        )
        feedback_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Placeholder text
        feedback_text.insert("1.0", "Ejemplo:\n• Me gustaría poder importar precios desde Excel\n• Sería útil tener alertas de stock bajo\n• Necesito poder categorizar materiales por proveedor\n\nEscribe aquí tus sugerencias...")
        
        # Botones
        button_frame = ctk.CTkFrame(dialog, fg_color=TRANSPARENT_BG)
        button_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=dialog.destroy,
            height=40,
            width=100,
            fg_color=TRANSPARENT_BG,
            hover_color=BORDER_PRIMARY,
            text_color=self.colors['text_secondary'],
            border_width=2,
            border_color=BORDER_PRIMARY
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        send_btn = ctk.CTkButton(
            button_frame,
            text="📤 Enviar",
            command=lambda: self._send_feedback(feedback_text.get("1.0", "end-1c"), dialog),
            height=40,
            width=100,
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_HOVER
        )
        send_btn.pack(side="right")

    def _send_feedback(self, feedback_text, dialog):
        """Envía el feedback (placeholder)"""
        
        if not feedback_text.strip() or "Escribe aquí tus sugerencias..." in feedback_text:
            messagebox.showwarning("Advertencia", "Por favor, escribe tus sugerencias antes de enviar.")
            return
        
        # En una implementación real, aquí guardarías el feedback en la base de datos
        # Por ahora, solo mostramos un mensaje
        messagebox.showinfo(
            "¡Gracias por tu Feedback!",
            "Tus sugerencias han sido registradas.\n\nLas consideraremos para futuras versiones del módulo de materiales."
        )
        
        dialog.destroy()