# src/ui/pages/configuracion_view.py

import customtkinter as ctk
from tkinter import messagebox
from config import (
    FONT_SIZE_TITLE, FONT_SIZE_NORMAL, FONT_SIZE_SMALL, 
    get_main_colors, BACKGROUND_CARD, ACCENT_PRIMARY, 
    ACCENT_HOVER, TEXT_PRIMARY, TEXT_SECONDARY, BORDER_PRIMARY,
    SUCCESS_COLOR, ERROR_COLOR, WARNING_COLOR, INFO_COLOR, 
    NEUTRAL_COLOR, TRANSPARENT_BG, TRANSPARENT_HOVER
)

class ConfiguracionView(ctk.CTkFrame):
    def __init__(self, master, master_app, on_logout, **kwargs):
        colors = get_main_colors()
        super().__init__(master, fg_color=colors['bg_primary'], **kwargs)
        
        self.on_logout = on_logout
        self.master_app = master_app
        self.colors = colors
        
        self._build_ui()

    def _build_ui(self):
        """Construye la interfaz de usuario"""
        
        # === HEADER SECTION ===
        header_frame = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        header_frame.pack(fill="x", padx=0, pady=(0, 25))
        
        # Título principal
        title_label = ctk.CTkLabel(
            header_frame, 
            text="⚙️ Configuración de la Aplicación", 
            font=ctk.CTkFont(size=FONT_SIZE_TITLE, weight="bold"),
            text_color=self.colors['text_primary']
        )
        title_label.pack(side="left", anchor="w", pady=15)
        
        # Descripción
        desc_label = ctk.CTkLabel(
            header_frame, 
            text="Personaliza tu experiencia y gestiona tu cuenta", 
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1),
            text_color=self.colors['text_secondary']
        )
        desc_label.pack(side="left", anchor="w", padx=(20, 0))
        
        # === MAIN CONTENT GRID ===
        main_container = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        main_container.pack(fill="both", expand=True, padx=0)
        
        # Grid layout
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_columnconfigure(1, weight=1)
        main_container.grid_rowconfigure(0, weight=0)
        main_container.grid_rowconfigure(1, weight=0)
        main_container.grid_rowconfigure(2, weight=1)
        
        # === ACCOUNT SECTION ===
        self._create_account_section(main_container, 0, 0)
        
        # === APP PREFERENCES SECTION ===
        self._create_preferences_section(main_container, 0, 1)
        
        # === SYSTEM INFO SECTION ===
        self._create_system_info_section(main_container, 1, 0)
        
        # === SUPPORT SECTION ===
        self._create_support_section(main_container, 1, 1)

    def _create_account_section(self, parent, row, col):
        """Crea la sección de cuenta de usuario"""
        
        account_card = ctk.CTkFrame(
            parent,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        account_card.grid(row=row, column=col, padx=(0, 15), pady=(0, 15), sticky="nsew")
        
        # Header
        self._create_section_header(account_card, "👤", "Cuenta de Usuario")
        
        # Content
        content_frame = ctk.CTkFrame(account_card, fg_color=TRANSPARENT_BG)
        content_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        
        # User info (placeholder - you'd get this from auth service)
        user_info_frame = ctk.CTkFrame(content_frame, fg_color="#F8FAFC", corner_radius=10)
        user_info_frame.pack(fill="x", pady=(0, 15))
        
        user_content = ctk.CTkFrame(user_info_frame, fg_color=TRANSPARENT_BG)
        user_content.pack(fill="x", padx=15, pady=15)
        
        # Email (placeholder)
        ctk.CTkLabel(
            user_content,
            text="📧 Email:",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL, weight="bold"),
            text_color=self.colors['text_secondary']
        ).pack(anchor="w")
        
        ctk.CTkLabel(
            user_content,
            text="usuario@ejemplo.com",  # Placeholder
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
            text_color=self.colors['text_primary']
        ).pack(anchor="w", pady=(2, 10))
        
        # Session status
        ctk.CTkLabel(
            user_content,
            text="🟢 Sesión activa",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=SUCCESS_COLOR
        ).pack(anchor="w")
        
        # Account actions
        actions_frame = ctk.CTkFrame(content_frame, fg_color=TRANSPARENT_BG)
        actions_frame.pack(fill="x")
        
        # Change password button (placeholder)
        change_password_btn = ctk.CTkButton(
            actions_frame,
            text="🔑 Cambiar Contraseña",
            command=self._show_change_password_info,
            height=40,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            fg_color=TRANSPARENT_BG,
            hover_color=TRANSPARENT_HOVER,
            text_color=self.colors['text_primary'],
            border_width=2,
            border_color=BORDER_PRIMARY,
            corner_radius=8
        )
        change_password_btn.pack(fill="x", pady=(0, 10))
        
        # Logout button
        logout_btn = ctk.CTkButton(
            actions_frame,
            text="🚪 Cerrar Sesión",
            command=self._confirm_logout,
            height=45,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            fg_color=ERROR_COLOR,
            hover_color="#DC2626",
            corner_radius=8
        )
        logout_btn.pack(fill="x")

    def _create_preferences_section(self, parent, row, col):
        """Crea la sección de preferencias"""
        
        prefs_card = ctk.CTkFrame(
            parent,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        prefs_card.grid(row=row, column=col, padx=(15, 0), pady=(0, 15), sticky="nsew")
        
        # Header
        self._create_section_header(prefs_card, "🎨", "Preferencias")
        
        # Content
        content_frame = ctk.CTkFrame(prefs_card, fg_color=TRANSPARENT_BG)
        content_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        
        # Theme selection
        theme_frame = ctk.CTkFrame(content_frame, fg_color=TRANSPARENT_BG)
        theme_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            theme_frame,
            text="🌙 Tema de la aplicación:",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w", pady=(0, 8))
        
        theme_combo = ctk.CTkComboBox(
            theme_frame,
            values=["Claro", "Oscuro", "Sistema"],
            state="readonly",
            height=40,
            corner_radius=8,
            border_width=2,
            border_color=BORDER_PRIMARY,
            button_color=ACCENT_PRIMARY,
            button_hover_color=ACCENT_HOVER,
            dropdown_hover_color=ACCENT_HOVER
        )
        theme_combo.set("Claro")
        theme_combo.pack(fill="x")
        
        # Auto-save option
        autosave_frame = ctk.CTkFrame(content_frame, fg_color=TRANSPARENT_BG)
        autosave_frame.pack(fill="x", pady=(15, 0))
        
        autosave_var = ctk.BooleanVar(value=True)
        autosave_check = ctk.CTkCheckBox(
            autosave_frame,
            text="💾 Guardado automático",
            variable=autosave_var,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            text_color=self.colors['text_primary'],
            border_color=ACCENT_PRIMARY,
            checkmark_color=ACCENT_PRIMARY
        )
        autosave_check.pack(anchor="w")
        
        ctk.CTkLabel(
            autosave_frame,
            text="Guarda automáticamente los cambios en las dimensiones",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL),
            text_color=self.colors['text_secondary']
        ).pack(anchor="w", padx=(25, 0), pady=(5, 0))

    def _create_system_info_section(self, parent, row, col):
        """Crea la sección de información del sistema"""
        
        system_card = ctk.CTkFrame(
            parent,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        system_card.grid(row=row, column=col, padx=(0, 15), pady=(15, 0), sticky="nsew")
        
        # Header
        self._create_section_header(system_card, "📱", "Información del Sistema")
        
        # Content
        content_frame = ctk.CTkFrame(system_card, fg_color=TRANSPARENT_BG)
        content_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        
        # App info
        info_items = [
            ("📱 Aplicación:", "BuildMate v1.0.0"),
            ("🗏 Tipo:", "Sistema de Gestión de Construcción"),
            ("📅 Última actualización:", "Septiembre 2025"),
            ("💾 Base de datos:", "Conectado ✅"),
            ("🔧 Estado:", "Funcionando correctamente")
        ]
        
        for label, value in info_items:
            item_frame = ctk.CTkFrame(content_frame, fg_color=TRANSPARENT_BG)
            item_frame.pack(fill="x", pady=2)
            
            ctk.CTkLabel(
                item_frame,
                text=label,
                font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"),
                text_color=self.colors['text_secondary']
            ).pack(side="left")
            
            ctk.CTkLabel(
                item_frame,
                text=value,
                font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1),
                text_color=self.colors['text_primary']
            ).pack(side="right")
        
        # Separator
        separator = ctk.CTkFrame(content_frame, height=1, fg_color=BORDER_PRIMARY)
        separator.pack(fill="x", pady=15)
        
        # System actions
        check_updates_btn = ctk.CTkButton(
            content_frame,
            text="🔄 Buscar Actualizaciones",
            command=self._check_updates,
            height=35,
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"),
            fg_color=TRANSPARENT_BG,
            hover_color=TRANSPARENT_HOVER,
            text_color=self.colors['text_primary'],
            border_width=1,
            border_color=BORDER_PRIMARY,
            corner_radius=6
        )
        check_updates_btn.pack(fill="x")

    def _create_support_section(self, parent, row, col):
        """Crea la sección de soporte"""
        
        support_card = ctk.CTkFrame(
            parent,
            fg_color=BACKGROUND_CARD,
            corner_radius=15,
            border_width=1,
            border_color=BORDER_PRIMARY
        )
        support_card.grid(row=row, column=col, padx=(15, 0), pady=(15, 0), sticky="nsew")
        
        # Header
        self._create_section_header(support_card, "🆘", "Soporte y Ayuda")
        
        # Content
        content_frame = ctk.CTkFrame(support_card, fg_color=TRANSPARENT_BG)
        content_frame.pack(fill="both", expand=True, padx=25, pady=(0, 25))
        
        # Help info
        help_text = ctk.CTkLabel(
            content_frame,
            text="¿Necesitas ayuda con BuildMate?\nEstamos aquí para asistirte",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
            text_color=self.colors['text_primary'],
            justify="center"
        )
        help_text.pack(pady=(0, 15))
        
        # Support buttons
        buttons_data = [
            ("📚", "Manual de Usuario", self._open_manual, INFO_COLOR),
            ("💬", "Reportar Problema", self._report_issue, WARNING_COLOR),
            ("📧", "Contactar Soporte", self._contact_support, ACCENT_PRIMARY),
            ("⭐", "Calificar App", self._rate_app, SUCCESS_COLOR)
        ]
        
        for icon, text, command, color in buttons_data:
            btn = ctk.CTkButton(
                content_frame,
                text=f"{icon} {text}",
                command=command,
                height=40,
                font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1, weight="bold"),
                fg_color=color,
                hover_color=self._darken_color(color),
                corner_radius=8
            )
            btn.pack(fill="x", pady=3)

    def _create_section_header(self, parent, icon, title):
        """Crea un header para una sección"""
        
        header_frame = ctk.CTkFrame(parent, fg_color=ACCENT_PRIMARY, corner_radius=12)
        header_frame.pack(fill="x", padx=2, pady=2)
        
        header_content = ctk.CTkFrame(header_frame, fg_color=TRANSPARENT_BG)
        header_content.pack(fill="x", padx=20, pady=15)
        
        # Icon
        icon_label = ctk.CTkLabel(
            header_content,
            text=icon,
            font=ctk.CTkFont(size=20)
        )
        icon_label.pack(side="left", padx=(0, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            header_content,
            text=title,
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 1, weight="bold"),
            text_color="white"
        )
        title_label.pack(side="left")

    def _darken_color(self, color):
        """Oscurece un color para efectos hover (simple implementation)"""
        color_map = {
            ACCENT_PRIMARY: ACCENT_HOVER,
            SUCCESS_COLOR: "#059669",
            WARNING_COLOR: "#D97706",
            INFO_COLOR: "#2563EB",
            NEUTRAL_COLOR: "#7C3AED"
        }
        return color_map.get(color, "#374151")

    def _confirm_logout(self):
        """Confirma el cierre de sesión"""
        
        # Crear diálogo personalizado
        dialog = ctk.CTkToplevel(self)
        dialog.title("Confirmar Cierre de Sesión")
        dialog.geometry("400x250")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (250 // 2)
        dialog.geometry(f"400x250+{x}+{y}")
        
        # Icon
        icon_label = ctk.CTkLabel(
            dialog,
            text="🚪",
            font=ctk.CTkFont(size=60)
        )
        icon_label.pack(pady=(30, 10))
        
        # Message
        message_label = ctk.CTkLabel(
            dialog,
            text="¿Estás seguro que deseas cerrar sesión?",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 2, weight="bold"),
            text_color=self.colors['text_primary']
        )
        message_label.pack(pady=(0, 5))
        
        sub_message_label = ctk.CTkLabel(
            dialog,
            text="Tendrás que volver a iniciar sesión la próxima vez",
            font=ctk.CTkFont(size=FONT_SIZE_SMALL + 1),
            text_color=self.colors['text_secondary']
        )
        sub_message_label.pack(pady=(0, 30))
        
        # Buttons
        button_frame = ctk.CTkFrame(dialog, fg_color=TRANSPARENT_BG)
        button_frame.pack(fill="x", padx=40, pady=(0, 30))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=dialog.destroy,
            height=40,
            width=120,
            fg_color=TRANSPARENT_BG,
            hover_color=TRANSPARENT_HOVER,
            text_color=self.colors['text_secondary'],
            border_width=2,
            border_color=BORDER_PRIMARY
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        confirm_btn = ctk.CTkButton(
            button_frame,
            text="Cerrar Sesión",
            command=lambda: (dialog.destroy(), self.on_logout()),
            height=40,
            width=120,
            fg_color=ERROR_COLOR,
            hover_color="#DC2626"
        )
        confirm_btn.pack(side="right")

    def _show_change_password_info(self):
        """Muestra información sobre cambiar contraseña"""
        messagebox.showinfo(
            "Cambiar Contraseña",
            "La funcionalidad de cambio de contraseña estará disponible en una próxima actualización.\n\n" +
            "Por ahora, puedes usar la opción 'Olvidé mi contraseña' en la pantalla de login."
        )

    def _check_updates(self):
        """Simula la búsqueda de actualizaciones"""
        # Crear diálogo de progreso
        progress_dialog = ctk.CTkToplevel(self)
        progress_dialog.title("Buscando Actualizaciones")
        progress_dialog.geometry("350x150")
        progress_dialog.transient(self)
        progress_dialog.grab_set()
        
        # Centrar ventana
        progress_dialog.update_idletasks()
        x = (progress_dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (progress_dialog.winfo_screenheight() // 2) - (150 // 2)
        progress_dialog.geometry(f"350x150+{x}+{y}")
        
        ctk.CTkLabel(
            progress_dialog,
            text="🔄 Buscando actualizaciones...",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 1, weight="bold")
        ).pack(pady=30)
        
        progress_bar = ctk.CTkProgressBar(progress_dialog, width=250)
        progress_bar.pack(pady=10)
        progress_bar.set(0)
        
        # Simular progreso
        def update_progress(value):
            progress_bar.set(value)
            if value < 1.0:
                self.after(200, lambda: update_progress(value + 0.1))
            else:
                progress_dialog.destroy()
                messagebox.showinfo(
                    "Actualizaciones",
                    "✅ Tu aplicación está actualizada\n\nBuildMate v1.0.0 es la versión más reciente."
                )
        
        update_progress(0.1)

    def _open_manual(self):
        """Abre el manual de usuario"""
        messagebox.showinfo(
            "Manual de Usuario",
            "📚 El manual de usuario estará disponible próximamente.\n\n" +
            "Mientras tanto, puedes explorar la aplicación o contactar soporte si tienes dudas."
        )

    def _report_issue(self):
        """Permite reportar un problema"""
        # Crear diálogo para reportar problema
        dialog = ctk.CTkToplevel(self)
        dialog.title("Reportar Problema")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (dialog.winfo_screenheight() // 2) - (400 // 2)
        dialog.geometry(f"500x400+{x}+{y}")
        
        # Header
        ctk.CTkLabel(
            dialog,
            text="🐛 Reportar Problema",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 4, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            dialog,
            text="Describe el problema que encontraste",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
            text_color=self.colors['text_secondary']
        ).pack(pady=(0, 20))
        
        # Problema textbox
        problem_text = ctk.CTkTextbox(
            dialog,
            height=200,
            corner_radius=10,
            border_width=2,
            border_color=BORDER_PRIMARY
        )
        problem_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
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
            hover_color=TRANSPARENT_HOVER,
            text_color=self.colors['text_secondary'],
            border_width=2,
            border_color=BORDER_PRIMARY
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        send_btn = ctk.CTkButton(
            button_frame,
            text="📤 Enviar Reporte",
            command=lambda: self._send_report(problem_text.get("1.0", "end-1c"), dialog),
            height=40,
            width=140,
            fg_color=WARNING_COLOR,
            hover_color="#D97706"
        )
        send_btn.pack(side="right")

    def _send_report(self, problem_text, dialog):
        """Envía el reporte de problema"""
        if not problem_text.strip():
            messagebox.showwarning("Advertencia", "Por favor, describe el problema antes de enviar.")
            return
        
        # Simular envío
        messagebox.showinfo(
            "Reporte Enviado",
            "✅ Tu reporte ha sido enviado exitosamente.\n\nNuestro equipo lo revisará y te contactaremos si necesitamos más información."
        )
        dialog.destroy()

    def _contact_support(self):
        """Muestra información de contacto"""
        messagebox.showinfo(
            "Contactar Soporte",
            "📧 Información de Contacto:\n\n" +
            "• Email: soporte@buildmate.com\n" +
            "• Teléfono: +54 (11) 1234-5678\n" +
            "• Horario: Lunes a Viernes, 9:00 - 18:00\n\n" +
            "También puedes usar la función 'Reportar Problema' para enviar consultas específicas."
        )

    def _rate_app(self):
        """Permite calificar la aplicación"""
        # Crear diálogo de calificación
        dialog = ctk.CTkToplevel(self)
        dialog.title("Calificar BuildMate")
        dialog.geometry("400x300")
        dialog.transient(self)
        dialog.grab_set()
        
        # Centrar ventana
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (300 // 2)
        dialog.geometry(f"400x300+{x}+{y}")
        
        # Header
        ctk.CTkLabel(
            dialog,
            text="⭐ Califica BuildMate",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL + 4, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(pady=(30, 10))
        
        ctk.CTkLabel(
            dialog,
            text="¿Qué te parece nuestra aplicación?",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
            text_color=self.colors['text_secondary']
        ).pack(pady=(0, 20))
        
        # Rating buttons
        rating_frame = ctk.CTkFrame(dialog, fg_color=TRANSPARENT_BG)
        rating_frame.pack(pady=10)
        
        rating_var = ctk.IntVar(value=5)
        
        for i in range(1, 6):
            star_btn = ctk.CTkRadioButton(
                rating_frame,
                text=f"{i} ⭐",
                variable=rating_var,
                value=i,
                font=ctk.CTkFont(size=FONT_SIZE_NORMAL),
                text_color=self.colors['text_primary']
            )
            star_btn.pack(pady=2)
        
        # Comentarios
        ctk.CTkLabel(
            dialog,
            text="Comentarios (opcional):",
            font=ctk.CTkFont(size=FONT_SIZE_NORMAL, weight="bold"),
            text_color=self.colors['text_primary']
        ).pack(anchor="w", padx=40, pady=(20, 5))
        
        comment_entry = ctk.CTkEntry(
            dialog,
            height=40,
            placeholder_text="Cuéntanos tu experiencia..."
        )
        comment_entry.pack(fill="x", padx=40, pady=(0, 20))
        
        # Botones
        button_frame = ctk.CTkFrame(dialog, fg_color=TRANSPARENT_BG)
        button_frame.pack(fill="x", padx=40, pady=(0, 30))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancelar",
            command=dialog.destroy,
            height=40,
            width=100,
            fg_color=TRANSPARENT_BG,
            hover_color=TRANSPARENT_HOVER,
            text_color=self.colors['text_secondary'],
            border_width=2,
            border_color=BORDER_PRIMARY
        )
        cancel_btn.pack(side="right", padx=(10, 0))
        
        submit_btn = ctk.CTkButton(
            button_frame,
            text="⭐ Enviar Calificación",
            command=lambda: self._submit_rating(rating_var.get(), comment_entry.get(), dialog),
            height=40,
            width=160,
            fg_color=SUCCESS_COLOR,
            hover_color="#059669"
        )
        submit_btn.pack(side="right")

    def _submit_rating(self, rating, comment, dialog):
        """Envía la calificación"""
        messagebox.showinfo(
            "¡Gracias por tu Calificación!",
            f"⭐ Calificación: {rating}/5 estrellas\n\n" +
            "Tu opinión es muy valiosa para nosotros y nos ayuda a mejorar BuildMate."
        )
        dialog.destroy()