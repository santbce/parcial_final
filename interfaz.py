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


    def mostrar_reporte_general_gui(self):
        if not gestion.datos_participantes:
            messagebox.showinfo("Reporte General", "No hay participantes registrados.")
            return

        report_window = tk.Toplevel(self.root)
        report_window.title("Reporte General de Rendimiento")
        report_window.geometry("800x700") 

        
        text_frame = ttk.Frame(report_window)
        text_frame.pack(pady=10, padx=10, fill=tk.X)

        text_area = tk.Text(text_frame, wrap=tk.WORD, height=15, width=90)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(text_frame, command=text_area.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_area.config(yscrollcommand=scrollbar.set)

        report_str = "Reporte General de Rendimiento\n\n"
        for item in gestion.obtener_reporte_general_data():
            report_str += f"Participante: {item['nombre']}, Puntaje Final: {item['puntaje_final']}, Estado: {item['estado']}\n"
        
        report_str += f"\Estadísticas del Grupo\n"
        report_str += f"Puntaje Promedio del Grupo: {gestion.calcular_puntaje_promedio_grupo()}\n"

        pd_data = []
        for reg in gestion.datos_participantes:
            row = {
                "nombre": reg["nombre"],
                "puntaje_final": reg["puntaje_final"],
                "estado": reg["estado"]
            }
            for prueba_key, detalles in reg["detalle_pruebas"].items():
                row[f"{prueba_key}_puntaje"] = detalles["puntaje"]
            pd_data.append(row)
        
        df = pd.DataFrame(pd_data)

        if not df.empty:
            report_str += "\nEstadísticas Descriptivas (Puntajes por Prueba y Final)\n"
            puntaje_cols = [col for col in df.columns if '_puntaje' in col or col == 'puntaje_final']
            if puntaje_cols:
                report_str += df[puntaje_cols].describe().to_string()
            else:
                report_str += "No hay suficientes datos de puntajes para estadísticas descriptivas.\n"
            report_str += "\n\n"

            report_str += "--- Matriz de Correlación (Puntajes por Prueba) ---\n"
            score_cols_for_corr = [col for col in df.columns if '_puntaje' in col]
            if len(score_cols_for_corr) > 1:
                report_str += df[score_cols_for_corr].corr().to_string()
            else:
                report_str += "Se necesitan al menos dos pruebas con puntajes para calcular la correlación.\n"
            report_str += "\n"

        text_area.insert(tk.END, report_str)
        text_area.config(state=tk.DISABLED)

        
        chart_frame = ttk.Frame(report_window)
        chart_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        conteo_clasificados = gestion.contar_clasificados()
        labels = conteo_clasificados.keys()
        sizes = conteo_clasificados.values()
        
        if sum(sizes) > 0: 
            fig = Figure(figsize=(5, 4), dpi=100)
            ax = fig.add_subplot(111)
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            ax.axis('equal')  
            ax.set_title('Distribución de Clasificación')

            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            canvas.draw()
        else:
            ttk.Label(chart_frame, text="No hay datos suficientes para el gráfico de torta.").pack()


    def mostrar_reporte_individual_gui(self):
        nombre_participante = self.participante_reporte_entry.get()
        if not nombre_participante.strip():
            messagebox.showerror("Error", "Ingrese el nombre del participante para el reporte.")
            return

        registros_participante = gestion.obtener_datos_participante(nombre_participante)

        if not registros_participante:
            messagebox.showinfo("Reporte Individual", f"No se encontraron registros para '{nombre_participante}'.")
            return

        
        registro_actual = registros_participante[-1] 

        report_window = tk.Toplevel(self.root)
        report_window.title(f"Reporte Individual - {nombre_participante}")
        report_window.geometry("900x750")