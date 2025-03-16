import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import os

class EspectroSismicoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Espectro de Diseño Sísmico - NEC")
        self.root.geometry("1000x700")
        self
        
        # Dividir la ventana en dos partes
        self.panel_izquierdo = ttk.Frame(root, padding="10 10 10 10", width=400)
        self.panel_izquierdo.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.panel_derecho = ttk.Frame(root, padding="10 10 10 10")
        self.panel_derecho.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el panel izquierdo para que mantenga su ancho
        self.panel_izquierdo.grid_propagate(False)
        
        # Variables
        self.zona_sismica_var = tk.StringVar()
        self.region_var = tk.StringVar()
        self.tipo_suelo_var = tk.StringVar()
        self.r_var = tk.StringVar()
        self.i_var = tk.StringVar()
        self.phi_p_var = tk.DoubleVar(value=0.9)
        self.phi_e_var = tk.DoubleVar(value=0.9)
        
        # Datos de espectro calculados
        self.T = None
        self.Sa = None
        self.Se = None
        self.Si = None
        
        # Crear la interfaz
        self.crear_interfaz()
        
        # Configurar el panel para la gráfica
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.panel_derecho)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Añadir barra de herramientas de navegación
        self.toolbar_frame = ttk.Frame(self.panel_derecho)
        self.toolbar_frame.pack(fill=tk.X)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.toolbar_frame)
        
        # Hacer que la ventana sea redimensionable
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Iniciar valores por defecto
        self.zona_sismica_combo.set('III')
        self.region_combo.set('Sierra')
        self.tipo_suelo_combo.set('C')
        self.r_combo.set('8.0 - Pórticos especiales sismo resistentes')
        self.i_combo.set('1.5 - Edificaciones esenciales')
    
    def crear_interfaz(self):
        # Título
        ttk.Label(self.panel_izquierdo, text="Generador de Espectro de Diseño Sísmico - NEC", 
                  font=('Arial', 12, 'bold')).grid(column=0, row=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # Zona sísmica
        ttk.Label(self.panel_izquierdo, text="Zona Sísmica (Z):", 
                  font=('Arial', 10, 'bold')).grid(column=0, row=1, sticky=tk.W, pady=5)
        self.zona_sismica_combo = ttk.Combobox(self.panel_izquierdo, textvariable=self.zona_sismica_var, width=30)
        self.zona_sismica_combo['values'] = ('I (0.15g)', 'II (0.25g)', 'III (0.30g)', 'IV (0.35g)', 'V (0.40g)', 'VI (0.50g)')
        self.zona_sismica_combo.grid(column=1, row=1, sticky=tk.W, pady=5)
        
        # Región
        ttk.Label(self.panel_izquierdo, text="Región:", 
                  font=('Arial', 10, 'bold')).grid(column=0, row=2, sticky=tk.W, pady=5)
        self.region_combo = ttk.Combobox(self.panel_izquierdo, textvariable=self.region_var, width=30)
        self.region_combo['values'] = ('Costa', 'Sierra', 'Oriente')
        self.region_combo.grid(column=1, row=2, sticky=tk.W, pady=5)
        
        # Tipo de suelo
        ttk.Label(self.panel_izquierdo, text="Tipo de Suelo:", 
                  font=('Arial', 10, 'bold')).grid(column=0, row=3, sticky=tk.W, pady=5)
        self.tipo_suelo_combo = ttk.Combobox(self.panel_izquierdo, textvariable=self.tipo_suelo_var, width=30)
        self.tipo_suelo_combo['values'] = ('A - Roca competente', 'B - Roca de rigidez media', 
                                          'C - Suelos muy densos o roca blanda', 
                                          'D - Suelos rígidos', 'E - Suelos blandos')
        self.tipo_suelo_combo.grid(column=1, row=3, sticky=tk.W, pady=5)
        
        # Factor R
        ttk.Label(self.panel_izquierdo, text="Factor R:", 
                  font=('Arial', 10, 'bold')).grid(column=0, row=4, sticky=tk.W, pady=5)
        self.r_combo = ttk.Combobox(self.panel_izquierdo, textvariable=self.r_var, width=30)
        self.r_combo['values'] = (
            '8.0 - Pórticos especiales sismo resistentes',
            '7.0 - Pórticos con vigas banda',
            '6.0 - Pórticos intermedios',
            '5.0 - Muros estructurales dúctiles',
            '4.0 - Pórticos resistentes a momento',
            '3.0 - Mampostería reforzada',
            '2.5 - Estructuras de acero conformado',
            '1.5 - Muros de hormigón sin refuerzo',
            '1.0 - Mampostería sin refuerzo'
        )
        self.r_combo.grid(column=1, row=4, sticky=tk.W, pady=5)
        
        # Factor I
        ttk.Label(self.panel_izquierdo, text="Factor I:", 
                  font=('Arial', 10, 'bold')).grid(column=0, row=5, sticky=tk.W, pady=5)
        self.i_combo = ttk.Combobox(self.panel_izquierdo, textvariable=self.i_var, width=30)
        self.i_combo['values'] = (
            '1.0 - Estructuras comunes',
            '1.3 - Estructuras de ocupación especial',
            '1.5 - Edificaciones esenciales'
        )
        self.i_combo.grid(column=1, row=5, sticky=tk.W, pady=5)
        
        # Factor phi_P
        ttk.Label(self.panel_izquierdo, text="Factor φP:", 
                  font=('Arial', 10, 'bold')).grid(column=0, row=6, sticky=tk.W, pady=5)
        ttk.Entry(self.panel_izquierdo, textvariable=self.phi_p_var, width=10).grid(column=1, row=6, sticky=tk.W, pady=5)
        ttk.Label(self.panel_izquierdo, text="(Factor de configuración en planta)").grid(column=1, row=6, sticky=tk.E, pady=5)
        
        # Factor phi_E
        ttk.Label(self.panel_izquierdo, text="Factor φE:", 
                  font=('Arial', 10, 'bold')).grid(column=0, row=7, sticky=tk.W, pady=5)
        ttk.Entry(self.panel_izquierdo, textvariable=self.phi_e_var, width=10).grid(column=1, row=7, sticky=tk.W, pady=5)
        ttk.Label(self.panel_izquierdo, text="(Factor de configuración en elevación)").grid(column=1, row=7, sticky=tk.E, pady=5)
        
        # Botones
        botones_frame = ttk.Frame(self.panel_izquierdo)
        botones_frame.grid(column=0, row=8, columnspan=2, pady=20)
        
        ttk.Button(botones_frame, text="Generar Espectro", command=self.generar_espectro).grid(column=0, row=0, padx=5)
        ttk.Button(botones_frame, text="Exportar a Excel", command=self.exportar_excel).grid(column=1, row=0, padx=5)
        ttk.Button(botones_frame, text="Guardar Imagen", command=self.guardar_imagen).grid(column=2, row=0, padx=5)
        
        # Información adicional
        info_frame = ttk.LabelFrame(self.panel_izquierdo, text="Información", padding="10 10 10 10")
        info_frame.grid(column=0, row=9, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        info_text = "Este programa genera el espectro de diseño sísmico según la NEC.\n"
        info_text += "Los valores de R deben seleccionarse según el sistema estructural.\n"
        info_text += "Los valores de I deben seleccionarse según el tipo de uso o importancia de la estructura."
        
        ttk.Label(info_frame, text=info_text, wraplength=380).grid(column=0, row=0)
    
    def parsear_valores(self):
        # Parsear zona sísmica
        zona_text = self.zona_sismica_var.get()
        zona_romana = zona_text.split(' ')[0]
        
        # Parsear tipo de suelo
        tipo_suelo_text = self.tipo_suelo_var.get()
        tipo_suelo = tipo_suelo_text.split(' ')[0]
        
        # Parsear factor R
        r_text = self.r_var.get()
        r_valor = float(r_text.split(' ')[0])
        
        # Parsear factor I
        i_text = self.i_var.get()
        i_valor = float(i_text.split(' ')[0])
        
        return zona_romana, tipo_suelo, self.region_var.get(), r_valor, i_valor
    
    def calcular_parametros(self, tipo_suelo, zona_sismica, region):
        parametros = {
            'A': {'Fa': 0.9, 'Fd': 0.9, 'Fs': 0.75, 'r': 1},
            'B': {'Fa': 1.0, 'Fd': 1.0, 'Fs': 0.75, 'r': 1},
            'C': {'Fa': 1.4, 'Fd': 1.36, 'Fs': 0.85, 'r': 1},
            'D': {'Fa': 1.6, 'Fd': 1.62, 'Fs': 1.02, 'r': 1},
            'E': {'Fa': 1.8, 'Fd': 2.1, 'Fs': 1.75, 'r': 1.5}
        }

        eta_zona = {
            'Costa': 1.8,
            'Sierra': 2.48,
            'Oriente': 2.60
        }

        Z_valores = {
            'I': 0.15, 'II': 0.25, 'III': 0.30,
            'IV': 0.35, 'V': 0.40, 'VI': 0.50
        }

        return parametros[tipo_suelo], eta_zona[region], Z_valores[zona_sismica]
    
    def espectro_diseno(self, T, Z, Fa, Fd, Fs, eta, R, I, phi_P, phi_E, r=1):
        T0 = 0.1 * Fs * Fd / Fa
        Tc = 0.55 * Fs * Fd / Fa
        TL = 2.4 * Fd

        Sa = np.zeros_like(T)
        Se = np.zeros_like(T)
        Si = np.zeros_like(T)

        for i, t in enumerate(T):
            if t <= T0:
                Sa[i] = Z * Fa * (1 + (eta - 1) * t / T0)
            elif T0 < t <= Tc:
                Sa[i] = eta * Z * Fa
            elif Tc < t <= TL:
                Sa[i] = eta * Z * Fa * (Tc / t)**r
            else:
                Sa[i] = eta * Z * Fa * (Tc / t)**r 

            Se[i] = Sa[i]
            Si[i] = (I * Sa[i]) / (R * phi_P * phi_E)

        return Sa, Se, Si, T0, Tc, TL
    
    def generar_espectro(self):
        try:
            # Parsear valores de la interfaz
            zona_sismica, tipo_suelo, region, r_valor, i_valor = self.parsear_valores()
            phi_p = float(self.phi_p_var.get())
            phi_e = float(self.phi_e_var.get())
            
            # Verificar valores válidos
            if r_valor <= 0 or i_valor <= 0 or phi_p <= 0 or phi_e <= 0:
                messagebox.showerror("Error", "Todos los factores deben ser mayores que cero.")
                return
                
            # Calcular parámetros
                        # Calcular parámetros
            parametros, eta, Z = self.calcular_parametros(tipo_suelo, zona_sismica, region)
            Fa, Fd, Fs, r = parametros['Fa'], parametros['Fd'], parametros['Fs'], parametros['r']
            
            # Generar el espectro
            T = np.linspace(0, TL+0.1, 1000)  # Rango de periodos de 0 a 4 segundos
            Sa, Se, Si, T0, Tc, TL = self.espectro_diseno(T, Z, Fa, Fd, Fs, eta, r_valor, i_valor, phi_p, phi_e, r)
            
            # Guardar datos calculados
            self.T = T
            self.Sa = Sa
            self.Se = Se
            self.Si = Si
            
            # Actualizar la gráfica
            self.actualizar_grafica(T, Sa, Se, Si, T0, Tc, TL, Z, Fa, Fd, Fs, eta, r_valor, i_valor, phi_p, phi_e)
            
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", "Espectro generado correctamente.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el espectro: {str(e)}")
    
    def actualizar_grafica(self, T, Sa, Se, Si, T0, Tc, TL, Z, Fa, Fd, Fs, eta, R, I, phi_P, phi_E):
        # Limpiar la gráfica anterior
        self.ax.clear()
        
        # Graficar los espectros
        self.ax.plot(T, Sa, 'b-', label='Sa (Espectro de aceleración)')
        self.ax.plot(T, Si, 'r-', label='Si (Espectro inelástico)')
        
        # Marcar puntos de cambio
        self.ax.axvline(x=T0, color='g', linestyle='--', alpha=0.7, label=f'T0 = {T0:.2f}s')
        self.ax.axvline(x=Tc, color='m', linestyle='--', alpha=0.7, label=f'Tc = {Tc:.2f}s')
        self.ax.axvline(x=TL, color='c', linestyle='--', alpha=0.7, label=f'TL = {TL:.2f}s')
        
        # Añadir título y etiquetas
        self.ax.set_xlim(0, max(5, TL + 0.1))
        self.ax.set_title('Espectro de Diseño Sísmico NEC')
        self.ax.set_xlabel('Período T (s)')
        self.ax.set_ylabel('Aceleración Sa (g)')
        self.ax.grid(True)
        self.ax.legend()
        
        # Añadir información de parámetros
        info_text = (f"Z = {Z:.2f}g, R = {R}, I = {I}\n"
                    f"Fa = {Fa:.2f}, Fd = {Fd:.2f}, Fs = {Fs:.2f}, η = {eta:.2f}\n"
                    f"φP = {phi_P:.2f}, φE = {phi_E:.2f}")
        self.ax.text(0.02, 0.02, info_text, transform=self.ax.transAxes, 
                    bbox=dict(facecolor='white', alpha=0.8))
        
        # Actualizar el lienzo
        self.canvas.draw()
    
    def exportar_excel(self):
        if self.T is None or self.Sa is None:
            messagebox.showerror("Error", "Primero debe generar el espectro.")
            return
        
        try:
            # Crear un DataFrame con los datos
            df = pd.DataFrame({
                'Período (s)': self.T,
                'Sa (g)': self.Sa,
                'Se (g)': self.Se,
                'Si (g)': self.Si
            })
            
            # Solicitar al usuario la ubicación para guardar el archivo
            file_path = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                title="Guardar espectro como Excel"
            )
            
            if not file_path:
                return  # El usuario canceló la operación
            
            # Guardar el DataFrame como Excel
            df.to_excel(file_path, index=False)
            
            messagebox.showinfo("Éxito", f"Datos exportados correctamente a {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar los datos: {str(e)}")
    
    def guardar_imagen(self):
        if self.Sa is None:
            messagebox.showerror("Error", "Primero debe generar el espectro.")
            return
        
        try:
            # Solicitar al usuario la ubicación para guardar la imagen
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("PDF files", "*.pdf"), ("All files", "*.*")],
                title="Guardar gráfica como imagen"
            )
            
            if not file_path:
                return  # El usuario canceló la operación
            
            # Guardar la figura
            self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
            
            messagebox.showinfo("Éxito", f"Imagen guardada correctamente como {os.path.basename(file_path)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar la imagen: {str(e)}")


# Función principal para iniciar la aplicación
def main():
    root = tk.Tk()
    app = EspectroSismicoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()