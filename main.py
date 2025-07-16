import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from database_sqlite import Database
from web_automation import WebBot
import threading
# import pandas as pd  # Removido para ejecutable
import csv
import os
import time

class BotApp:
    def __init__(self):
        self.db = Database()
        self.current_user = None
        self.tarjetas = []
        self.resultados = []
        self.setup_gui()
    
    def setup_gui(self):
        self.root = tk.Tk()
        self.root.title("Bot Automatización de Tarjetas")
        self.root.geometry("600x500")
        
        # Login Frame
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=50)
        
        tk.Label(self.login_frame, text="INICIAR SESIÓN", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)
        
        tk.Label(self.login_frame, text="Usuario:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.username_entry = tk.Entry(self.login_frame, width=20)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)
        
        tk.Label(self.login_frame, text="Contraseña:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.password_entry = tk.Entry(self.login_frame, show="*", width=20)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Button(self.login_frame, text="Iniciar Sesión", command=self.login, bg="#4CAF50", fg="white", width=15).grid(row=3, column=0, columnspan=2, pady=15)
        
        # Main Frame (oculto inicialmente)
        self.main_frame = tk.Frame(self.root)
        
        # Título y créditos
        title_frame = tk.Frame(self.main_frame)
        title_frame.pack(pady=10)
        
        tk.Label(title_frame, text="VERIFICADOR DE TARJETAS", font=("Arial", 16, "bold")).pack()
        
        # Frame para subir archivo
        upload_frame = tk.LabelFrame(self.main_frame, text="1. Subir Archivo", font=("Arial", 12, "bold"))
        upload_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Button(upload_frame, text="Seleccionar CSV", command=self.upload_file, bg="#2196F3", fg="white", width=20).pack(pady=10)
        self.file_label = tk.Label(upload_frame, text="Ningún archivo seleccionado", fg="gray")
        self.file_label.pack()
        
        # Frame para verificar
        check_frame = tk.LabelFrame(self.main_frame, text="2. Verificar Tarjetas", font=("Arial", 12, "bold"))
        check_frame.pack(pady=10, padx=20, fill="x")
        
        self.check_button = tk.Button(check_frame, text="Checkear Tarjetas", command=self.check_cards, bg="#FF9800", fg="white", width=20, state="disabled")
        self.check_button.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(check_frame, mode='determinate')
        self.progress.pack(pady=5, padx=20, fill="x")
        
        self.status_label = tk.Label(check_frame, text="", fg="blue")
        self.status_label.pack()
        
        # Frame para resultados
        results_frame = tk.LabelFrame(self.main_frame, text="3. Resultados", font=("Arial", 12, "bold"))
        results_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Treeview para mostrar resultados
        columns = ('Número', 'Mes', 'Año', 'CVV', 'Estado')
        self.tree = ttk.Treeview(results_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar.pack(side="right", fill="y")
        
        # Botones finales
        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="Generar CSV Live", command=self.generate_csv, bg="#4CAF50", fg="white", width=15).pack(side="left", padx=5)
        tk.Button(button_frame, text="Cerrar Sesión", command=self.logout, bg="#f44336", fg="white", width=15).pack(side="left", padx=5)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not username or not password:
            messagebox.showerror("Error", "Ingrese usuario y contraseña")
            return
        
        if self.db.authenticate(username, password) is not None:
            self.current_user = username
            self.show_main_interface()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")
    
    def show_main_interface(self):
        self.login_frame.pack_forget()
        self.main_frame.pack(pady=10, fill="both", expand=True)
    
    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    with open(file_path, 'r') as f:
                        reader = csv.reader(f, delimiter='|')
                        self.tarjetas = [row for row in reader if len(row) == 4]
                else:
                    # Para otros archivos, intentar leer como CSV
                    with open(file_path, 'r') as f:
                        reader = csv.reader(f, delimiter='|')
                        self.tarjetas = [row for row in reader if len(row) == 4]
                
                self.file_label.config(text=f"Archivo cargado: {len(self.tarjetas)} tarjetas", fg="green")
                self.check_button.config(state="normal")
                
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar archivo: {e}")
    
    def check_cards(self):
        if not self.tarjetas:
            messagebox.showerror("Error", "No hay tarjetas para verificar")
            return
        
        # Ejecutar verificación en hilo separado
        threading.Thread(target=self.execute_verification, daemon=True).start()
    
    def execute_verification(self):
        bot = None
        try:
            
            # Configurar progress bar
            total_cards = len(self.tarjetas)
            self.root.after(0, lambda: self.progress.config(maximum=total_cards))
            self.root.after(0, lambda: self.status_label.config(text="Iniciando navegador...", fg="blue"))
            
            # Inicializar bot
            bot = WebBot(browser_type="chrome", headless=False)
            
            if bot.start_browser():
                self.root.after(0, lambda: self.status_label.config(text="Navegador iniciado correctamente", fg="green"))
                self.resultados = []
                
                for i, tarjeta in enumerate(self.tarjetas):
                    try:
                        # Actualizar status
                        self.root.after(0, lambda i=i: self.status_label.config(text=f"Verificando tarjeta {i+1}/{total_cards}: {tarjeta[0][:4]}****", fg="blue"))
                        self.root.after(0, lambda i=i: self.progress.config(value=i+1))
                        
                        print(f"\n[INFO] Procesando tarjeta {i+1}: {tarjeta}")
                        
                        # Verificar tarjeta
                        success = bot.donar_una_vez(*tarjeta)
                        estado = "LIVE" if success else "DEATH"
                        
                        # Reproducir sonido si es LIVE
                        if success:
                            try:
                                import winsound
                                winsound.Beep(1500, 1000)  # Sonido más largo para LIVE
                            except:
                                pass
                        
                        print(f"[RESULT] Resultado: {estado}")
                        
                        # Agregar resultado
                        resultado = list(tarjeta) + [estado]
                        self.resultados.append(resultado)
                        
                        # Actualizar tabla
                        self.root.after(0, lambda r=resultado: self.add_result_to_tree(r))
                        
                        # Pausa entre tarjetas
                        time.sleep(2)
                        
                    except Exception as card_error:
                        print(f"[ERROR] Error procesando tarjeta {i+1}: {card_error}")
                        resultado = list(tarjeta) + ["ERROR"]
                        self.resultados.append(resultado)
                        self.root.after(0, lambda r=resultado: self.add_result_to_tree(r))
                
                self.root.after(0, lambda: self.status_label.config(text="Verificación completada", fg="green"))
            else:
                self.root.after(0, lambda: messagebox.showerror("Error", "No se pudo iniciar el navegador"))
                
        except Exception as e:
            print(f"[ERROR] Error general: {e}")
            import traceback
            traceback.print_exc()
            self.root.after(0, lambda: messagebox.showerror("Error", f"Error inesperado: {e}"))
        finally:
            # Asegurar que el navegador se cierre correctamente
            if bot and bot.driver:
                try:
                    bot.close_browser()
                    print("[INFO] Navegador cerrado correctamente")
                except:
                    print("[WARN] Error cerrando navegador")
    
    def add_result_to_tree(self, resultado):
        # Configurar colores según el estado
        if resultado[4] == "LIVE":
            self.tree.insert('', 'end', values=resultado, tags=('live',))
        elif resultado[4] == "ERROR":
            self.tree.insert('', 'end', values=resultado, tags=('error',))
        else:
            self.tree.insert('', 'end', values=resultado, tags=('death',))
        
        # Configurar colores
        self.tree.tag_configure('live', background='#d4edda', foreground='#155724')
        self.tree.tag_configure('death', background='#f8d7da', foreground='#721c24')
        self.tree.tag_configure('error', background='#fff3cd', foreground='#856404')
    
    def generate_csv(self):
        if not self.resultados:
            messagebox.showwarning("Advertencia", "No hay resultados para generar")
            return
        
        # Filtrar solo las tarjetas LIVE
        live_cards = [r for r in self.resultados if r[4] == "LIVE"]
        
        if not live_cards:
            messagebox.showwarning("Advertencia", "No hay tarjetas LIVE para generar")
            return
        
        # Generar CSV
        filename = "tarjetas_live.csv"
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f, delimiter='|')
            for card in live_cards:
                writer.writerow(card[:4])  # Solo número, mes, año, cvv
        
        messagebox.showinfo("Éxito", f"CSV generado: {filename} con {len(live_cards)} tarjetas LIVE")
    
    def logout(self):
        self.current_user = None
        self.tarjetas = []
        self.resultados = []
        
        # Limpiar interfaz
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        self.file_label.config(text="Ningún archivo seleccionado", fg="gray")
        self.check_button.config(state="disabled")
        self.progress.config(value=0)
        self.status_label.config(text="")
        
        # Mostrar login
        self.main_frame.pack_forget()
        self.login_frame.pack(pady=50)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
    
    def run(self):
        self.root.mainloop()

def create_test_user():
    """Función para crear usuario de prueba"""
    db = Database()
    db.add_user("admin", "123456", 999999)
    print("Usuario de prueba creado: admin/123456 con créditos infinitos")

if __name__ == "__main__":
    create_test_user()
    app = BotApp()
    app.run()