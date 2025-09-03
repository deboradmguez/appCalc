"""
Configuración segura para la aplicación.
Este archivo puede ser importado sin problemas antes de inicializar CTk.
"""

# --- Configuración de CustomTkinter (solo configuración, no objetos) ---
CTK_APPEARANCE_MODE = "dark"  # "light", "dark", "system"
CTK_COLOR_THEME = "blue"      # "blue", "green", "dark-blue"

# --- Paleta de Colores ---
COLORS = {
    "bg_primary": "#212121",      # Fondo principal
    "bg_secondary": "#2b2b2b",    # Fondo secundario
    "bg_tertiary": "#3c3f41",     # Fondo terciario
    "text_primary": "#ffffff",    # Texto principal
    "text_secondary": "#bbbbbb",  # Texto secundario
    "text_muted": "#888888",      # Texto apagado
    "accent": "#1f538d",          # Color de acento
    "accent_hover": "#144870",    # Color de acento hover
    "success": "#2a9d8f",         # Color de éxito
    "error": "#e74c3c",           # Color de error
    "warning": "#f39c12",         # Color de advertencia
    "border": "#555555",          # Color de bordes
}

# --- Fuentes ---
def get_system_font():
    """Detecta la mejor fuente para el sistema."""
    try:
        import platform
        system = platform.system()
        
        if system == 'Windows':
            return "Segoe UI"
        elif system == 'Darwin':  # macOS
            return "SF Pro Display"
        else:  # Linux/Unix
            return "Ubuntu"
    except:
        return "Arial"

FONT_FAMILY = get_system_font()

# --- Tamaños de fuente ---
FONT_SIZES = {
    "title": 24,
    "subtitle": 18,
    "heading": 16,
    "body": 14,
    "body_small": 12,
    "caption": 10,
}

# --- Funciones para crear fuentes CTk (solo cuando se necesiten) ---
def create_ctk_fonts():
    """
    Crea objetos CTkFont. Solo llamar después de inicializar CTk.
    """
    try:
        import customtkinter as ctk
        return {
            "title": ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["title"], weight="bold"),
            "subtitle": ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["subtitle"], weight="bold"),
            "heading": ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["heading"], weight="bold"),
            "body": ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["body"]),
            "body_small": ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["body_small"]),
            "caption": ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["caption"]),
            "button": ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["body"], weight="bold"),
        }
    except Exception as e:
        print(f"Error creando fuentes CTk: {e}")
        return {}

# --- Funciones individuales para crear fuentes (alternativa más segura) ---
def get_title_font():
    """Crea fuente de título. Solo usar después de inicializar CTk."""
    try:
        import customtkinter as ctk
        return ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["title"], weight="bold")
    except:
        return (FONT_FAMILY, FONT_SIZES["title"], "bold")

def get_subtitle_font():
    """Crea fuente de subtítulo. Solo usar después de inicializar CTk."""
    try:
        import customtkinter as ctk
        return ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["subtitle"], weight="bold")
    except:
        return (FONT_FAMILY, FONT_SIZES["subtitle"], "bold")

def get_heading_font():
    """Crea fuente de encabezado. Solo usar después de inicializar CTk."""
    try:
        import customtkinter as ctk
        return ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["heading"], weight="bold")
    except:
        return (FONT_FAMILY, FONT_SIZES["heading"], "bold")

def get_body_font():
    """Crea fuente de cuerpo. Solo usar después de inicializar CTk."""
    try:
        import customtkinter as ctk
        return ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["body"])
    except:
        return (FONT_FAMILY, FONT_SIZES["body"])

def get_button_font():
    """Crea fuente de botón. Solo usar después de inicializar CTk."""
    try:
        import customtkinter as ctk
        return ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["body"], weight="bold")
    except:
        return (FONT_FAMILY, FONT_SIZES["body"], "bold")

# --- Configuración de fuentes como tuplas (para tkinter nativo) ---
FONTS = {
    "title": (FONT_FAMILY, FONT_SIZES["title"], "bold"),
    "subtitle": (FONT_FAMILY, FONT_SIZES["subtitle"], "bold"),
    "heading": (FONT_FAMILY, FONT_SIZES["heading"], "bold"),
    "body": (FONT_FAMILY, FONT_SIZES["body"]),
    "body_small": (FONT_FAMILY, FONT_SIZES["body_small"]),
    "caption": (FONT_FAMILY, FONT_SIZES["caption"]),
    "button": (FONT_FAMILY, FONT_SIZES["body"], "bold"),
}

# --- Estilo para elementos Tkinter nativos (como Listbox) ---
LISTBOX_STYLE = {
    "font": FONTS["body"],
    "bg": COLORS["bg_secondary"],
    "fg": COLORS["text_primary"],
    "relief": "flat",
    "bd": 0,
    "highlightthickness": 1,
    "highlightbackground": COLORS["border"],
    "selectbackground": COLORS["accent"],
    "selectforeground": COLORS["text_primary"],
    "activestyle": "none"
}

# --- Configuraciones comunes para CustomTkinter ---
WIDGET_CONFIG = {
    "entry_height": 40,
    "button_height": 40,
    "corner_radius": 6,
    "border_width": 1,
}

# --- Mantener compatibilidad con código existente ---
GRAPHITE = COLORS["bg_primary"]
DARK_GRAY = COLORS["bg_secondary"]
MEDIUM_GRAY = COLORS["bg_tertiary"]
LIGHT_GRAY_TEXT = COLORS["text_secondary"]
NEAR_WHITE = COLORS["text_primary"]
ACCENT_CYAN = COLORS["accent"]
ACCENT_CYAN_DARK = COLORS["accent_hover"]
ERROR_COLOR = COLORS["error"]
WHITE = COLORS["text_primary"]

FONT_PRIMARY = FONT_FAMILY
FONT_SIZE_TITLE = FONT_SIZES["title"]
FONT_SIZE_LARGE = FONT_SIZES["heading"]
FONT_SIZE_NORMAL = FONT_SIZES["body"]
FONT_SIZE_SMALL = FONT_SIZES["body_small"]

# --- Funciones de inicialización ---
def initialize_customtkinter():
    """
    Inicializa CustomTkinter con la configuración predefinida.
    Llamar al inicio de la aplicación.
    """
    try:
        import customtkinter as ctk
        ctk.set_appearance_mode(CTK_APPEARANCE_MODE)
        ctk.set_default_color_theme(CTK_COLOR_THEME)
        return True
    except Exception as e:
        print(f"Error inicializando CustomTkinter: {e}")
        return False

def get_safe_font(font_type="body"):
    """
    Obtiene una fuente de forma segura, devolviendo tupla si CTk no está disponible.
    """
    try:
        import customtkinter as ctk
        
        font_map = {
            "title": lambda: ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["title"], weight="bold"),
            "subtitle": lambda: ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["subtitle"], weight="bold"),
            "heading": lambda: ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["heading"], weight="bold"),
            "body": lambda: ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["body"]),
            "body_small": lambda: ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["body_small"]),
            "caption": lambda: ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["caption"]),
            "button": lambda: ctk.CTkFont(family=FONT_FAMILY, size=FONT_SIZES["body"], weight="bold"),
        }
        
        return font_map.get(font_type, font_map["body"])()
        
    except Exception:
        # Fallback a tuplas de tkinter
        return FONTS.get(font_type, FONTS["body"])