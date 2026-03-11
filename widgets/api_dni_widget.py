# widgets/api_dni_widget.py
import customtkinter as ctk
from tkinter import messagebox
import requests
import threading
import os
from dotenv import load_dotenv

# Cargamos las variables ocultas del archivo .env al sistema
load_dotenv()

class DniApiEntry(ctk.CTkFrame):
    """Input de DNI con botón para buscar en APIPeru (Seguro)"""
    def __init__(self, parent, target_var, width=280, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.target_var = target_var 
        
        # --- SEGURIDAD: Leer el token desde el entorno ---
        self.api_token = os.getenv("API_PERU_TOKEN")
        
        self.dni_var = ctk.StringVar()
        
        self.entry = ctk.CTkEntry(
            self, textvariable=self.dni_var, width=width - 40, height=24, 
            font=("Segoe UI", 11), placeholder_text="DNI"
        )
        self.entry.pack(side="left", padx=(0, 2))
        
        self.btn = ctk.CTkButton(
            self, text="🔍", width=32, height=24, 
            font=("Segoe UI", 11),
            command=self.buscar_dni, fg_color=("#3498db", "#2980b9"),
            corner_radius=4
        )
        self.btn.pack(side="left")

        self.dni_var.trace_add("write", self._validate_dni)

    def _validate_dni(self, *args):
        value = self.dni_var.get()
        if not value.isdigit():
            self.dni_var.set(''.join(filter(str.isdigit, value)))
        if len(self.dni_var.get()) > 8:
            self.dni_var.set(self.dni_var.get()[:8])

    def buscar_dni(self):
        dni = self.dni_var.get().strip()
        if len(dni) != 8:
            messagebox.showwarning("Aviso", "Ingrese un DNI de 8 dígitos")
            return
            
        # Verificar que el token exista antes de intentar conectarse
        if not self.api_token:
            messagebox.showerror("Error de Configuración", "No se encontró el token de API en el archivo .env")
            return
            
        self.btn.configure(text="...", state="disabled")
        threading.Thread(target=self._hacer_peticion, args=(dni,)).start()
        
    def _hacer_peticion(self, dni):
        try:
            url = "https://apiperu.dev/api/dni"
            headers = {'Authorization': f'Bearer {self.api_token}', 'Content-Type': 'application/json'}
            response = requests.post(url, headers=headers, json={"dni": dni}, timeout=10)
            res = response.json()
            
            if res.get("success"):
                data = res["data"]
                
                nombres = data.get("nombres", "").strip()
                paterno = data.get("apellido_paterno", "").strip()
                materno = data.get("apellido_materno", "").strip()
                
                nombre_final = f"{nombres} {paterno} {materno}".strip()
                
                if not nombres and "nombre_completo" in data:
                    partes = data["nombre_completo"].split(",")
                    if len(partes) == 2:
                        nombre_final = f"{partes[1].strip()} {partes[0].strip()}"

                self.after(0, lambda: self.target_var.set(nombre_final))
            else:
                self.after(0, lambda: messagebox.showinfo("API", "DNI no encontrado, ingrese manualmente."))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror("Error Red", "No hay conexión a la API."))
        finally:
            self.after(0, lambda: self.btn.configure(text="🔍", state="normal"))
            
    def get(self): return self.dni_var.get()
    def set(self, val): self.dni_var.set(val)
    def clear(self): self.dni_var.set("")