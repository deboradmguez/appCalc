import tkinter
import customtkinter as ctk
import logging

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))
from config import *

class ProyectosPage(ctk.CTkFrame):
    def __init__(self, master, supabase_client, on_create_new, on_view_details):
        super().__init__(master, fg_color=DARK_GRAY)
        self.supabase_client = supabase_client
        self.on_create_new = on_create_new
        self.on_view_details = on_view_details
        self._build_ui()
        self.load_proyectos_list()

    def _build_ui(self):
        title_label = ctk.CTkLabel(self, text="Mis Proyectos", font=(FONT_PRIMARY, FONT_SIZE_TITLE, "bold"), text_color=NEAR_WHITE)
        title_label.pack(pady=30, padx=30, anchor="w")
        btn_crear_proyecto = ctk.CTkButton(self, text="Crear Nuevo Proyecto", command=self.on_create_new, height=40, font=(FONT_PRIMARY, FONT_SIZE_NORMAL, "bold"))
        btn_crear_proyecto.pack(pady=(0, 20), padx=30, anchor="w")
        self.proyectos_list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.proyectos_list_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

    def load_proyectos_list(self):
        for widget in self.proyectos_list_frame.winfo_children(): widget.destroy()
        try:
            proyectos = self.supabase_client.table("proyectos").select("*").order("fecha_creacion", desc=True).execute().data
            if not proyectos:
                ctk.CTkLabel(self.proyectos_list_frame, text="No hay proyectos todavía.", text_color=LIGHT_GRAY_TEXT).pack(pady=50)
            else:
                for proyecto in proyectos:
                    frame = ctk.CTkFrame(self.proyectos_list_frame, fg_color=GRAPHITE)
                    frame.pack(fill="x", pady=4)
                    info = ctk.CTkFrame(frame, fg_color="transparent")
                    info.pack(side="left", fill="x", expand=True, padx=15, pady=10)
                    ctk.CTkLabel(info, text=proyecto['nombre_proyecto'], font=(FONT_PRIMARY, FONT_SIZE_NORMAL, "bold")).pack(anchor="w")
                    ctk.CTkLabel(info, text=proyecto['direccion_proyecto'], font=(FONT_PRIMARY, FONT_SIZE_SMALL), text_color=LIGHT_GRAY_TEXT).pack(anchor="w")
                    btn = ctk.CTkButton(frame, text="Administrar", command=lambda p=proyecto: self.on_view_details(p), fg_color=DARK_GRAY, hover_color=MEDIUM_GRAY)
                    btn.pack(side="right", padx=15, pady=10)
        except Exception as e:
            logging.error(f"Error al cargar proyectos: {e}")
