import tkinter as tk
from tkinter import ttk
from .constants import (ZONA_SISMICA_OPTIONS, REGION_OPTIONS, TIPO_SUELO_OPTIONS,
                      FACTOR_R_OPTIONS, FACTOR_I_OPTIONS)

def create_input_panel(panel, variables, generar_callback, exportar_callback, imagen_callback, pdf_callback):
    """
    Crea los componentes de la interfaz de usuario en el panel izquierdo
    
    Args:
        panel: Panel donde se crearán los componentes
        variables: Diccionario con todas las variables tkinter
        generar_callback: Función a llamar al generar espectro
        exportar_callback: Función a llamar al exportar a Excel
        imagen_callback: Función a llamar al guardar imagen
        pdf_callback: Función a llamar al generar PDF
    """
    # Título
    ttk.Label(panel, text="Generador de Espectro de Diseño Sísmico - NEC", 
              font=('Arial', 12, 'bold')).grid(column=0, row=0, columnspan=2, sticky=tk.W, pady=(0, 20))
    
    # Zona sísmica
    ttk.Label(panel, text="Zona Sísmica (Z):", 
              font=('Arial', 10, 'bold')).grid(column=0, row=1, sticky=tk.W, pady=5)
    zona_sismica_combo = ttk.Combobox(panel, textvariable=variables['zona_sismica_var'], width=30)
    zona_sismica_combo['values'] = ZONA_SISMICA_OPTIONS
    zona_sismica_combo.grid(column=1, row=1, sticky=tk.W, pady=5)
    
    # Región
    ttk.Label(panel, text="Región:", 
              font=('Arial', 10, 'bold')).grid(column=0, row=2, sticky=tk.W, pady=5)
    region_combo = ttk.Combobox(panel, textvariable=variables['region_var'], width=30)
    region_combo['values'] = REGION_OPTIONS
    region_combo.grid(column=1, row=2, sticky=tk.W, pady=5)
    
    # Tipo de suelo
    ttk.Label(panel, text="Tipo de Suelo:", 
              font=('Arial', 10, 'bold')).grid(column=0, row=3, sticky=tk.W, pady=5)
    tipo_suelo_combo = ttk.Combobox(panel, textvariable=variables['tipo_suelo_var'], width=30)
    tipo_suelo_combo['values'] = TIPO_SUELO_OPTIONS
    tipo_suelo_combo.grid(column=1, row=3, sticky=tk.W, pady=5)
    
    # Factor R
    ttk.Label(panel, text="Factor R:", 
              font=('Arial', 10, 'bold')).grid(column=0, row=4, sticky=tk.W, pady=5)
    r_combo = ttk.Combobox(panel, textvariable=variables['r_var'], width=30)
    r_combo['values'] = FACTOR_R_OPTIONS
    r_combo.grid(column=1, row=4, sticky=tk.W, pady=5)
    
    # Factor I
    ttk.Label(panel, text="Factor I:", 
              font=('Arial', 10, 'bold')).grid(column=0, row=5, sticky=tk.W, pady=5)
    i_combo = ttk.Combobox(panel, textvariable=variables['i_var'], width=30)
    i_combo['values'] = FACTOR_I_OPTIONS
    i_combo.grid(column=1, row=5, sticky=tk.W, pady=5)
    
    # Factor phi_P
    ttk.Label(panel, text="Factor φP:", 
              font=('Arial', 10, 'bold')).grid(column=0, row=6, sticky=tk.W, pady=5)
    ttk.Entry(panel, textvariable=variables['phi_p_var'], width=10).grid(column=1, row=6, sticky=tk.W, pady=5)
    ttk.Label(panel, text="(Factor de configuración en planta)").grid(column=1, row=6, sticky=tk.E, pady=5)
    
    # Factor phi_E
    ttk.Label(panel, text="Factor φE:", 
              font=('Arial', 10, 'bold')).grid(column=0, row=7, sticky=tk.W, pady=5)
    ttk.Entry(panel, textvariable=variables['phi_e_var'], width=10).grid(column=1, row=7, sticky=tk.W, pady=5)
    ttk.Label(panel, text="(Factor de configuración en elevación)").grid(column=1, row=7, sticky=tk.E, pady=5)
    
    # Botones
    botones_frame = ttk.Frame(panel)
    botones_frame.grid(column=0, row=8, columnspan=2, pady=20)
    
    ttk.Button(botones_frame, text="Generar Espectro", command=generar_callback).grid(column=0, row=0, padx=5)
    ttk.Button(botones_frame, text="Exportar a Excel", command=exportar_callback).grid(column=1, row=0, padx=5)
    ttk.Button(botones_frame, text="Guardar Imagen", command=imagen_callback).grid(column=2, row=0, padx=5)
    ttk.Button(botones_frame, text="Generar Reporte PDF", command=pdf_callback).grid(column=3, row=0, padx=5)
    
    # Información adicional
    info_frame = ttk.LabelFrame(panel, text="Información", padding="10 10 10 10")
    info_frame.grid(column=0, row=9, columnspan=2, sticky=(tk.W, tk.E), pady=10)
    
    info_text = "Este programa genera el espectro de diseño sísmico según la NEC.\n"
    info_text += "Los valores de R deben seleccionarse según el sistema estructural.\n"
    info_text += "Los valores de I deben seleccionarse según el tipo de uso o importancia de la estructura."
    
    ttk.Label(info_frame, text=info_text, wraplength=380).grid(column=0, row=0)