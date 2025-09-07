# src/ui/components/sidebar.py (Versión final con animación de ancho estable)

import customtkinter as ctk
from PIL import Image
from pathlib import Path
import unicodedata
import time
import math

from config import get_sidebar_colors

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, commands, animation_callback=None, **kwargs):
        self.colors = get_sidebar_colors()
        self.EXPANDED_WIDTH = 240
        self.COLLAPSED_WIDTH = 70
        
        super().__init__(master, corner_radius=0, fg_color=self.colors['bg'], width=self.EXPANDED_WIDTH, **kwargs)
        
        self.pack_propagate(False)
        self.commands = commands
        self.animation_callback = animation_callback
        self.is_expanded = True
        self.animation_in_progress = False
        self._animation_after_id = None

        self.ANIMATION_DURATION = 0.19
        self.ANIMATION_FPS = 30
        self.ANIMATION_DELAY = int(1000 / self.ANIMATION_FPS)

        self.icons = self._load_icons()
        sidebar_bg_color = self.colors['bg']

        # --- CONTENEDOR PRINCIPAL INTERNO ---
        # Este contenedor nos permite usar padx sin que los elementos se corten durante la animación
        self.main_content_frame = ctk.CTkFrame(self, fg_color=sidebar_bg_color)
        self.main_content_frame.pack(fill="both", expand=True, padx=15, pady=15)
        
        # --- HEADER ---
        header_frame = ctk.CTkFrame(self.main_content_frame, fg_color=sidebar_bg_color)
        header_frame.pack(fill="x", pady=(5, 10))
        
        try:
            base_path = Path(__file__).resolve().parents[2]
            logo_path = base_path / "assets" / "logoNuevo.png"
            if logo_path.exists():
                self.logo_img = ctk.CTkImage(Image.open(logo_path), size=(32, 32))
                self.logo_label = ctk.CTkLabel(header_frame, image=self.logo_img, text="")
                self.logo_label.pack(side="left", padx=(5, 10))
        except:
            self.logo_img = None
        
        self.app_title = ctk.CTkLabel(
            header_frame, text="Constructor Pro", font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.colors['text']
        )
        self.app_title.pack(side="left", anchor="w")
        
        # --- BOTÓN DE MENÚ ---
        menu_frame = ctk.CTkFrame(self.main_content_frame, fg_color=sidebar_bg_color)
        menu_frame.pack(fill="x", pady=(0, 20))
        
        self.menu_btn = self._create_button(
            menu_frame, self.icons["menu"], " Ocultar Menú", self.toggle_sidebar, is_menu=True
        )
        self.menu_btn.pack(anchor="w", fill="x")

        # --- BOTONES DE NAVEGACIÓN ---
        self.button_container = ctk.CTkFrame(self.main_content_frame, fg_color=sidebar_bg_color)
        self.button_container.pack(fill="y", expand=True, anchor="n")

        separator = ctk.CTkFrame(self.main_content_frame, height=1, fg_color="#4B5563")
        separator.pack(fill="x", pady=(0, 15))

        self.nav_buttons = {}
        for name, command in self.commands.items():
            icon_name = self._normalize_str(name)
            icon = self.icons.get(icon_name, self.icons["proyectos"])
            btn = self._create_button(self.button_container, icon, f" {name}", command)
            btn.pack(pady=3, anchor="w", fill="x")
            self.nav_buttons[name] = btn

        # --- FOOTER ---
        footer_frame = ctk.CTkFrame(self.main_content_frame, fg_color=sidebar_bg_color)
        footer_frame.pack(side="bottom", fill="x")
        
        self.version_label = ctk.CTkLabel(
            footer_frame, text="v1.0.0", font=ctk.CTkFont(size=10), text_color="#9CA3AF"
        )
        self.version_label.pack(anchor="w")

    def _normalize_str(self, s):
        return "".join(c for c in unicodedata.normalize('NFD', s.lower()) if unicodedata.category(c) != 'Mn')

    def _load_icons(self):
        icon_path = Path(__file__).resolve().parent.parent.parent / "assets" / "icons"
        icon_names = ["menu", "proyectos", "materiales", "areas", "configuracion"]
        icons = {}
        for name in icon_names:
            try:
                img = Image.open(icon_path / f"{name}.png")
                icons[name] = ctk.CTkImage(img, size=(20, 20))
            except FileNotFoundError:
                icons[name] = ctk.CTkImage(Image.new('RGBA', (20, 20), (255, 255, 255, 100)), size=(20, 20))
        return icons

    def _create_button(self, parent, icon, text, command, is_menu=False):
        return ctk.CTkButton(
            parent, image=icon, text=text, command=command,
            fg_color=self.colors['bg'], hover_color=self.colors['hover'],
            text_color=self.colors['text'], anchor="w",
            font=ctk.CTkFont(size=14, weight="bold" if is_menu else "normal"),
            height=45 if not is_menu else 40, corner_radius=8
        )

    def set_selected_button(self, name):
        for btn_name, btn in self.nav_buttons.items():
            fg = self.colors['selected'] if btn_name == name else self.colors['bg']
            hover = self.colors['selected'] if btn_name == name else self.colors['hover']
            btn.configure(fg_color=fg, hover_color=hover)

    def _hide_texts(self):
        self.app_title.pack_forget()
        self.version_label.pack_forget()
        self.menu_btn.configure(text="")
        if self.logo_img: self.logo_img.configure(size=(24,24))
        for btn in self.nav_buttons.values():
            btn.configure(text="")

    def _show_texts(self):
        self.app_title.pack(side="left", anchor="w")
        self.version_label.pack(anchor="w")
        self.menu_btn.configure(text=" Ocultar Menú")
        if self.logo_img: self.logo_img.configure(size=(32,32))
        for name, btn in self.nav_buttons.items():
            btn.configure(text=f" {name}")
    
    def toggle_sidebar(self):
        if self.animation_in_progress: return
        self.animation_in_progress = True
        
        if self.is_expanded:
            self._hide_texts()
            self.start_width, self.end_width = self.EXPANDED_WIDTH, self.COLLAPSED_WIDTH
        else:
            self.start_width, self.end_width = self.COLLAPSED_WIDTH, self.EXPANDED_WIDTH
        
        self.animation_start_time = time.time()
        self.animate_width()

    def animate_width(self):
        elapsed_time = time.time() - self.animation_start_time
        
        if elapsed_time >= self.ANIMATION_DURATION:
            self.configure(width=self.end_width)
            self.animation_in_progress = False
            self.is_expanded = not self.is_expanded
            # Mostramos el texto SOLO cuando la animación de apertura ha terminado
            if self.is_expanded:
                self._show_texts()
            return

        progress = elapsed_time / self.ANIMATION_DURATION
        progress = -(math.cos(math.pi * progress) - 1) / 2
        
        new_width = self.start_width + (self.end_width - self.start_width) * progress
        
        self.configure(width=int(new_width))
        
        if self.animation_callback:
            self.animation_callback(int(new_width))
            
        self._animation_after_id = self.after(self.ANIMATION_DELAY, self.animate_width)

    def destroy(self):
        if self._animation_after_id: self.after_cancel(self._animation_after_id)
        super().destroy()