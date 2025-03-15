import numpy as np
import matplotlib.pyplot as plt

def espectro_diseno(T, Z, Fa, Fd, Fs, eta, r=1):
    T0 = 0.1 * Fs * Fd / Fa
    Tc = 0.55 * Fs * Fd / Fa
    Sa = np.zeros_like(T)

    for i, t in enumerate(T):
        if t <= T0:
            Sa[i] = Z * Fa * (1 + (eta - 1) * t / T0)
        elif T0 < t <= Tc:
            Sa[i] = eta * Z * Fa
        else:
            Sa[i] = eta * Z * Fa * (Tc / t)**r
    
    return Sa

# Parámetros de entrada para el espectro de diseño
T = np.linspace(0, 4, 500)  # Rango de periodos
Z = 0.40                    # Factor Z para una zona sísmica específica (ajusta según tu caso)
Fa = 1.4                    # Coeficiente de amplificación de aceleración (ejemplo tipo D)
Fd = 1.62                   # Coeficiente de amplificación de desplazamiento (ejemplo tipo D)
Fs = 1.02                   # Factor de comportamiento no lineal (ejemplo tipo D)
eta = 2.48                  # Razón Sa/Z para una zona sísmica específica (ajusta según tu caso)
r = 1                       # Factor r para suelos tipo D

# Generar espectro
Sa = espectro_diseno(T, Z, Fa, Fd, Fs, eta, r)

# Graficar el espectro
plt.figure(figsize=(8, 5))
plt.plot(T, Sa, label='Espectro de Diseño', color='b')
plt.axvline(x=0.1 * Fs * Fd / Fa, color='r', linestyle='--', label='$T_0$')
plt.axvline(x=0.55 * Fs * Fd / Fa, color='g', linestyle='--', label='$T_c$')
plt.title('Espectro de Diseño Sísmico')
plt.xlabel('Periodo (s)')
plt.ylabel('Sa (g)')
plt.grid(True)
plt.legend()
plt.show()
