import tkinter as tk

# --- Paleta de Colores Moderna (Tema Oscuro) ---
GRAPHITE = "#2b2b2b"      # Fondo principal oscuro
DARK_GRAY = "#3c3f41"     # Fondo secundario para widgets
MEDIUM_GRAY = "#555555"   # Bordes y elementos inactivos
LIGHT_GRAY_TEXT = "#bbbbbb" # Texto secundario o de ayuda
NEAR_WHITE = "#f5f5f5"     # Texto principal
ACCENT_CYAN = "#00a8cc"    # Color primario para botones y highlights
ACCENT_CYAN_DARK = "#008aab" # Para el efecto "active" del botón
SUCCESS_COLOR = "#2ecc71"
ERROR_COLOR = "#e74c3c"
WHITE = "#ffffff"

# --- Fuentes ---
# La función para detectar la fuente del sistema es excelente, la mantenemos.
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

FONT_PRIMARY = get_system_font()
# Tamaños de fuente ajustados para una mejor jerarquía visual
FONT_SIZE_TITLE = 20
FONT_SIZE_LARGE = 16
FONT_SIZE_NORMAL = 12
FONT_SIZE_SMALL = 10

# --- Estilos de Widgets ---

# Estilo para campos de entrada (Entry)
ENTRY_STYLE = {
    "font": (FONT_PRIMARY, FONT_SIZE_NORMAL), 
    "bg": DARK_GRAY,
    "fg": NEAR_WHITE,
    "relief": 'flat', 
    "bd": 0, 
    "highlightthickness": 2,
    "highlightcolor": ACCENT_CYAN,
    "highlightbackground": MEDIUM_GRAY,
    "insertbackground": NEAR_WHITE # Color del cursor de texto
}

# Estilo para botones primarios (Acción principal)
BUTTON_STYLE_PRIMARY = {
    "bg": ACCENT_CYAN, 
    "fg": WHITE, 
    "font": (FONT_PRIMARY, FONT_SIZE_NORMAL, "bold"),
    "relief": 'flat', 
    "bd": 0, 
    "cursor": "hand2",
    "activebackground": ACCENT_CYAN_DARK,
    "activeforeground": WHITE
}

# Estilo para botones secundarios (Acciones alternativas o "ghost button")
BUTTON_STYLE_SECONDARY = {
    "bg": DARK_GRAY, 
    "fg": NEAR_WHITE, 
    "font": (FONT_PRIMARY, FONT_SIZE_NORMAL),
    "relief": 'flat', 
    "bd": 0, 
    "cursor": "hand2",
    "activebackground": MEDIUM_GRAY,
    "activeforeground": WHITE,
    "highlightthickness": 1,
    "highlightbackground": MEDIUM_GRAY
}

# Estilo para botones de la barra de navegación
NAVBAR_BUTTON_STYLE = {
    "bg": GRAPHITE, # Fondo igual al de la barra para que parezcan integrados
    "fg": LIGHT_GRAY_TEXT,
    "font": (FONT_PRIMARY, FONT_SIZE_NORMAL, "bold"),
    "relief": 'flat',
    "bd": 0,
    "cursor": "hand2",
    "activebackground": DARK_GRAY,
    "activeforeground": ACCENT_CYAN
}

# Estilo para Listbox
LISTBOX_STYLE = {
    "font": (FONT_PRIMARY, FONT_SIZE_NORMAL),
    "bg": DARK_GRAY,
    "fg": NEAR_WHITE,
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 1,
    "highlightbackground": MEDIUM_GRAY,
    "selectbackground": ACCENT_CYAN,
    "selectforeground": WHITE
}