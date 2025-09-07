# src/ui/components/sidebar.py

import customtkinter as ctk
from PIL import Image
from pathlib import Path
import unicodedata
import time
from config import get_sidebar_colors, TRANSPARENT_BG, TRANSPARENT_HOVER

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, commands, width_animation_callback=None, **kwargs):
        # Obtenemos los colores del sidebar
        colors = get_sidebar_colors()
        
        super().__init__(master, corner_radius=0, fg_color=colors['bg'], **kwargs)
        
        self.pack_propagate(False)
        self.colors = colors
        self.commands = commands
        self.width_animation_callback = width_animation_callback
        self.is_expanded = True
        self.animation_in_progress = False
        self._animation_after_id = None
        self.animation_start_time = None

        # --- DIMENSIONES ---
        self.EXPANDED_WIDTH = 240
        self.COLLAPSED_WIDTH = 70
        
        # --- ANIMACIÓN ---
        self.ANIMATION_DURATION = 0.25
        self.ANIMATION_FPS = 60
        self.ANIMATION_DELAY = int(1000 / self.ANIMATION_FPS)

        # Configuración inicial
        self.configure(width=self.EXPANDED_WIDTH)

        # Cargar assets
        self.icons = self._load_icons()
        
        # --- HEADER DEL SIDEBAR ---
        self.header_frame = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        self.header_frame.pack(fill="x", pady=(20, 15), padx=15)
        
        # Logo/icono de la app
        try:
            base_path = Path(__file__).resolve().parents[2]
            logo_path = base_path / "assets" / "logoNuevo.png"
            if logo_path.exists():
                # CORREGIDO: Guardar el CTkImage como un atributo de instancia
                self.logo_img = ctk.CTkImage(Image.open(logo_path), size=(32, 32))
                self.logo_label = ctk.CTkLabel(
                    self.header_frame, 
                    image=self.logo_img, # Usar el atributo de instancia
                    text=""
                )
                self.logo_label.pack(side="left", padx=(0, 10))
        except:
            pass
        
        # Título de la app
        self.app_title = ctk.CTkLabel(
            self.header_frame, 
            text="Constructor Pro", 
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=colors['text'],
            fg_color=TRANSPARENT_BG
        )
        self.app_title.pack(side="left", anchor="w")
        
        # --- BOTÓN DE MENÚ ---
        self.menu_frame = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        self.menu_frame.pack(fill="x", pady=(0, 20), padx=15)
        
        self.menu_btn = self._create_button(
            self.menu_frame, 
            self.icons["menu"], 
            " Menú", 
            self.toggle_sidebar,
            is_menu=True
        )
        self.menu_btn.pack(anchor="w")

        # --- CONTENEDOR DE BOTONES DE NAVEGACIÓN ---
        self.button_container = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        self.button_container.pack(fill="y", expand=True, anchor="n")

        # Separador
        separator = ctk.CTkFrame(self, height=1, fg_color="#4B5563")
        separator.pack(fill="x", padx=15, pady=(0, 15))

        self.nav_buttons = {}
        for name, command in self.commands.items():
            icon_name = self._normalize_str(name)
            icon = self.icons.get(icon_name, self.icons["proyectos"])
            
            btn = self._create_button(self.button_container, icon, f" {name}", command)
            btn.pack(pady=3, padx=15, anchor="w", fill="x")
            self.nav_buttons[name] = btn

        # --- PIE DEL SIDEBAR ---
        self.footer_frame = ctk.CTkFrame(self, fg_color=TRANSPARENT_BG)
        self.footer_frame.pack(side="bottom", fill="x", pady=15, padx=15)
        
        # Información adicional cuando está expandido
        self.version_label = ctk.CTkLabel(
            self.footer_frame,
            text="v1.0.0",
            font=ctk.CTkFont(size=10),
            text_color="#9CA3AF"
        )
        self.version_label.pack(anchor="w")

    def _normalize_str(self, s):
        return "".join(
            c for c in unicodedata.normalize('NFD', s.lower())
            if unicodedata.category(c) != 'Mn'
        )

    def _load_icons(self):
        icon_path = Path(__file__).resolve().parent.parent.parent / "assets" / "icons"
        icon_names = ["menu", "proyectos", "materiales", "areas", "configuracion"]
        icons = {}
        for name in icon_names:
            try:
                img = Image.open(icon_path / f"{name}.png")
                icons[name] = ctk.CTkImage(img, size=(20, 20))
            except FileNotFoundError:
                img = Image.new('RGBA', (20, 20), (255, 255, 255, 100))
                icons[name] = ctk.CTkImage(img, size=(20, 20))
        return icons

    def _create_button(self, parent, icon, text, command, is_menu=False):
        button = ctk.CTkButton(
            parent, 
            image=icon, 
            text=text, 
            command=command,
            fg_color=self.colors['button_transparent'],
            hover_color=self.colors['hover'],
            text_color=self.colors['text'],
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold" if is_menu else "normal"),
            height=45 if not is_menu else 40,
            corner_radius=8
        )
        return button

    def set_selected_button(self, name):
        """Resalta el botón seleccionado y deselecciona otros."""
        self.selected_button_name = name
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name:
                btn.configure(
                    fg_color=self.colors['selected'],
                    hover_color=self.colors['selected']
                )
            else:
                btn.configure(
                    fg_color=self.colors['button_transparent'],
                    hover_color=self.colors['hover']
                )

    def toggle_sidebar(self):
        if self.animation_in_progress:
            return
        self.animation_in_progress = True
        self.animation_start_time = time.time()
        
        if self.is_expanded:
            self.hide_texts()
            self.start_width = self.EXPANDED_WIDTH
            self.target_width = self.COLLAPSED_WIDTH
        else:
            self.start_width = self.COLLAPSED_WIDTH
            self.target_width = self.EXPANDED_WIDTH

        self.animate_width()

    def animate_width(self):
        elapsed_time = time.time() - self.animation_start_time
        
        if elapsed_time >= self.ANIMATION_DURATION:
            self.configure(width=self.target_width)
            self.animation_in_progress = False
            self.is_expanded = not self.is_expanded

            if self.is_expanded:
                self.show_texts()

            if self.width_animation_callback:
                self.width_animation_callback(self.target_width)
            self._animation_after_id = None
            return

        progress = elapsed_time / self.ANIMATION_DURATION
        progress = 1 - (1 - progress) ** 3
        
        new_width = self.start_width + (self.target_width - self.start_width) * progress
        
        self.configure(width=int(new_width))
        
        self._animation_after_id = self.after(self.ANIMATION_DELAY, self.animate_width)

    def hide_texts(self):
        """Oculta todos los textos cuando el sidebar se colapsa"""
        if hasattr(self, 'app_title'):
            self.app_title.pack_forget()
        if hasattr(self, 'logo_label') and hasattr(self, 'logo_img'):
            # CORREGIDO: Configurar el objeto CTkImage, no el CTkLabel
            self.logo_img.configure(size=(24, 24))
        
        self.menu_btn.configure(text="")
        for btn in self.nav_buttons.values():
            btn.configure(text="")
        
        if hasattr(self, 'version_label'):
            self.version_label.pack_forget()

    def show_texts(self):
        """Muestra todos los textos cuando el sidebar se expande"""
        if hasattr(self, 'app_title'):
            self.app_title.pack(side="left", anchor="w")
        if hasattr(self, 'logo_label') and hasattr(self, 'logo_img'):
            # CORREGIDO: Configurar el objeto CTkImage de vuelta a su tamaño normal
            self.logo_img.configure(size=(32, 32))
        
        self.menu_btn.configure(text=" Menú")
        for name, btn in self.nav_buttons.items():
            btn.configure(text=f" {name}")
            
        if hasattr(self, 'version_label'):
            self.version_label.pack(anchor="w")
            
    def destroy(self):
        if self._animation_after_id:
            self.after_cancel(self._animation_after_id)
        super().destroy()