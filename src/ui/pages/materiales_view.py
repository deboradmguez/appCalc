import customtkinter as ctk
from tkinter import messagebox

class MaterialesView(ctk.CTkFrame):
    def __init__(self, master, master_app, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.supabase_client = master_app.supabase_client
        self.materials_data = []

        ctk.CTkLabel(self, text="Página de Materiales (En Construcción)", font=("", 22, "bold")).pack(expand=True)