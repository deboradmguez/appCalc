import customtkinter as ctk
from PIL import Image
from pathlib import Path
import logging

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, commands, **kwargs):
        # Configuración inicial del frame
        super().__init__(
            master, 
            corner_radius=0,
            fg_color=("gray90", "gray13"),  # Color de fondo claro/oscuro
            **kwargs
        )
        
        self.commands = commands
        self.is_expanded = True
        self.animation_in_progress = False
        
        # Configurar el tamaño fijo inicial
        self.configure(width=220)
        self.grid_propagate(False)  # CRUCIAL: Evita que el contenido cambie el tamaño del frame
        
        # Configurar grid interno
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # --- Cargar iconos ---
        self.icons = self._load_icons()
        
        # --- Frame del menú (parte superior) ---
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        self.menu_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(15, 5))
        self.menu_frame.grid_propagate(False)
        
        # --- Frame de botones de navegación ---
        self.button_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.button_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        
        # --- Crear botón de menú ---
        self.menu_btn = self._create_menu_button()
        
        # --- Crear botones de navegación ---
        self.nav_buttons = {}
        self._create_nav_buttons()

    def _load_icons(self):
        """Carga los iconos con manejo de errores mejorado."""
        icon_path = Path(__file__).resolve().parents[2] / "assets" / "icons"
        icon_names = ["menu", "proyectos", "materiales", "areas", "configuracion"]
        icons = {}
        
        # Crear imagen por defecto
        default_img = Image.new('RGBA', (20, 20), (0, 0, 0, 0))
        
        for name in icon_names:
            try:
                img_path = icon_path / f"{name}.png"
                if img_path.exists():
                    img = Image.open(img_path)
                    icons[name] = ctk.CTkImage(img, size=(20, 20))
                else:
                    icons[name] = ctk.CTkImage(default_img, size=(20, 20))
            except Exception as e:
                logging.warning(f"No se pudo cargar el icono {name}: {e}")
                icons[name] = ctk.CTkImage(default_img, size=(20, 20))
        
        return icons

    def _create_menu_button(self):
        """Crea el botón de menú con configuración optimizada."""
        btn = ctk.CTkButton(
            self.menu_frame,
            image=self.icons.get("menu"),
            text=" Menú",
            command=self.toggle_sidebar,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray80", "gray25"),
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=40
        )
        btn.pack(fill="x")
        return btn

    def _create_nav_buttons(self):
        """Crea los botones de navegación."""
        for i, (name, command) in enumerate(self.commands.items()):
            icon_key = self._get_icon_key(name)
            
            btn = ctk.CTkButton(
                self.button_frame,
                image=self.icons.get(icon_key, self.icons["proyectos"]),
                text=f" {name}",
                command=command,
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray80", "gray25"),
                anchor="w",
                font=ctk.CTkFont(size=13),
                height=45
            )
            btn.pack(fill="x", pady=2)
            self.nav_buttons[name] = btn

    def _get_icon_key(self, name):
        """Convierte el nombre del botón a la clave del icono."""
        return name.lower().replace('á', 'a').replace('ó', 'o').replace('ñ', 'n')

    def toggle_sidebar(self):
        """Alterna el estado del sidebar con animación suave."""
        if self.animation_in_progress:
            return
        
        self.animation_in_progress = True
        
        if self.is_expanded:
            self._collapse_sidebar()
        else:
            self._expand_sidebar()

    def _collapse_sidebar(self):
        """Colapsa el sidebar a modo icono."""
        # Primero ocultar textos
        self.menu_btn.configure(text="")
        for btn in self.nav_buttons.values():
            btn.configure(text="", anchor="center")
        
        # Luego animar el ancho
        self._animate_width(220, 70, callback=self._on_collapse_complete)

    def _expand_sidebar(self):
        """Expande el sidebar a modo completo."""
        # Primero animar el ancho
        self._animate_width(70, 220, callback=self._on_expand_complete)

    def _animate_width(self, start_width, target_width, callback=None):
        """Animación suave del ancho del sidebar."""
        steps = 15  # Número de pasos de la animación
        step_size = (target_width - start_width) / steps
        current_step = 0
        
        def animate_step():
            nonlocal current_step
            current_step += 1
            
            if current_step <= steps:
                new_width = start_width + (step_size * current_step)
                self.configure(width=int(new_width))
                self.after(20, animate_step)  # 20ms entre pasos para suavidad
            else:
                # Asegurar el ancho final exacto
                self.configure(width=target_width)
                self.animation_in_progress = False
                if callback:
                    callback()
        
        animate_step()

    def _on_collapse_complete(self):
        """Callback ejecutado cuando se completa el colapso."""
        self.is_expanded = False

    def _on_expand_complete(self):
        """Callback ejecutado cuando se completa la expansión."""
        # Mostrar textos después de la animación
        self.menu_btn.configure(text=" Menú")
        for name, btn in self.nav_buttons.items():
            btn.configure(text=f" {name}", anchor="w")
        
        self.is_expanded = True

    def set_active_button(self, button_name):
        """Marca un botón como activo."""
        # Resetear todos los botones
        for btn in self.nav_buttons.values():
            btn.configure(fg_color="transparent")
        
        # Activar el botón seleccionado
        if button_name in self.nav_buttons:
            self.nav_buttons[button_name].configure(
                fg_color=("gray75", "gray30")
            )