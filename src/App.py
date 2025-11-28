import tkinter as tk
from tkinter import messagebox


class App:
	def telaInicial(self, root=None):
		"""Create a simple desktop home screen (Tkinter) with a welcome message.

		If `root` is provided, a Toplevel window will be used so this method
		can be embedded in larger apps. Otherwise a new Tk root will be created
		and mainloop will be run.
		"""
		owns_root = False
		if root is None:
			root = tk.Tk()
			owns_root = True

		# Configure window
		root.title("Sistema de Gestão da Cafeteria")
		width, height = 600, 320
		screen_w = root.winfo_screenwidth()
		screen_h = root.winfo_screenheight()
		x = (screen_w - width) // 2
		y = (screen_h - height) // 2
		root.geometry(f"{width}x{height}+{x}+{y}")

		# Root frame
		frame = tk.Frame(root, padx=20, pady=20)
		frame.pack(expand=True, fill=tk.BOTH)

		# Welcome message
		title = tk.Label(frame, text="Bem-vindo ao Sistema de Gestão da Cafeteria",
						 font=("Segoe UI", 18, "bold"), wraplength=520, justify=tk.CENTER)
		title.pack(pady=(10, 18))

		subtitle = tk.Label(frame, text="Organize pedidos, estoque e gastos com simplicidade.",
							font=("Segoe UI", 12), fg="#333333")
		subtitle.pack(pady=(0, 18))

		# Buttons
		btn_frame = tk.Frame(frame)
		btn_frame.pack(pady=10)

		def on_enter():
			# Open the Login modal and handle returned credentials
			from Login import Login
			login_screen = Login(parent=root)
			creds = login_screen.show()
			if creds is None:
				messagebox.showinfo("Login", "Login cancelado.")
			else:
				username, password = creds
				# We don't create users yet; just show what was entered as a placeholder
				messagebox.showinfo("Login", f"Usuário: {username}\nSenha: {'*' * len(password)}")
			

		enter_btn = tk.Button(btn_frame, text="Entrar", width=12, command=on_enter)
		enter_btn.grid(row=0, column=0, padx=8)

		def on_exit():
			if owns_root:
				root.destroy()
			else:
				root.withdraw()

		exit_btn = tk.Button(btn_frame, text="Sair", width=12, command=on_exit)
		exit_btn.grid(row=0, column=1, padx=8)

		# Make the window non-resizable for a cleaner welcome screen
		root.resizable(False, False)

		if owns_root:
			root.mainloop()
    