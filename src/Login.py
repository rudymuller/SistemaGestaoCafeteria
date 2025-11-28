import tkinter as tk
from tkinter import ttk


class Login:
   """Small modal login dialog.

   Usage:
      login = Login(parent)
      creds = login.show()  # returns (username, password) or None if cancelled
   """

   def __init__(self, parent=None):
      self.parent = parent
      self.username = None
      self.password = None

   def _center(self, win, w=380, h=200):
      win.update_idletasks()
      sw = win.winfo_screenwidth()
      sh = win.winfo_screenheight()
      x = (sw - w) // 2
      y = (sh - h) // 2
      win.geometry(f"{w}x{h}+{x}+{y}")

   def show(self):
      # Create the window
      owns_root = False
      if self.parent is None:
         root = tk.Tk()
         owns_root = True
      else:
         root = tk.Toplevel(self.parent)
         root.transient(self.parent)

      root.title("Login")
      self._center(root, 420, 190)

      # Make it modal
      if self.parent is not None:
         root.grab_set()

      frm = ttk.Frame(root, padding=16)
      frm.pack(expand=True, fill=tk.BOTH)

      ttk.Label(frm, text="Usuário:").grid(row=0, column=0, sticky=tk.W)
      user_entry = ttk.Entry(frm, width=36)
      user_entry.grid(row=0, column=1, pady=6, padx=6)

      ttk.Label(frm, text="Senha:").grid(row=1, column=0, sticky=tk.W)
      pass_entry = ttk.Entry(frm, width=36, show="*")
      pass_entry.grid(row=1, column=1, pady=6, padx=6)

      result = {'value': None}

      def submit():
         u = user_entry.get().strip()
         p = pass_entry.get()
         # Accept empty values (no user creation/verification yet) but still return them
         self.username = u
         self.password = p
         result['value'] = (u, p)
         root.destroy()

      def cancel():
         result['value'] = None
         root.destroy()

      btn_frame = ttk.Frame(frm)
      btn_frame.grid(row=2, column=0, columnspan=2, pady=(12, 0))

      enter_btn = ttk.Button(btn_frame, text="Entrar", command=submit)
      enter_btn.pack(side=tk.LEFT, padx=6)

      cancel_btn = ttk.Button(btn_frame, text="Cancelar", command=cancel)
      cancel_btn.pack(side=tk.LEFT, padx=6)

      # Focus
      user_entry.focus_set()

      if owns_root:
         root.mainloop()
      else:
         # Wait for the window to be closed when used as a modal
         root.wait_window()

      return result['value']