# src/ui/pages/proyectos_page.py (Corregido)

import customtkinter as ctk
import logging
from config import *

class ProyectosPage(ctk.CTkFrame):
    def __init__(self, master, master_app, on_create_new, on_view_details, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        # Obtenemos el cliente de la ventana principal 'App'
        self.supabase_client = master_app.supabase_client
        self.on_create_new = on_create_new
        self.on_view_details = on_view_details
        
        self._build_ui()
        self.load_proyectos_list()

    def _build_ui(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=10)
        
        title_label = ctk.CTkLabel(header_frame, text="Mis Proyectos", font=ctk.CTkFont(family=FONT_PRIMARY, size=FONT_SIZE_TITLE, weight="bold"))
        title_label.pack(side="left")
        
        btn_crear_proyecto = ctk.CTkButton(header_frame, text="+ Crear Nuevo Proyecto", command=self.on_create_new, height=35)
        btn_crear_proyecto.pack(side="right")
        
        self.proyectos_list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.proyectos_list_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def load_proyectos_list(self):
        for widget in self.proyectos_list_frame.winfo_children(): 
            widget.destroy()
            
        try:
            proyectos = self.supabase_client.table("proyectos").select("*").order("fecha_creacion", desc=True).execute().data
            if not proyectos:
                ctk.CTkLabel(self.proyectos_list_frame, text="No hay proyectos todavía. ¡Crea uno nuevo!").pack(pady=50)
            else:
                for proyecto in proyectos:
                    frame = ctk.CTkFrame(self.proyectos_list_frame)
                    frame.pack(fill="x", pady=4, ipady=10)
                    
                    info = ctk.CTkFrame(frame, fg_color="transparent")
                    info.pack(side="left", fill="x", expand=True, padx=15)
                    
                    ctk.CTkLabel(info, text=proyecto['nombre_proyecto'], font=ctk.CTkFont(family=FONT_PRIMARY, size=FONT_SIZE_NORMAL, weight="bold")).pack(anchor="w")
                    ctk.CTkLabel(info, text=proyecto['direccion_proyecto'], font=ctk.CTkFont(family=FONT_PRIMARY, size=FONT_SIZE_SMALL), text_color="gray").pack(anchor="w")
                    
                    btn = ctk.CTkButton(frame, text="Administrar", command=lambda p=proyecto: self.on_view_details(p))
                    btn.pack(side="right", padx=15)
        except Exception as e:
            logging.error(f"Error al cargar proyectos: {e}")