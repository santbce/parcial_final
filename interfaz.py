import tkinter as tk
from tkinter import ttk, messagebox
import gestion 


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class CompetenciaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Rendimiento Deportivo")
        self.root.geometry("700x600") 

        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        
        reg_frame = ttk.LabelFrame(main_frame, text="1. Registrar Participante", padding="10")
        reg_frame.pack(fill=tk.X, pady=10)

        ttk.Label(reg_frame, text="Nombre del Participante:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.nombre_participante_entry = ttk.Entry(reg_frame, width=30)
        self.nombre_participante_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)

        self.puntaje_entries = {}
        row_num = 1
        for key, nombre_prueba in gestion.PRUEBAS.items():
            ttk.Label(reg_frame, text=f"Puntaje {nombre_prueba} (0-100):").grid(row=row_num, column=0, padx=5, pady=5, sticky=tk.W)
            entry = ttk.Entry(reg_frame, width=10)
            entry.grid(row=row_num, column=1, padx=5, pady=5, sticky=tk.W)
            self.puntaje_entries[key] = entry
            row_num += 1
        
        reg_button = ttk.Button(reg_frame, text="Registrar Participante", command=self.registrar_participante_gui)
        reg_button.grid(row=row_num, column=0, columnspan=2, pady=10)

        
        report_gen_frame = ttk.LabelFrame(main_frame, text="2. Mostrar Reporte General", padding="10")
        report_gen_frame.pack(fill=tk.X, pady=10)
        
        report_gen_button = ttk.Button(report_gen_frame, text="Ver Reporte General", command=self.mostrar_reporte_general_gui)
        report_gen_button.pack(pady=5)

        
        report_ind_frame = ttk.LabelFrame(main_frame, text="3. Mostrar Reporte Individual", padding="10")
        report_ind_frame.pack(fill=tk.X, pady=10)

        ttk.Label(report_ind_frame, text="Nombre del Participante:").pack(side=tk.LEFT, padx=5)
        self.participante_reporte_entry = ttk.Entry(report_ind_frame, width=25)
        self.participante_reporte_entry.pack(side=tk.LEFT, padx=5)
        report_ind_button = ttk.Button(report_ind_frame, text="Ver Reporte Individual", command=self.mostrar_reporte_individual_gui)
        report_ind_button.pack(side=tk.LEFT, padx=5)

        
        exit_button = ttk.Button(main_frame, text="4. Salir", command=self.root.quit)
        exit_button.pack(pady=20)

    def registrar_participante_gui(self):
        nombre_participante = self.nombre_participante_entry.get()
        if not nombre_participante.strip():
            messagebox.showerror("Error", "El nombre del participante no puede estar vacío.")
            return

        resultados_pruebas = {}
        try:
            for key, entry_widget in self.puntaje_entries.items():
                puntaje_str = entry_widget.get()
                if not puntaje_str: 
                    messagebox.showerror("Error de Entrada", f"El puntaje para {gestion.PRUEBAS[key]} no puede estar vacío.")
                    return
                
                puntaje = int(puntaje_str)
                if not (0 <= puntaje <= 100):
                    messagebox.showerror("Error de Validación", 
                                         f"El puntaje para {gestion.PRUEBAS[key]} debe estar entre 0 y 100.")
                    return
                resultados_pruebas[key] = puntaje
        except ValueError:
            messagebox.showerror("Error de Entrada", "Los puntajes deben ser números enteros.")
            return

        registro = gestion.registrar_participante(nombre_participante, resultados_pruebas)

        if registro:
            messagebox.showinfo("Registro Exitoso", 
                                f"Participante '{nombre_participante}' registrado.\n"
                                f"Puntaje Final: {registro['puntaje_final']}\n"
                                f"Estado: {registro['estado']}")
            self.nombre_participante_entry.delete(0, tk.END)
            for entry_widget in self.puntaje_entries.values():
                entry_widget.delete(0, tk.END)
        else:
            messagebox.showerror("Error de Registro", "No se pudo registrar al participante. Verifique los datos.")

        


        

        


