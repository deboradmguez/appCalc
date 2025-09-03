import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path
from config import *

class Sidebar(tk.Frame):
    """
    Componente de Sidebar colapsible para la navegación principal.
    """
    def __init__(self, master, commands, **kwargs):
        super().__init__(master, bg=GRAPHITE, **kwargs)
        self.commands = commands
        self.is_collapsed = True  # El sidebar empieza colapsado

        # --- Cargar y preparar iconos ---
        self.icons = self._load_icons()
        
        # --- Contenedor para los botones ---
        # El botón de menú va arriba y el resto en otro frame
        self.menu_btn = self._create_sidebar_button(
            self, # Se ancla directamente al sidebar
            self.icons["menu"],
            " menú", # Espacio inicial para alineación
            self.toggle_sidebar
        )
        self.menu_btn.pack(pady=15, padx=15, anchor="w")

        self.button_container = tk.Frame(self, bg=GRAPHITE)
        self.button_container.pack(fill=tk.Y, expand=True)

        # --- Crear los botones de navegación ---
        self.nav_buttons = {}
        for name, command in self.commands.items():
            icon = self.icons.get(name.lower(), self.icons["proyectos"]) # Icono por defecto
            btn = self._create_sidebar_button(self.button_container, icon, f" {name}", command)
            btn.pack(pady=10, padx=15, anchor="w")
            self.nav_buttons[name] = btn

        # Inicializar en estado colapsado
        self.toggle_sidebar()

    def _load_icons(self):
        """Carga los iconos desde la carpeta de assets."""
        icon_path = Path(__file__).resolve().parents[2] / "assets" / "icons"
        icon_names = ["menu", "proyectos", "materiales", "areas", "configuración"]
        icons = {}
        for name in icon_names:
            try:
                img = Image.open(icon_path / f"{name}.png").resize((24, 24), Image.Resampling.LANCZOS)
                icons[name] = ImageTk.PhotoImage(img)
            except FileNotFoundError:
                print(f"Advertencia: No se encontró el icono {name}.png")
                # Crear una imagen en blanco como placeholder
                img = Image.new('RGBA', (24, 24), (0,0,0,0))
                icons[name] = ImageTk.PhotoImage(img)
        return icons

    def _create_sidebar_button(self, parent, icon, text, command):
        """Función helper para crear un botón estandarizado del sidebar."""
        btn = tk.Button(parent, 
                        image=icon, 
                        text=text, 
                        compound=tk.LEFT, 
                        command=command,
                        anchor="w",
                        **NAVBAR_BUTTON_STYLE,
                        highlightthickness=0,
                        padx=10)
        return btn

    def toggle_sidebar(self):
        """Expande o contrae el sidebar."""
        if self.is_collapsed:
            # Expandir
            self.config(width=220)
            self.menu_btn.config(text=" Menú")
            for name, btn in self.nav_buttons.items():
                btn.config(text=f" {name}")
        else:
            # Colapsar
            self.config(width=60)
            self.menu_btn.config(text="")
            for name, btn in self.nav_buttons.items():
                btn.config(text="")
        
        self.is_collapsed = not self.is_collapsed