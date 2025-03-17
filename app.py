import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from ui_components import create_input_panel
from seismic_calculations import parse_values, calculate_parameters, calculate_spectrum
from export_utilities import export_to_excel, save_image, generate_pdf_report

class EspectroSismicoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Espectro de Diseño Sísmico - NEC")
        self.root.geometry("1000x700")
        
        # Dividir la ventana en dos partes
        self.panel_izquierdo = ttk.Frame(root, padding="10 10 10 10", width=400)
        self.panel_izquierdo.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.panel_derecho = ttk.Frame(root, padding="10 10 10 10")
        self.panel_derecho.grid(column=1, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el panel izquierdo para que mantenga su ancho
        self.panel_izquierdo.grid_propagate(False)
        
        # Variables para almacenar los valores de entrada
        self.variables = {
            'zona_sismica_var': tk.StringVar(),
            'region_var': tk.StringVar(),
            'tipo_suelo_var': tk.StringVar(),
            'r_var': tk.StringVar(),
            'i_var': tk.StringVar(),
            'phi_p_var': tk.DoubleVar(value=0.9),
            'phi_e_var': tk.DoubleVar(value=0.9),
        }
        
        # Datos de espectro calculados
        self.T = None
        self.Sa = None
        self.Se = None
        self.Si = None
        
        # Crear la interfaz
        create_input_panel(self.panel_izquierdo, self.variables, self.generar_espectro, 
                           self.exportar_excel, self.guardar_imagen, self.generar_reporte_pdf)
        
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
        self.set_default_values()
    
    def set_default_values(self):
        # Establecer valores por defecto para los combos
        for combo_name, widget in self.variables.items():
            if combo_name == 'zona_sismica_var':
                widget.set('VI')
            elif combo_name == 'region_var':
                widget.set('Costa (Excepto Esmeralda)')
            elif combo_name == 'tipo_suelo_var':
                widget.set('C')
            elif combo_name == 'r_var':
                widget.set('8.0 - Pórticos especiales sismo resistentes')
            elif combo_name == 'i_var':
                widget.set('1.0 - Edificaciones esenciales')
    
    def generar_espectro(self):
        from tkinter import messagebox
        try:
            # Parsear valores de la interfaz
            zona_sismica, tipo_suelo, region, r_valor, i_valor = parse_values(self.variables)
            phi_p = float(self.variables['phi_p_var'].get())
            phi_e = float(self.variables['phi_e_var'].get())
            
            # Verificar valores válidos
            if r_valor <= 0 or i_valor <= 0 or phi_p <= 0 or phi_e <= 0:
                messagebox.showerror("Error", "Todos los factores deben ser mayores que cero.")
                return
                
            # Calcular parámetros
            parametros, eta, Z = calculate_parameters(tipo_suelo, zona_sismica, region)
            Fa, Fd, Fs, r = parametros['Fa'], parametros['Fd'], parametros['Fs'], parametros['r']
            
            # Generar el espectro
            T, Sa, Se, Si, T0, Tc, TL = calculate_spectrum(Z, Fa, Fd, Fs, eta, r_valor, i_valor, phi_p, phi_e, r)
            
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
        from tkinter import messagebox
        if self.T is None or self.Sa is None:
            messagebox.showerror("Error", "Primero debe generar el espectro.")
            return
        
        # Obtener parámetros para el encabezado del Excel
        zona_sismica, tipo_suelo, region, r_valor, i_valor = parse_values(self.variables)
        phi_p = float(self.variables['phi_p_var'].get())
        phi_e = float(self.variables['phi_e_var'].get())
        
        # Llamar a la función de exportación
        export_to_excel(self.T, self.Sa, self.Se, self.Si, zona_sismica, tipo_suelo, region, 
                       r_valor, i_valor, phi_p, phi_e)
    
    def guardar_imagen(self):
        from tkinter import messagebox
        if self.Sa is None:
            messagebox.showerror("Error", "Primero debe generar el espectro.")
            return
        
        save_image(self.fig)
    
    def generar_reporte_pdf(self):
        from tkinter import messagebox
        if self.T is None or self.Sa is None:
            messagebox.showerror("Error", "Primero debe generar el espectro.")
            return
        
        # Obtener parámetros actuales
        zona_sismica, tipo_suelo, region, r_valor, i_valor = parse_values(self.variables)
        phi_p = float(self.variables['phi_p_var'].get())
        phi_e = float(self.variables['phi_e_var'].get())
        
        generate_pdf_report(self.T, self.Sa, self.Se, self.Si, zona_sismica, tipo_suelo, region,
                           r_valor, i_valor, phi_p, phi_e, self.fig)