import customtkinter as ctk
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))
from config import *

class ConfiguracionView(ctk.CTkFrame):
    def __init__(self, master, on_logout):
        super().__init__(master, fg_color=DARK_GRAY)
        self.on_logout = on_logout
        ctk.CTkLabel(self, text="Configuración", font=(FONT_PRIMARY, FONT_SIZE_TITLE, "bold")).pack(pady=30, padx=30, anchor="w")
        ctk.CTkButton(self, text="Cerrar Sesión", command=self.on_logout, width=150, height=40).pack(pady=20, padx=30, anchor="w")