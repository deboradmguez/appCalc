# src/ui/pages/configuracion_view.py

import customtkinter as ctk
from config import * # Solo para los tamaños

class ConfiguracionView(ctk.CTkFrame):
    def __init__(self, master, master_app, on_logout, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.on_logout = on_logout
        
        # --- CORRECCIÓN DE FUENTE ---
        ctk.CTkLabel(self, text="Configuración", font=ctk.CTkFont(size=FONT_SIZE_TITLE, weight="bold")).pack(pady=30, padx=10, anchor="w")
        ctk.CTkButton(self, text="Cerrar Sesión", command=self.on_logout, width=150, height=40).pack(pady=20, padx=10, anchor="w")