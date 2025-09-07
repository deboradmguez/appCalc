# config.py - Esquema de colores mejorado para construcción

# === PALETA DE COLORES PRINCIPAL ===
# Inspirada en materiales de construcción con tonos más suaves y profesionales

# Colores base - Tonos tierra y cemento
BACKGROUND_PRIMARY = "#F5F6FA"      # Gris muy claro, casi blanco (fondo principal)
BACKGROUND_SECONDARY = "#E8EAF0"    # Gris claro suave (contenedores)
BACKGROUND_CARD = "#FFFFFF"         # Blanco puro (tarjetas)

# Sidebar - Tonos tierra más suaves
SIDEBAR_PRIMARY = "#6B7280"         # Gris azulado elegante
SIDEBAR_HOVER = "#4B5563"          # Gris más oscuro para hover
SIDEBAR_SELECTED = "#374151"        # Gris oscuro para selección

# Acentos - Naranja construcción más refinado
ACCENT_PRIMARY = "#F97316"          # Naranja vibrante pero elegante
ACCENT_HOVER = "#EA580C"           # Naranja más oscuro para hover
ACCENT_LIGHT = "#FED7AA"           # Naranja muy claro para fondos
ACCENT_BORDER = "#FB923C"          # Naranja medio para bordes

# Textos
TEXT_PRIMARY = "#111827"            # Negro suave para texto principal
TEXT_SECONDARY = "#6B7280"          # Gris medio para texto secundario
TEXT_ON_DARK = "#F9FAFB"           # Blanco cremoso para texto en fondos oscuros
TEXT_ON_ACCENT = "#FFFFFF"         # Blanco puro para texto en acentos

# Estados y feedback
SUCCESS_COLOR = "#10B981"           # Verde esmeralda
WARNING_COLOR = "#F59E0B"           # Ámbar
ERROR_COLOR = "#EF4444"             # Rojo coral
INFO_COLOR = "#3B82F6"              # Azul
NEUTRAL_COLOR = "#8B5CF6"           # Púrpura para elementos neutrales

# Bordes y líneas
BORDER_PRIMARY = "#D1D5DB"          # Gris claro
BORDER_FOCUS = "#F97316"            # Naranja para elementos enfocados
BORDER_ERROR = "#EF4444"            # Rojo para errores

# Colores especiales para transparencia
TRANSPARENT_BG = "transparent"               # Para fg_color transparente
TRANSPARENT_HOVER = "#F3F4F6"       # Color suave para hover en elementos transparentes

# Sombras (para efectos de profundidad)
SHADOW_LIGHT = "rgba(0, 0, 0, 0.05)"
SHADOW_MEDIUM = "rgba(0, 0, 0, 0.1)"
SHADOW_STRONG = "rgba(0, 0, 0, 0.15)"

# === CONFIGURACIÓN DE FUENTES ===
FONT_SIZE_TITLE = 22
FONT_SIZE_LARGE = 18
FONT_SIZE_NORMAL = 14
FONT_SIZE_SMALL = 12

# === CONFIGURACIÓN DE VENTANA ===
WINDOW_MIN_WIDTH = 1200
WINDOW_MIN_HEIGHT = 700
START_MAXIMIZED = True  # Cambiar a False si prefieres tamaño normal

# === UTILIDADES DE APLICACIÓN DE COLORES ===
def get_login_colors():
    """Colores específicos para la ventana de login"""
    return {
        'frame_bg': BACKGROUND_CARD,
        'frame_border': ACCENT_PRIMARY,
        'input_border': BORDER_PRIMARY,
        'input_focus_border': ACCENT_PRIMARY,
        'button_bg': ACCENT_PRIMARY,
        'button_hover': ACCENT_HOVER,
        'text_primary': TEXT_PRIMARY,
        'text_secondary': TEXT_SECONDARY,
        'accent_text': ACCENT_PRIMARY
    }

def get_sidebar_colors():
    """Colores específicos para el sidebar"""
    return {
        'bg': SIDEBAR_PRIMARY,
        'hover': SIDEBAR_HOVER,
        'selected': SIDEBAR_SELECTED,
        'text': TEXT_ON_DARK,
        'button_transparent': TRANSPARENT_BG
    }

def get_main_colors():
    """Colores específicos para ventana principal"""
    return {
        'bg_primary': BACKGROUND_PRIMARY,
        'bg_secondary': BACKGROUND_SECONDARY,
        'card_bg': BACKGROUND_CARD,
        'text_primary': TEXT_PRIMARY,
        'text_secondary': TEXT_SECONDARY,
        'accent': ACCENT_PRIMARY,
        'border': BORDER_PRIMARY
    }