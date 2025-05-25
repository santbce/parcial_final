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


