import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

def calcular_parametros(tipo_suelo, zona_sismica, region):
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

def espectro_diseno(T, Z, Fa, Fd, Fs, eta, R, I, phi_P, phi_E, r=1):
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
            Sa[i] = Sa[i-1]  # Mantener el valor constante después de TL

        Se[i] = Sa[i]
        Si[i] = (I * Sa[i]) / (R * phi_P * phi_E)  # Corrección del espectro inelástico

    return Sa, Se, Si, T0, Tc, TL

def graficar_espectro(tipo_suelo, zona_sismica, region, R, I, phi_P, phi_E):
    parametros, eta, Z = calcular_parametros(tipo_suelo, zona_sismica, region)

    T = np.linspace(0.01, 4, 500)
    Sa, Se, Si, T0, Tc, TL = espectro_diseno(T, Z, **parametros, eta=eta, R=R, I=I, phi_P=phi_P, phi_E=phi_E)

    plt.figure(figsize=(10, 6))
    plt.plot(T, Sa, label='Espectro de Diseño', color='k', linewidth=2)
    plt.plot(T, Se, label='Espectro Elástico', color='black', linestyle='-', linewidth=1.5)
    plt.plot(T, Si, label='Espectro Inelástico', color='gray', linestyle='-.', linewidth=1.5)

    plt.axvline(x=T0, color='r', linestyle=':', linewidth=1.2, label='$T_0$')
    plt.axvline(x=Tc, color='g', linestyle=':', linewidth=1.2, label='$T_c$')
    plt.axvline(x=TL, color='b', linestyle=':', linewidth=1.2, label='$T_L$')

    plt.title('Espectro de Diseño Sísmico')
    plt.xlabel('Periodo (s)')
    plt.ylabel('Sa (g)')
    plt.xlim(0, 4)
    plt.ylim(0, max(Sa) + 0.1)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.show()

# Interfaz gráfica con Tkinter
def iniciar_interfaz():
    root = tk.Tk()
    root.title("Generador de Espectro Sísmico")

    ttk.Label(root, text="Seleccione el tipo de suelo:").grid(column=0, row=0)
    suelo_var = ttk.Combobox(root, values=['A', 'B', 'C', 'D', 'E'])
    suelo_var.grid(column=1, row=0)

    ttk.Label(root, text="Seleccione la zona sísmica:").grid(column=0, row=1)
    sismica_var = ttk.Combobox(root, values=['I', 'II', 'III', 'IV', 'V', 'VI'])
    sismica_var.grid(column=1, row=1)

    ttk.Label(root, text="Seleccione la región:").grid(column=0, row=2)
    region_var = ttk.Combobox(root, values=['Costa', 'Sierra', 'Oriente'])
    region_var.grid(column=1, row=2)

    def ejecutar_grafico():
        tipo_suelo = suelo_var.get()
        zona_sismica = sismica_var.get()
        region = region_var.get()
        R, I, phi_P, phi_E = 8, 1.5, 0.9, 0.9  # Valores por defecto
        if tipo_suelo and zona_sismica and region:
            graficar_espectro(tipo_suelo, zona_sismica, region, R, I, phi_P, phi_E)

    ttk.Button(root, text="Generar Espectro", command=ejecutar_grafico).grid(column=0, row=3, columnspan=2)

    root.mainloop()

# Iniciar la interfaz
tk._default_root = None  # Corregir errores con Tkinter en ciertos entornos
iniciar_interfaz()