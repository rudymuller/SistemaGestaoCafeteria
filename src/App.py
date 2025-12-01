import tkinter as tk
from tkinter import messagebox, ttk, font as tkfont
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
		width, height = WIN_WIDTH, WIN_HEIGHT
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
					# Render the users management view inside the same frame
					from Usuario import Usuario

					u_mgr = Usuario()

					# clear frame
					for w in list(frm.winfo_children()):
						w.destroy()

					title = tk.Label(frm, text="Gerenciamento de Usuários", font=("Segoe UI", 14, "bold"))
					title.pack(pady=(4, 8))

					# add button always visible
					ctrl_top = tk.Frame(frm)
					ctrl_top.pack(fill=tk.X, pady=(0, 8))

					def on_add():
						# open modal to add a user
						add_win = tk.Toplevel(win)
						add_win.title('Adicionar Usuário')
						add_win.geometry('480x360')
						frm_add = tk.Frame(add_win, padx=12, pady=12)
						frm_add.pack(expand=True, fill=tk.BOTH)

						labels = ['Nome', 'Sobrenome', 'CPF', 'Nome de usuário', 'Senha', 'Data admissão', 'Tipo acesso']
						entries = {}
						for i, lbl in enumerate(labels):
							tk.Label(frm_add, text=lbl+':').grid(row=i, column=0, sticky=tk.W, pady=4)
							if lbl == 'Tipo acesso':
								combo = ttk.Combobox(frm_add, values=['Administrador', 'Funcionário'], state='readonly', width=33)
								combo.grid(row=i, column=1, pady=4, padx=6)
								entries[lbl] = combo
							else:
								e = tk.Entry(frm_add, width=36, show='*' if lbl == 'Senha' else None)
								e.grid(row=i, column=1, pady=4, padx=6)
								entries[lbl] = e

						def submit_add():
							try:
								tipo_sel = entries['Tipo acesso'].get().strip()
								tipo_val = None
								if tipo_sel == 'Administrador':
									tipo_val = 'admin'
								elif tipo_sel == 'Funcionário':
									tipo_val = 'atend'

								nid = u_mgr.adicionar(
									entries['Nome'].get().strip(),
									entries['Sobrenome'].get().strip(),
									entries['CPF'].get().strip(),
									entries['Nome de usuário'].get().strip(),
									entries['Senha'].get(),
									entries['Data admissão'].get().strip() or None,
									tipo_val,
								)
								messagebox.showinfo('Usuários', f'Usuário criado (id={nid})')
								add_win.destroy()
								refresh_list()
							except Exception as ex:
								messagebox.showerror('Erro', f'Falha ao adicionar usuário: {ex}')

						btns = tk.Frame(frm_add)
						btns.grid(row=len(labels), column=0, columnspan=2, pady=(12,0))
						tk.Button(btns, text='Salvar', command=submit_add).pack(side=tk.LEFT, padx=6)
						tk.Button(btns, text='Cancelar', command=add_win.destroy).pack(side=tk.LEFT, padx=6)

					add_btn = tk.Button(ctrl_top, text='Adicionar', width=12, command=on_add)
					add_btn.pack(side=tk.LEFT)

					# Back button to return to Controle menu
					back_btn = tk.Button(ctrl_top, text='Voltar', width=12, command=render_controle_menu)
					back_btn.pack(side=tk.RIGHT)

					# Treeview list for users
					cols = ('id', 'nome', 'sobrenome', 'nome_usuario', 'cpf', 'tipo_acesso', 'ativo')
					tree = ttk.Treeview(frm, columns=cols, show='headings', selectmode='browse')
					# friendly column labels
					label_map = {
						'id': 'ID',
						'nome': 'Nome',
						'sobrenome': 'Sobrenome',
						'nome_usuario': 'Nome de Usuario',
						'cpf': 'CPF',
						'tipo_acesso': 'Tipo de acesso',
						'ativo': 'Status',
					}
					for c in cols:
						tree.heading(c, text=label_map.get(c, c), anchor=tk.CENTER)
						# initial width; will be adjusted after populating
						tree.column(c, width=120, anchor=tk.CENTER)

					# vertical scrollbar
					vsb = ttk.Scrollbar(frm, orient='vertical', command=tree.yview)
					tree.configure(yscrollcommand=vsb.set)
					tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
					vsb.pack(side=tk.LEFT, fill=tk.Y)

					# action area
					action_frame = tk.Frame(frm, padx=8)
					action_frame.pack(side=tk.RIGHT, fill=tk.Y)

					info_label = tk.Label(action_frame, text='Selecione um usuário', wraplength=180)
					info_label.pack(pady=(4,8))

					selected_user_id = {'id': None}

					def refresh_list():
						# clear
						for r in tree.get_children():
							tree.delete(r)
						users = u_mgr.listar(include_inativos=True)
						for urec in users:
							# display human-friendly tipo_acesso label
							tipo = urec.get('tipo_acesso')
							if tipo == 'admin':
								tipo_label = 'Administrador'
							elif tipo == 'atend':
								tipo_label = 'Funcionário'
							else:
								tipo_label = tipo
							tree.insert('', tk.END, values=(urec['id'], urec['nome'], urec['sobrenome'], urec['nome_usuario'], urec['cpf'], tipo_label, 'Ativo' if urec.get('ativo',1) == 1 else 'Inativo'))

						# After populating, compute column widths based on content and header
						adjust_columns()

					def adjust_columns():
						f = tkfont.Font(tree, tree.cget('font'))
						padding = 18
						for c in cols:
							# header
							header = tree.heading(c)['text']
							max_w = f.measure(str(header))
							for iid in tree.get_children():
								val = tree.set(iid, c)
								if val is None:
									val = ''
								w = f.measure(str(val))
								if w > max_w:
									max_w = w
							tree.column(c, width=max_w + padding, anchor=tk.CENTER)

					def on_select(event):
						sel = tree.selection()
						if not sel:
							return
						item = tree.item(sel[0])
						uid = item['values'][0]
						selected_user_id['id'] = uid
						info_label.config(text=f"Selecionado ID {uid}\n{item['values'][1]} {item['values'][2]}")
						# show update and remove buttons
						btn_update.pack_forget()
						btn_remove.pack_forget()
						btn_update.pack(pady=6)
						btn_remove.pack(pady=6)

					tree.bind('<<TreeviewSelect>>', on_select)

					def do_remove():
						uid = selected_user_id['id']
						if uid is None:
							messagebox.showwarning('Remover', 'Nenhum usuário selecionado')
							return
						if not messagebox.askyesno('Remover', 'Confirmar remoção permanente do usuário do banco de dados?'):
							return
						ok = u_mgr.remover(uid)
						if ok:
							messagebox.showinfo('Remover', 'Usuário removido do banco de dados')
							refresh_list()
						else:
							messagebox.showwarning('Remover', 'Falha ao remover (id não encontrado)')

					def do_update():
						uid = selected_user_id['id']
						if uid is None:
							messagebox.showwarning('Atualizar', 'Nenhum usuário selecionado')
							return
						data = u_mgr.obter(uid)
						if not data:
							messagebox.showerror('Atualizar', 'Usuário não encontrado')
							return
						upd_win = tk.Toplevel(win)
						upd_win.title('Atualizar usuário')
						upd_win.geometry('480x380')
						fup = tk.Frame(upd_win, padx=12, pady=12)
						fup.pack(expand=True, fill=tk.BOTH)

						labels = [('Nome','nome'),('Sobrenome','sobrenome'),('CPF','cpf'),('Nome de usuário','nome_usuario'),('Senha (deixe em branco para não alterar)','senha'),('Data admissão','data_admissao'),('Tipo acesso','tipo_acesso')]
						entries = {}
						for i, (lbl, key) in enumerate(labels):
							tk.Label(fup, text=lbl+':').grid(row=i, column=0, sticky=tk.W, pady=4)
							if key == 'tipo_acesso':
								# show combobox, map stored value ('admin'/'atend') to display
								combo = ttk.Combobox(fup, values=['Administrador', 'Funcionário'], state='readonly', width=33)
								combo.grid(row=i, column=1, pady=4, padx=6)
								current = data.get('tipo_acesso')
								if current == 'admin':
									combo.set('Administrador')
								elif current == 'atend':
									combo.set('Funcionário')
								entries[key] = combo
							else:
								e = tk.Entry(fup, width=36, show='*' if 'Senha' in lbl else None)
								e.grid(row=i, column=1, pady=4, padx=6)
								if key in data and data[key] is not None and key != 'senha':
									e.insert(0, str(data[key]))
								entries[key] = e

						# ativo checkbox (allow re-activation)
						ativo_var = tk.IntVar(value=1 if data.get('ativo', 1) == 1 else 0)
						tk.Label(fup, text='Ativo:').grid(row=len(labels), column=0, sticky=tk.W, pady=4)
						ativo_chk = tk.Checkbutton(fup, variable=ativo_var)
						ativo_chk.grid(row=len(labels), column=1, sticky=tk.W, pady=4, padx=6)

						def submit_update():
							fields = {}
							for key in ['nome','sobrenome','cpf','nome_usuario','data_admissao','tipo_acesso']:
								val = entries[key].get().strip()
								if val != '':
									fields[key] = val
							passwd = entries['senha'].get()
							if passwd:
								fields['senha'] = passwd
							# map tipo_acesso display back to stored value
							ta = entries['tipo_acesso'].get().strip()
							if ta == 'Administrador':
								fields['tipo_acesso'] = 'admin'
							elif ta == 'Funcionário':
								fields['tipo_acesso'] = 'atend'
							# include ativo status (1 or 0)
							fields['ativo'] = int(ativo_var.get())
							try:
								ok = u_mgr.atualizar(uid, **fields)
								if ok:
									messagebox.showinfo('Atualizar', 'Usuário atualizado com sucesso')
									upd_win.destroy()
									refresh_list()
								else:
									messagebox.showwarning('Atualizar', 'Nenhuma alteração realizada')
							except Exception as ex:
								messagebox.showerror('Erro', f'Falha ao atualizar: {ex}')

						bfr = tk.Frame(fup)
						# move buttons down one row so they don't overlap the 'Ativo' checkbox
						bfr.grid(row=len(labels) + 1, column=0, columnspan=2, pady=(12,0))
						tk.Button(bfr, text='Salvar', command=submit_update).pack(side=tk.LEFT, padx=6)
						tk.Button(bfr, text='Cancelar', command=upd_win.destroy).pack(side=tk.LEFT, padx=6)

					btn_update = tk.Button(action_frame, text='Atualizar', width=16, command=do_update)
					btn_remove = tk.Button(action_frame, text='Remover', width=16, command=do_remove)

					refresh_list()

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
    