import tkinter as tk
from tkinter import messagebox, simpledialog  # ✅ simpledialog agregado
from database import Database

db = Database()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Login de Bot")
        self.root.geometry("300x250")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.credits = None
        self.logged_user = None

        # UI Login
        tk.Label(root, text="Usuario:").pack(pady=5)
        tk.Entry(root, textvariable=self.username_var).pack()

        tk.Label(root, text="Contraseña:").pack(pady=5)
        tk.Entry(root, textvariable=self.password_var, show="*").pack()

        tk.Button(root, text="Iniciar sesión", command=self.login).pack(pady=8)
        tk.Button(root, text="Registrar nuevo usuario", command=self.register_user).pack(pady=2)

        self.credit_label = tk.Label(root, text="")
        self.credit_label.pack()

        self.deduct_button = tk.Button(root, text="Descontar 1 crédito", command=self.deduct_credit, state=tk.DISABLED)
        self.deduct_button.pack(pady=10)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        self.credits = db.authenticate(username, password)
        if self.credits is not None:
            self.logged_user = username
            self.credit_label.config(text=f"Créditos: {self.credits}")
            self.deduct_button.config(state=tk.NORMAL)
            messagebox.showinfo("Éxito", "Inicio de sesión correcto")
        else:
            self.credit_label.config(text="")
            self.deduct_button.config(state=tk.DISABLED)
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def register_user(self):
        username = simpledialog.askstring("Nuevo usuario", "Nombre de usuario:")
        password = simpledialog.askstring("Contraseña", "Contraseña:", show="*")
        credits = simpledialog.askinteger("Créditos", "Cantidad de créditos:", minvalue=1)

        if username and password and credits is not None:
            success = db.add_user(username, password, credits)
            if success:
                messagebox.showinfo("Usuario creado", "✅ Usuario registrado con éxito")
            else:
                messagebox.showerror("Error", "❌ Ya existe un usuario con ese nombre")
        else:
            messagebox.showwarning("Campos vacíos", "Por favor completa todos los campos")

    def deduct_credit(self):
        if db.deduct_credits(self.logged_user, 1):
            self.credits -= 1
            self.credit_label.config(text=f"Créditos: {self.credits}")
            messagebox.showinfo("OK", "Crédito descontado")
        else:
            messagebox.showwarning("Sin créditos", "No tienes créditos disponibles")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
