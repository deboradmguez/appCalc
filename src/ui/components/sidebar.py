# src/ui/components/sidebar.py (Versión Final y Corregida)

import customtkinter as ctk
from PIL import Image
from pathlib import Path

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, commands, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        self.commands = commands
        self.is_expanded = True
        self.animation_in_progress = False
        self.animation_after_id = None  # <-- NUEVO: Para guardar el ID de la tarea de animación

        self.icons = self._load_icons()
        
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(fill="x", pady=(15, 10), padx=15)

        self.button_container = ctk.CTkFrame(self, fg_color="transparent")
        self.button_container.pack(fill="y", expand=True)

        self.menu_btn = self._create_sidebar_button(
            self.menu_frame, self.icons["menu"], " Menú", self.toggle_sidebar
        )
        self.menu_btn.pack(anchor="w")

        self.nav_buttons = {}
        for name, command in self.commands.items():
            icon_name = name.lower().replace('á', 'a').replace('ó', 'o')
            icon = self.icons.get(icon_name, self.icons["proyectos"])
            btn = self._create_sidebar_button(self.button_container, icon, f" {name}", command)
            btn.pack(pady=5, padx=15, anchor="w")
            self.nav_buttons[name] = btn

        self.configure(width=220)

    def _load_icons(self):
        icon_path = Path(__file__).resolve().parents[2] / "assets" / "icons"
        icon_names = ["menu", "proyectos", "materiales", "areas", "configuracion"]
        icons = {}
        for name in icon_names:
            try:
                img = Image.open(icon_path / f"{name}.png")
                icons[name] = ctk.CTkImage(img, size=(22, 22))
            except FileNotFoundError:
                img = Image.new('RGBA', (22, 22), (0, 0, 0, 0))
                icons[name] = ctk.CTkImage(img, size=(22, 22))
        return icons

    def _create_sidebar_button(self, parent, icon, text, command):
        btn = ctk.CTkButton(
            parent, image=icon, text=text, command=command,
            fg_color="transparent", anchor="w",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        return btn

    def toggle_sidebar(self):
        if self.animation_in_progress:
            return
        self.animation_in_progress = True
        
        if self.is_expanded:
            self.animate_width(start=220, end=70, is_collapsing=True)
        else:
            self.menu_btn.configure(text=" Menú")
            for name, btn in self.nav_buttons.items():
                btn.configure(text=f" {name}", anchor="w")
            self.animate_width(start=70, end=220, is_collapsing=False)
        
        self.is_expanded = not self.is_expanded

    def animate_width(self, start, end, is_collapsing):
        step = -10 if is_collapsing else 10
        new_width = self.winfo_width() + step

        if (is_collapsing and new_width <= end) or (not is_collapsing and new_width >= end):
            self.configure(width=end)
            if is_collapsing:
                self.menu_btn.configure(text="")
                for name, btn in self.nav_buttons.items():
                    btn.configure(text="", anchor="center")
            self.animation_in_progress = False
            self.animation_after_id = None # Limpiamos el ID
            return

        self.configure(width=new_width)
        # Guardamos el ID de la tarea programada
        self.animation_after_id = self.after(10, lambda: self.animate_width(start, end, is_collapsing))

    def destroy(self):
        """
        Sobrescribe el método destroy para cancelar cualquier animación pendiente.
        """
        # --- LA CORRECCIÓN CLAVE ---
        if self.animation_after_id:
            self.after_cancel(self.animation_after_id)
        
        # Llama al método destroy original para cerrar el widget
        super().destroy()