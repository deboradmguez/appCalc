# notification_system.py (Refactored for CustomTkinter)

import customtkinter as ctk

# Colores predefinidos que puedes usar. Podrías moverlos a un archivo de configuración.
SUCCESS_COLOR = "#2a9d8f"
ERROR_COLOR = "#e76f51"
WHITE = "#FFFFFF"

class NotificationSystem:
    def __init__(self, parent):
        self.parent = parent
        self.notification_frame = None
        self.active_notifications = []

    def pack_notification_frame(self):
        """
        Crea y empaqueta el frame de notificaciones en la parte superior.
        """
        # Usamos un CTkFrame que se coloca sobre el resto del contenido
        self.notification_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.notification_frame.place(relx=0.98, y=20, anchor="ne")

    def show_success(self, message):
        self.show_notification(message, SUCCESS_COLOR, "✓")

    def show_error(self, message):
        self.show_notification(message, ERROR_COLOR, "✕")

    def show_notification(self, message, color, icon=None):
        if self.notification_frame is None:
            self.pack_notification_frame()

        notification_id = len(self.active_notifications)
        
        # --- Frame de notificación con CTkFrame ---
        notif_frame = ctk.CTkFrame(self.notification_frame, fg_color=color, corner_radius=6)
        notif_frame.pack(pady=4, padx=10, fill='x', anchor='e')
        
        if icon:
            icon_label = ctk.CTkLabel(notif_frame, text=icon, font=ctk.CTkFont(size=16, weight="bold"))
            icon_label.pack(side="left", padx=(10, 5))
        
        message_label = ctk.CTkLabel(notif_frame, text=message, wraplength=350, justify="left")
        message_label.pack(side="left", fill='x', expand=True, padx=(0, 10), pady=10)
        
        close_btn = ctk.CTkLabel(notif_frame, text="×", font=ctk.CTkFont(size=18, weight="bold"), cursor="hand2")
        close_btn.pack(side="right", padx=(0, 10))
        close_btn.bind("<Button-1>", lambda e: self.remove_notification(notification_id))
        
        self.active_notifications.append(notif_frame)
        
        self.parent.after(3000, lambda: self.remove_notification(notification_id))

    def remove_notification(self, notification_id):
        if notification_id < len(self.active_notifications):
            notif_frame = self.active_notifications[notification_id]
            # Verificar si el widget todavía existe antes de destruirlo
            if notif_frame and notif_frame.winfo_exists():
                notif_frame.destroy()
            self.active_notifications[notification_id] = None