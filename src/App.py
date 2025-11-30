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
				# If login set a userType (admin/atend), consider it a success and
				# destroy the home screen before opening the menu.
				ut = getattr(login_screen, 'userType', None)
				if ut is not None:
					if owns_root:
						root.destroy()
					else:
						root.withdraw()

					# detach the login modal from the destroyed root so the menu
					# windows will create their own root if needed
					login_screen.parent = None

					self.showMenutype(login_screen)
				else:
					# userType not set -> not a successful built-in login; inform user
					messagebox.showwarning("Login", "Credenciais não reconhecidas.\nTente novamente ou cadastre o usuário.")
			

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
			msg = tk.Label(frm, text="Aqui você encontrará opções administrativas:",
					wraplength=380, justify=tk.CENTER)
			msg.pack(pady=6)

			# Helper — render the admin menu and the controle submenu
			def open_pedidos():
				try:
					from Pedidos import Pedidos
					_ = Pedidos()
					messagebox.showinfo("Pedidos", "Abrindo módulo Pedidos (placeholder)")
				except Exception:
					messagebox.showinfo("Pedidos", "Módulo Pedidos não implementado - placeholder.")
			def render_admin_menu():
				# clear frame
				for w in list(frm.winfo_children()):
					w.destroy()

				heading = tk.Label(frm, text="Menu Administrativo", font=("Segoe UI", 14, "bold"))
				heading.pack(pady=(4, 12))

				info = tk.Label(frm, text="Escolha uma área administrativa:", wraplength=380, justify=tk.CENTER)
				info.pack(pady=6)

				# Admin options: Pedidos and Controle
				menu_frame = tk.Frame(frm)
				menu_frame.pack(pady=(8, 6))

				ped_btn = tk.Button(menu_frame, text="Pedidos", width=40, command=open_pedidos)
				ctr_btn = tk.Button(menu_frame, text="Controle", width=40, command=render_controle_menu)
				ped_btn.grid(row=0, column=0, padx=8, pady=6)
				ctr_btn.grid(row=0, column=1, padx=8, pady=6)

			def render_controle_menu():
				# replace frame contents with controle submenu
				for w in list(frm.winfo_children()):
					w.destroy()

				heading = tk.Label(frm, text="Controle — Opções", font=("Segoe UI", 14, "bold"))
				heading.pack(pady=(4, 12))

				info = tk.Label(frm, text="Gerencie usuários, estoque, gastos e faturamento:", wraplength=520, justify=tk.CENTER)
				info.pack(pady=(0, 10))

				opts = tk.Frame(frm)
				opts.pack(pady=4)

				def open_usuarios():
					try:
						from Usuario import Usuario
						_ = Usuario()
						messagebox.showinfo("Usuários", "Abrindo tela de Usuários (placeholder)")
					except Exception:
						messagebox.showinfo("Usuários", "Módulo Usuários não implementado - placeholder.")

				def open_estoque_ctrl():
					try:
						from Estoque import Estoque
						_ = Estoque()
						messagebox.showinfo("Estoque", "Abrindo tela de Estoque (placeholder)")
					except Exception:
						messagebox.showinfo("Estoque", "Módulo Estoque não implementado - placeholder.")

				def open_gastos_ctrl():
					try:
						from Gastos import Gastos
						_ = Gastos()
						messagebox.showinfo("Gastos", "Abrindo tela de Gastos (placeholder)")
					except Exception:
						messagebox.showinfo("Gastos", "Módulo Gastos não implementado - placeholder.")

				def open_faturamento():
					messagebox.showinfo("Faturamento", "Abrindo Faturamento (placeholder)")

				def open_gestao():
					messagebox.showinfo("Gestão", "Abrindo Gestão (placeholder)")

				# layout controls
				usr_btn = tk.Button(opts, text="Usuários", width=20, command=open_usuarios)
				est_btn = tk.Button(opts, text="Estoque", width=20, command=open_estoque_ctrl)
				gas_btn = tk.Button(opts, text="Gastos", width=20, command=open_gastos_ctrl)
				fat_btn = tk.Button(opts, text="Faturamento", width=20, command=open_faturamento)
				ges_btn = tk.Button(opts, text="Gestão", width=20, command=open_gestao)

				# 2-column grid
				usr_btn.grid(row=0, column=0, padx=8, pady=6)
				est_btn.grid(row=0, column=1, padx=8, pady=6)
				gas_btn.grid(row=1, column=0, padx=8, pady=6)
				fat_btn.grid(row=1, column=1, padx=8, pady=6)
				ges_btn.grid(row=2, column=0, columnspan=2, padx=8, pady=6)

				# Back button
				back_frm = tk.Frame(frm)
				back_frm.pack(pady=(10, 0))
				back_btn = tk.Button(back_frm, text="Voltar", width=12, command=render_admin_menu)
				back_btn.pack()

			# render the initial admin menu
			render_admin_menu()
			# maximize the menu window (Windows uses 'zoomed')
			try:
				win.state('zoomed')
			except Exception:
				# fallback: set fullscreen attribute as a last resort
				try:
					win.attributes('-zoomed', True)
				except Exception:
					win.attributes('-fullscreen', True)
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
			# maximize
			try:
				win.state('zoomed')
			except Exception:
				try:
					win.attributes('-zoomed', True)
				except Exception:
					win.attributes('-fullscreen', True)
		else:
			messagebox.showwarning("Tipo de usuário", "Tipo de usuário não identificado (userType=None).\nVerifique as credenciais ou cadastre o usuário.")
    