import tkinter as tk
from tkinter import messagebox, simpledialog
from database import Database
from web_automation import WebBot
import threading

class BotApp:
    def __init__(self):
        self.db = Database()
        self.current_user = None
        self.current_credits = 0
        self.setup_gui()
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Bot Automatización")
        self.root.geometry("400x300")
        
        # Login Frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)
        
        tk.Label(self.login_frame, text="Usuario:").grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(self.login_frame, text="Contraseña:").grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Button(self.login_frame, text="Iniciar Sesión", command=self.login).grid(row=2, column=0, columnspan=2, pady=10)
        
        # Main Frame (oculto inicialmente)
        self.main_frame = tk.Frame(self.root)
        
        self.credits_label = tk.Label(self.main_frame, text="Créditos: 0", font=("Arial", 12))
        self.credits_label.pack(pady=10)
        
        tk.Button(self.main_frame, text="Ejecutar Bot", command=self.run_bot, bg="green", fg="white").pack(pady=10)
        tk.Button(self.main_frame, text="Cerrar Sesión", command=self.logout).pack(pady=5)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Ingrese usuario y contraseña")
            return
        
        credits = self.db.authenticate(username, password)
        if credits is not None:
            self.current_user = username
            self.current_credits = credits
            self.show_main_interface()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def show_main_interface(self):
        self.login_frame.pack_forget()
        self.main_frame.pack(pady=20)
        self.update_credits_display()
    
    def update_credits_display(self):
        self.credits_label.config(text=f"Créditos: {self.current_credits}")
    
    def run_bot(self):
        if self.current_credits <= 0:
            messagebox.showerror("Error", "No tienes créditos suficientes")
            return
        
        # Ejecutar bot en hilo separado
        threading.Thread(target=self.execute_bot_task, daemon=True).start()
    
    def execute_bot_task(self):
        try:
            # Descontar crédito
            if not self.db.deduct_credits(self.current_user, 1):
                messagebox.showerror("Error", "No se pudo descontar crédito")
                return
            
            self.current_credits -= 1
            self.root.after(0, self.update_credits_display)
            
            # Ejecutar automatización
            bot = WebBot(headless=False)
            if bot.start_browser():
                # Ejemplo de datos a registrar
                data = {
                    "name": "Usuario Test",
                    "email": "test@example.com",
                    "phone": "123456789"
                }
                
                success = bot.register_data_example(data)
                bot.close_browser()
                
                if success:
                    messagebox.showinfo("Éxito", "Tarea completada correctamente")
                else:
                    messagebox.showerror("Error", "Error ejecutando tarea")
            else:
                messagebox.showerror("Error", "No se pudo iniciar el navegador")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")
    
    def logout(self):
        self.current_user = None
        self.current_credits = 0
        self.main_frame.pack_forget()
        self.login_frame.pack(pady=20)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    def run(self):
        self.root.mainloop()

def create_test_user():
    """Función para crear usuario de prueba"""
    db = Database()
    db.add_user("admin", "123456", 10)
    print("Usuario de prueba creado: admin/123456 con 10 créditos")

if __name__ == "__main__":
    create_test_user()
    app = BotApp()
    app.run()