# src/ui/components/sidebar.py (Versión final Overlay, sin cabezal interno)

import customtkinter as ctk
from PIL import Image
from pathlib import Path
import unicodedata
import time
import math
from config import get_sidebar_colors

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, commands, **kwargs):
        self.colors = get_sidebar_colors()
        self.EXPANDED_WIDTH = 240
        
        super().__init__(master, corner_radius=0, fg_color=self.colors['bg'], width=self.EXPANDED_WIDTH, **kwargs)
        
        self.pack_propagate(False)
        self.commands = commands
        self.is_expanded = False
        self.animation_in_progress = False
        self._animation_after_id = None

        self.ANIMATION_DURATION = 0.3
        self.ANIMATION_FPS = 60
        self.ANIMATION_DELAY = int(1000 / self.ANIMATION_FPS)

        self.icons = self._load_icons()
        sidebar_bg_color = self.colors['bg']

        # --- CONTENIDO ---
        
        # CORREGIDO: Se eliminó toda la sección del cabezal (header_frame, logo y app_title)
        # para evitar que se superponga con el botón de menú principal.

        # CORREGIDO: Se ajustó el padding del contenedor de botones para dejar espacio arriba.
        button_container = ctk.CTkFrame(self, fg_color=sidebar_bg_color)
        button_container.pack(fill="y", expand=True, anchor="n", padx=20, pady=(60, 20))

        separator = ctk.CTkFrame(self, height=1, fg_color="#4B5563")
        separator.pack(fill="x", pady=(0, 15))

        self.nav_buttons = {}
        for name, command in self.commands.items():
            icon_name = self._normalize_str(name)
            icon = self.icons.get(icon_name, self.icons["proyectos"])
            btn = self._create_button(button_container, icon, f" {name}", command)
            btn.pack(pady=3, anchor="w", fill="x")
            self.nav_buttons[name] = btn

        footer_frame = ctk.CTkFrame(self, fg_color=sidebar_bg_color)
        footer_frame.pack(side="bottom", fill="x", pady=15, padx=20)
        
        ctk.CTkLabel(
            footer_frame, text="v1.0.0", font=ctk.CTkFont(size=10), text_color="#9CA3AF"
        ).pack(anchor="w")

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

    def toggle_slide(self):
        if self.animation_in_progress: return
        
        self.animation_in_progress = True
        self.start_x = self.winfo_x()
        self.end_x = 0 if not self.is_expanded else -self.EXPANDED_WIDTH
        
        self.animation_start_time = time.time()
        self.animate_slide()

    def animate_slide(self):
        elapsed_time = time.time() - self.animation_start_time
        
        if elapsed_time >= self.ANIMATION_DURATION:
            self.place_configure(x=self.end_x)
            self.is_expanded = not self.is_expanded
            self.animation_in_progress = False
            return

        progress = elapsed_time / self.ANIMATION_DURATION
        progress = -(math.cos(math.pi * progress) - 1) / 2
        
        new_x = self.start_x + (self.end_x - self.start_x) * progress
        self.place(x=int(new_x), y=0, relheight=1)
            
        self._animation_after_id = self.after(self.ANIMATION_DELAY, self.animate_slide)

    def destroy(self):
        if self._animation_after_id: self.after_cancel(self._animation_after_id)
        super().destroy()
    
    def hide(self):
        """Oculta el sidebar si está expandido."""
        if self.is_expanded and not self.animation_in_progress:
            self.toggle_slide()