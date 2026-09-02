import tkinter as tk
from tkinter import messagebox


class MenuFunc:
    """Tela principal do menu de atendimento."""

    def __init__(self, app, login_instance):
        self.app = app
        self.login_instance = login_instance
        self.win, self.frame = app._new_menu_window(login_instance, "Menu de Atendimento")
        self.render()

    def render(self):
        tk.Label(
            self.frame,
            text="Menu de Atendimento",
            font=("Segoe UI", 14, "bold"),
        ).pack(pady=(4, 12))
        tk.Label(
            self.frame,
            text="Selecione uma opção para continuar:",
            wraplength=380,
            justify=tk.CENTER,
        ).pack(pady=6)

        options = tk.Frame(self.frame)
        options.pack(pady=(8, 6))
        tk.Button(
            options,
            text="Pedidos",
            width=40,
            command=lambda: self.open_placeholder("Pedidos"),
        ).pack(pady=6)
        tk.Button(
            options,
            text="Estoque",
            width=40,
            command=lambda: self.open_placeholder("Estoque"),
        ).pack(pady=6)

        self.app._maximize_window(self.win)

    def open_placeholder(self, title):
        messagebox.showinfo(title, f"Abrindo {title} (placeholder)")