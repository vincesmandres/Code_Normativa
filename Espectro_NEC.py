import numpy as np
import matplotlib.pyplot as plt

def calcular_parametros(tipo_suelo, zona_sismica):
    # Parámetros según el tipo de suelo y zona sísmica
    parametros = {
        'A': {'Fa': 0.9, 'Fd': 0.9, 'Fs': 0.75, 'r': 1},
        'B': {'Fa': 1.0, 'Fd': 1.0, 'Fs': 0.75, 'r': 1},
        'C': {'Fa': 1.4, 'Fd': 1.36, 'Fs': 0.85, 'r': 1},
        'D': {'Fa': 1.6, 'Fd': 1.62, 'Fs': 1.02, 'r': 1},
        'E': {'Fa': 1.8, 'Fd': 2.1, 'Fs': 1.75, 'r': 1.5}
    }

    # Parámetros η según zona sísmica
    eta_zona = {
        'Costa': 1.8,
        'Sierra': 2.48,
        'Oriente': 2.60
    }

    return parametros[tipo_suelo], eta_zona[zona_sismica]

def espectro_diseno(T, Z, Fa, Fd, Fs, eta, r=1):
    T0 = 0.1 * Fs * Fd / Fa
    Tc = 0.55 * Fs * Fd / Fa
    Sa = np.zeros_like(T)
    Se = np.zeros_like(T)  # Espectro elástico
    Si = np.zeros_like(T)  # Espectro inelástico

    for i, t in enumerate(T):
        if t <= T0:
            Sa[i] = Z * Fa * (1 + (eta - 1) * t / T0)
        elif T0 < t <= Tc:
            Sa[i] = eta * Z * Fa
        else:
            Sa[i] = eta * Z * Fa * (Tc / t)**r
        
        # Espectro Elástico e Inelástico
        Se[i] = Sa[i]
        Si[i] = Sa[i] / (r + 1)
    
    return Sa, Se, Si, T0, Tc

# Parámetros seleccionados por el usuario
tipo_suelo = input("Ingrese el tipo de suelo (A, B, C, D, E): ")
zona_sismica = input("Ingrese la zona sísmica (Costa, Sierra, Oriente): ")

# Obtener parámetros según el tipo de suelo y zona sísmica
parametros, eta = calcular_parametros(tipo_suelo, zona_sismica)

# Datos del espectro
T = np.linspace(0.01, 4, 500)  # Rango de periodos
Z = 0.40                        # Factor Z para una zona sísmica específica

# Generar espectro
Sa, Se, Si, T0, Tc = espectro_diseno(T, Z, **parametros, eta=eta)

# Graficar el espectro
plt.figure(figsize=(10, 6))
plt.plot(T, Sa, label='Espectro de Diseño', color='b', linewidth=2)
plt.plot(T, Se, label='Espectro Elástico', color='c', linestyle='--', linewidth=2)
plt.plot(T, Si, label='Espectro Inelástico', color='m', linestyle='-.', linewidth=2)
plt.axvline(x=T0, color='r', linestyle='--', label='$T_0$')
plt.axvline(x=Tc, color='g', linestyle='--', label='$T_c$')

plt.title('Espectro de Diseño Sísmico')
plt.xlabel('Periodo (s)')
plt.ylabel('Sa (g)')
plt.xlim(0, 4)
plt.ylim(0, max(Sa) + 0.1)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.show()E
