import customtkinter as ctk
from typing import List, Callable, Optional

class CTkListbox(ctk.CTkScrollableFrame):
    """
    Un Listbox personalizado usando CustomTkinter que reemplaza tk.Listbox
    para mantener consistencia visual.
    """
    
    def __init__(self, master, command: Optional[Callable] = None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.command = command
        self.buttons: List[ctk.CTkButton] = []
        self.values: List[str] = []
        self.selected_index: Optional[int] = None
        self.selected_button: Optional[ctk.CTkButton] = None
        
        # Configuración del scrollable frame
        self._scrollbar.configure(width=16)

    def insert(self, index, value: str):
        """Inserta un elemento en la posición especificada."""
        if index == "end" or index >= len(self.values):
            self.values.append(value)
            self._create_button(value, len(self.values) - 1)
        else:
            self.values.insert(index, value)
            self._refresh_all_buttons()

    def delete(self, start, end=None):
        """Elimina elementos del listbox."""
        if start == "all" or (start == 0 and end == "end"):
            self.clear()
            return
            
        if end is None:
            end = start
            
        # Eliminar valores
        if end == "end":
            del self.values[start:]
        else:
            del self.values[start:end + 1]
            
        self._refresh_all_buttons()

    def clear(self):
        """Limpia todos los elementos del listbox."""
        self.values.clear()
        self.selected_index = None
        self.selected_button = None
        
        # Destruir todos los botones
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()

    def curselection(self) -> tuple:
        """Devuelve una tupla con los índices seleccionados."""
        if self.selected_index is not None:
            return (self.selected_index,)
        return ()

    def selection_clear(self, first=0, last="end"):
        """Limpia la selección."""
        if self.selected_button:
            self.selected_button.configure(fg_color="transparent")
        self.selected_index = None
        self.selected_button = None

    def get(self, index) -> str:
        """Obtiene el valor en el índice especificado."""
        if 0 <= index < len(self.values):
            return self.values[index]
        return ""

    def size(self) -> int:
        """Devuelve el número de elementos."""
        return len(self.values)

    def _create_button(self, text: str, index: int):
        """Crea un botón para un elemento de la lista."""
        button = ctk.CTkButton(
            self,
            text=text,
            fg_color="transparent",
            text_color=("gray10", "gray90"),
            hover_color=("gray80", "gray25"),
            anchor="w",
            height=32,
            corner_radius=6,
            font=ctk.CTkFont(size=12),
            command=lambda: self._on_button_click(index)
        )
        button.pack(fill="x", pady=1, padx=5)
        
        if index < len(self.buttons):
            self.buttons[index] = button
        else:
            self.buttons.append(button)

    def _on_button_click(self, index: int):
        """Maneja el clic en un botón de la lista."""
        # Deseleccionar el botón anterior
        if self.selected_button:
            self.selected_button.configure(fg_color="transparent")
        
        # Seleccionar el nuevo botón
        self.selected_index = index
        self.selected_button = self.buttons[index]
        self.selected_button.configure(fg_color=("gray70", "gray30"))
        
        # Ejecutar comando si existe
        if self.command:
            self.command()

    def _refresh_all_buttons(self):
        """Refresca todos los botones después de cambios en los valores."""
        # Destruir botones existentes
        for button in self.buttons:
            button.destroy()
        self.buttons.clear()
        
        # Recrear botones
        for i, value in enumerate(self.values):
            self._create_button(value, i)
        
        # Limpiar selección si el índice ya no es válido
        if self.selected_index is not None and self.selected_index >= len(self.values):
            self.selected_index = None
            self.selected_button = None


# Función helper para reemplazar fácilmente tk.Listbox
def replace_tk_listbox_with_ctk(parent, **listbox_style):
    """
    Función helper para reemplazar tk.Listbox con CTkListbox
    manteniendo la misma API básica.
    """
    # Ignorar estilos específicos de tk.Listbox
    ctk_kwargs = {}
    
    if 'selectmode' in listbox_style:
        # Por ahora solo soportamos selección simple
        pass
    
    return CTkListbox(parent, **ctk_kwargs)