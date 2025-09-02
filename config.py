import tkinter as tk
import sys
from os import name as os_name

# Colores
INDIGO_DYE = "#08415c"
PERSIAN_RED = "#cc2936"
TEA_ROSE = "#ebbab9"
BLUE_MUNSELL = "#388697"
AQUAMARINE = "#b5ffe1"
WHITE = "#ffffff"
LIGHT_GRAY = "#f8f9fa"
MEDIUM_GRAY = "#dee2e6"
DARK_GRAY = "#6c757d"

# Función para detectar fuentes del sistema
def get_system_font():
    """Detecta la mejor fuente para el sistema sin crear una ventana."""
    try:
        temp_root = tk.Tk()
        temp_root.withdraw()
        system = temp_root.tk.call('tk', 'windowingsystem')
        temp_root.destroy()
        
        if system == 'win32':
            return "Segoe UI"
        elif system == 'aqua':  # macOS
            return "Helvetica Neue"
        else:  # Linux/Unix
            return "Ubuntu"
    except:
        return "Arial"

# Fuentes
FONT_PRIMARY = get_system_font()
FONT_SECONDARY = "Arial"

# Tamaños de fuente
FONT_SIZE_TITLE = 18
FONT_SIZE_LARGE = 16
FONT_SIZE_SUBTITLE = 12
FONT_SIZE_NORMAL = 11
FONT_SIZE_SMALL = 10

# Estilos predefinidos para los campos de entrada
ENTRY_STYLE = {
    "font": (FONT_PRIMARY, FONT_SIZE_NORMAL), 
    "bg": WHITE,  # Fondo blanco para diferenciarse del contenedor gris claro
    "fg": INDIGO_DYE,
    "relief": 'flat', 
    "bd": 0, 
    "highlightthickness": 1, # Grosor del borde
    "highlightcolor": BLUE_MUNSELL, # Color del borde cuando el campo tiene foco
    "highlightbackground": MEDIUM_GRAY # Color del borde cuando el campo no tiene foco
}

BUTTON_STYLE_PRIMARY = {
    "bg": BLUE_MUNSELL, 
    "fg": WHITE, 
    "font": (FONT_PRIMARY, FONT_SIZE_NORMAL, "bold"),
    "relief": 'flat', 
    "bd": 0, 
    "cursor": "hand2",
    "activebackground": INDIGO_DYE,
    "activeforeground": WHITE
}

BUTTON_STYLE_SECONDARY = {
    "bg": WHITE, 
    "fg": BLUE_MUNSELL, 
    "font": (FONT_PRIMARY, FONT_SIZE_NORMAL, "bold"),
    "relief": 'flat', 
    "bd": 1, 
    "cursor": "hand2",
    "activebackground": LIGHT_GRAY,
    "activeforeground": INDIGO_DYE
}

# Estilo para los botones de la barra de navegación
NAVBAR_BUTTON_STYLE = {
    "bg": BLUE_MUNSELL,
    "fg": WHITE,
    "font": (FONT_PRIMARY, FONT_SIZE_NORMAL, "bold"),
    "relief": 'flat',
    "bd": 0,
    "activebackground": INDIGO_DYE,
    "activeforeground": WHITE
}
