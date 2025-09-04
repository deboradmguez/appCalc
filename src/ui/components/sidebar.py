# src/ui/components/sidebar.py

import customtkinter as ctk
from PIL import Image
from pathlib import Path
import unicodedata # NEW: For better string normalization

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, commands, **kwargs):
        super().__init__(master, corner_radius=0, **kwargs)
        
        self.commands = commands
        self.is_expanded = True
        self.animation_in_progress = False
        self.after_id = None
        
        # --- CONSTANTS ---
        self.EXPANDED_WIDTH = 220
        self.COLLAPSED_WIDTH = 75
        self.ANIMATION_STEP = 15 # NEW
        self.ANIMATION_DELAY = 10 # NEW
        
        # Initial configuration
        self.configure(width=self.EXPANDED_WIDTH)

        # Load assets
        self.icons = self._load_icons()
        
        # --- WIDGETS ---
        # Frame for the top menu button
        self.menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.menu_frame.pack(fill="x", pady=(15, 10), padx=15)
        
        # Frame for the main navigation buttons
        self.button_container = ctk.CTkFrame(self, fg_color="transparent")
        self.button_container.pack(fill="y", expand=True, anchor="n") # CHANGED: anchor="n" to keep buttons at the top

        # Menu toggle button
        self.menu_btn = self._create_button(
            self.menu_frame, 
            self.icons["menu"], 
            " Menú", 
            self.toggle_sidebar
        )
        self.menu_btn.pack(anchor="w")

        # Navigation buttons
        self.nav_buttons = {}
        for name, command in self.commands.items():
            # NEW: More robust way to find icon names from command names
            icon_name = self._normalize_str(name)
            icon = self.icons.get(icon_name, self.icons["proyectos"]) # Default to 'proyectos' icon
            
            btn = self._create_button(self.button_container, icon, f" {name}", command)
            btn.pack(pady=5, padx=15, anchor="w")
            self.nav_buttons[name] = btn

    def _normalize_str(self, s):
        # NEW: Helper to remove accents for matching icon files
        return "".join(
            c for c in unicodedata.normalize('NFD', s.lower())
            if unicodedata.category(c) != 'Mn'
        )

    def _load_icons(self):
        icon_path = Path(__file__).resolve().parent.parent.parent / "assets" / "icons"
        # The icon names should match the normalized command names
        icon_names = ["menu", "proyectos", "materiales", "areas", "configuracion"]
        icons = {}
        for name in icon_names:
            try:
                img = Image.open(icon_path / f"{name}.png")
                icons[name] = ctk.CTkImage(img, size=(22, 22))
            except FileNotFoundError:
                # Create a blank image if the icon is not found
                img = Image.new('RGBA', (22, 22), (0, 0, 0, 0)) 
                icons[name] = ctk.CTkImage(img, size=(22, 22))
        return icons

    def _create_button(self, parent, icon, text, command):
        return ctk.CTkButton(
            parent, 
            image=icon, 
            text=text, 
            command=command,
            fg_color="transparent", 
            anchor="w",
            font=ctk.CTkFont(size=14, weight="bold")
        )

    def toggle_sidebar(self):
        if self.animation_in_progress:
            return
        
        self.animation_in_progress = True
        
        if self.is_expanded:
            # --- Collapse Animation ---
            # First, hide the text from all buttons
            self.menu_btn.configure(text="")
            for btn in self.nav_buttons.values():
                btn.configure(text="")
            self.animate_width(self.COLLAPSED_WIDTH)
        else:
            # --- Expand Animation ---
            # The text will be restored after the animation finishes
            self.animate_width(self.EXPANDED_WIDTH)
    
    def animate_width(self, target_width):
        current_width = self.winfo_width()

        # Stop condition
        if current_width == target_width:
            self.animation_in_progress = False
            # CHANGED: Toggle state and restore text at the END of the animation
            self.is_expanded = not self.is_expanded
            if self.is_expanded:
                self.menu_btn.configure(text=" Menú")
                for name, btn in self.nav_buttons.items():
                    btn.configure(text=f" {name}")
            return

        # Determine direction and calculate new width
        if target_width > current_width:
            new_width = min(current_width + self.ANIMATION_STEP, target_width)
        else:
            new_width = max(current_width - self.ANIMATION_STEP, target_width)
        
        # Apply the new width
        self.configure(width=new_width)
        
        # Schedule the next step
        self.after_id = self.after(self.ANIMATION_DELAY, self.animate_width, target_width)

    def destroy(self):
        # Crucial cleanup to prevent errors when closing the app mid-animation
        if self.after_id:
            self.after_cancel(self.after_id)
        super().destroy()