# config.py

import customtkinter as ctk

# Ya no es necesario definir una paleta de colores.
# CustomTkinter gestiona los colores con set_appearance_mode() y set_default_color_theme().

def get_system_font():
    """Detecta la mejor fuente para el sistema."""
    try:
        temp_root = ctk.CTk()
        temp_root.withdraw()
        system = temp_root.tk.call('tk', 'windowingsystem')
        temp_root.destroy()
        
        if system == 'win32': return "Segoe UI"
        elif system == 'aqua': return "Helvetica Neue"
        else: return "Ubuntu"
    except:
        return "Arial"

FONT_PRIMARY = get_system_font()
FONT_SIZE_TITLE = 22
FONT_SIZE_LARGE = 18
FONT_SIZE_NORMAL = 14
FONT_SIZE_SMALL = 12