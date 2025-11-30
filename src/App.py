import tkinter as tk
from tkinter import messagebox
from const import WIN_WIDTH, WIN_HEIGHT


class App:
	def homeScreen(self, root=None):
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
		width, height = WIN_HEIGHT, WIN_WIDTH
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
				# Decide menu based on the Login instance's userType attribute
				# (Login.userType: True = admin, False = atend, None = unknown)
				self.showMenutype(login_screen)
			

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

	def showMenutype(self, login_instance):
		"""Open an admin or atendimento screen based on login_instance.userType.

		- If login_instance.userType is True -> show Administrative menu screen
		- If False -> show Atendimento menu screen
		- If None -> show a message informing that the user type was not identified
		"""
		ut = getattr(login_instance, 'userType', None)
		if ut is True:
			# Admin menu
			win = tk.Toplevel() if login_instance.parent else tk.Tk()
			win.title("Menu Administrativo")
			win.geometry("420x220")
			frm = tk.Frame(win, padx=16, pady=16)
			frm.pack(expand=True, fill=tk.BOTH)
			label = tk.Label(frm, text="Menu Administrativo", font=("Segoe UI", 14, "bold"))
			label.pack(pady=(4, 12))
			msg = tk.Label(frm, text="Aqui você encontrará opções administrativas (placeholder).",
					wraplength=380, justify=tk.CENTER)
			msg.pack(pady=6)
			win.resizable(False, False)
		elif ut is False:
			# Atendimento menu
			win = tk.Toplevel() if login_instance.parent else tk.Tk()
			win.title("Menu de Atendimento")
			win.geometry("420x220")
			frm = tk.Frame(win, padx=16, pady=16)
			frm.pack(expand=True, fill=tk.BOTH)
			label = tk.Label(frm, text="Menu de Atendimento", font=("Segoe UI", 14, "bold"))
			label.pack(pady=(4, 12))
			msg = tk.Label(frm, text="Aqui você encontrará opções de atendimento (placeholder).",
					wraplength=380, justify=tk.CENTER)
			msg.pack(pady=6)
			win.resizable(False, False)
		else:
			messagebox.showwarning("Tipo de usuário", "Tipo de usuário não identificado (userType=None).\nVerifique as credenciais ou cadastre o usuário.")
    