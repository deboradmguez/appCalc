import tkinter as tk
from tkinter import ttk

# Importación de la configuración
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))
from config import *

class NotificationSystem:
    def __init__(self, parent):
        self.parent = parent
        self.notification_frame = None
        self.active_notifications = []  # Para llevar un registro de notificaciones activas

    def pack_notification_frame(self):
        """
        Crea y empaqueta el frame de notificaciones.
        Este método se llama una vez al inicializar la ventana principal.
        """
        self.notification_frame = tk.Frame(self.parent, bg=self.parent['bg'])
        self.notification_frame.pack(side=tk.TOP, fill=tk.X, padx=20, pady=5)

    def show_success(self, message):
        """
        Muestra una notificación de éxito.
        """
        self.show_notification(message, SUCCESS_COLOR, "✓")

    def show_error(self, message):
        """
        Muestra una notificación de error.
        """
        self.show_notification(message, ERROR_COLOR, "✕")

    def show_notification(self, message, color, icon=None):
        """
        Crea y muestra una notificación temporal con diseño mejorado.
        """
        if self.notification_frame is None:
            self.pack_notification_frame()

        # Crear un frame para la notificación con bordes redondeados (simulados)
        notification_id = len(self.active_notifications)
        notif_frame = tk.Frame(self.notification_frame, bg=color, relief='flat', height=30)
        notif_frame.pack(fill='x', pady=2)
        notif_frame.pack_propagate(False)  # Evitar que el frame se ajuste al contenido
        
        # Frame interno para mejor control del padding
        inner_frame = tk.Frame(notif_frame, bg=color)
        inner_frame.pack(fill='both', expand=True, padx=1, pady=1)
        
        # Icono (si se proporciona)
        if icon:
            icon_label = tk.Label(inner_frame, text=icon, bg=color, fg=WHITE, 
                                 font=(FONT_PRIMARY, FONT_SIZE_SMALL, "bold"))
            icon_label.pack(side=tk.LEFT, padx=(10, 5))
        
        # Mensaje
        message_label = tk.Label(inner_frame, text=message, bg=color, fg=WHITE, 
                                font=(FONT_PRIMARY, FONT_SIZE_SMALL), wraplength=400)
        message_label.pack(side=tk.LEFT, fill='x', expand=True, padx=(0, 10), pady=5)
        
        # Botón de cerrar (opcional)
        close_btn = tk.Label(inner_frame, text="×", bg=color, fg=WHITE, 
                            font=(FONT_PRIMARY, FONT_SIZE_NORMAL, "bold"), cursor="hand2")
        close_btn.pack(side=tk.RIGHT, padx=(0, 10))
        close_btn.bind("<Button-1>", lambda e: self.remove_notification(notification_id))
        
        # Agregar a la lista de notificaciones activas
        notification_data = {
            'frame': notif_frame,
            'inner_frame': inner_frame,
            'message_label': message_label,
            'close_btn': close_btn,
            'icon_label': icon_label if icon else None
        }
        self.active_notifications.append(notification_data)
        
        # Ocultar la notificación después de 3 segundos
        self.parent.after(3000, lambda: self.remove_notification(notification_id))

    def remove_notification(self, notification_id):
        """
        Elimina una notificación específica.
        """
        if notification_id < len(self.active_notifications):
            notification = self.active_notifications[notification_id]
            notification['frame'].destroy()
            # Marcar como None para mantener los índices consistentes
            self.active_notifications[notification_id] = None