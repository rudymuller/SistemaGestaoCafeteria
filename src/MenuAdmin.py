import tkinter as tk
from tkinter import messagebox


class MenuAdmin:
    """Tela principal do menu administrativo."""

    def __init__(self, app, login_instance):
        self.app = app
        self.login_instance = login_instance
        self.win, self.frame = app._new_menu_window(login_instance, "Menu Administrativo")
        self.render()

    def render(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.frame,
            text="Menu Administrativo",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(4, 12))
        tk.Label(
            self.frame,
            text="Aqui você encontrará opções administrativas:",
            wraplength=380,
            justify=tk.CENTER,
        ).pack(pady=6)

        menu_frame = tk.Frame(self.frame)
        menu_frame.pack(pady=(8, 6))
        tk.Button(
            menu_frame,
            text="Pedidos",
            width=40,
            command=self.open_pedidos,
        ).grid(row=0, column=0, padx=8, pady=6)
        tk.Button(
            menu_frame,
            text="Controle",
            width=40,
            command=lambda: self.app._render_controle_menu(self.frame, self.win, self.render),
        ).grid(row=0, column=1, padx=8, pady=6)

        self.app._maximize_window(self.win)
        self.app._add_navigation_buttons(self.frame, self.win, self.render)

    def open_pedidos(self):
        try:
            from Pedidos import Pedidos
            Pedidos()
            messagebox.showinfo("Pedidos", "Abrindo módulo Pedidos (placeholder)")
        except Exception:
            messagebox.showinfo("Pedidos", "Módulo Pedidos não implementado - placeholder.")