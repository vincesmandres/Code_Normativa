import numpy as np

def parse_values(variables):
    """
    Parsea los valores de las variables de la interfaz
    
    Args:
        variables: Diccionario con las variables tkinter
        
    Returns:
        Tupla con zona_sismica, tipo_suelo, region, r_valor, i_valor
    """
    # Parsear zona sísmica
    zona_text = variables['zona_sismica_var'].get()
    zona_romana = zona_text.split(' ')[0]
    
    # Parsear tipo de suelo
    tipo_suelo_text = variables['tipo_suelo_var'].get()
    tipo_suelo = tipo_suelo_text.split(' ')[0]
    
    # Parsear factor R
    r_text = variables['r_var'].get()
    r_valor = float(r_text.split(' ')[0])
    
    # Parsear factor I
    i_text = variables['i_var'].get()
    i_valor = float(i_text.split(' ')[0])
    
    return zona_romana, tipo_suelo, variables['region_var'].get(), r_valor, i_valor

def calculate_parameters(tipo_suelo, zona_sismica, region):
    """
    Calcula los parámetros sísmicos según el tipo de suelo, zona sísmica y región
    
    Args:
        tipo_suelo: Tipo de suelo (A, B, C, D, E o F)
        zona_sismica: Zona sísmica (I, II, III, IV, V o VI)
        region: Región (Costa, Sierra, Oriente)
        
    Returns:
        Tupla con (parametros, eta, Z)
    """
    # Factores de amplificación del suelo según las tablas
    # Tabla 3: Fa - Coeficiente de amplificación de suelo en la zona de período corto
    Fa_valores = {
        'A': {'I': 0.9, 'II': 0.9, 'III': 0.9, 'IV': 0.9, 'V': 0.9, 'VI': 0.9},
        'B': {'I': 1.0, 'II': 1.0, 'III': 1.0, 'IV': 1.0, 'V': 1.0, 'VI': 1.0},
        'C': {'I': 1.4, 'II': 1.3, 'III': 1.25, 'IV': 1.23, 'V': 1.2, 'VI': 1.18},
        'D': {'I': 1.6, 'II': 1.4, 'III': 1.3, 'IV': 1.25, 'V': 1.2, 'VI': 1.12},
        'E': {'I': 1.8, 'II': 1.4, 'III': 1.25, 'IV': 1.1, 'V': 1.0, 'VI': 0.85}
    }
    
    # Tabla 4: Fd - Amplificación de las ordenadas del espectro elástico de respuesta de desplazamientos
    Fd_valores = {
        'A': {'I': 0.9, 'II': 0.9, 'III': 0.9, 'IV': 0.9, 'V': 0.9, 'VI': 0.9},
        'B': {'I': 1.0, 'II': 1.0, 'III': 1.0, 'IV': 1.0, 'V': 1.0, 'VI': 1.0},
        'C': {'I': 1.36, 'II': 1.28, 'III': 1.19, 'IV': 1.15, 'V': 1.11, 'VI': 1.06},
        'D': {'I': 1.62, 'II': 1.45, 'III': 1.36, 'IV': 1.28, 'V': 1.19, 'VI': 1.11},
        'E': {'I': 2.1, 'II': 1.75, 'III': 1.7, 'IV': 1.65, 'V': 1.6, 'VI': 1.5}
    }
    
    # Tabla 5: Fs - Comportamiento no lineal de los suelos
    Fs_valores = {
        'A': {'I': 0.75, 'II': 0.75, 'III': 0.75, 'IV': 0.75, 'V': 0.75, 'VI': 0.75},
        'B': {'I': 0.75, 'II': 0.75, 'III': 0.75, 'IV': 0.75, 'V': 0.75, 'VI': 0.75},
        'C': {'I': 0.85, 'II': 0.94, 'III': 1.02, 'IV': 1.06, 'V': 1.11, 'VI': 1.23},
        'D': {'I': 1.02, 'II': 1.06, 'III': 1.11, 'IV': 1.19, 'V': 1.28, 'VI': 1.40},
        'E': {'I': 1.5, 'II': 1.6, 'III': 1.7, 'IV': 1.8, 'V': 1.9, 'VI': 2.0}
    }
    
    # Valores de r (factor de control de caída del espectro)
    r_valores = {
        'A': 1,
        'B': 1,
        'C': 1,
        'D': 1,
        'E': 1.5
    }
    
    # Obtener valores específicos para el tipo de suelo y zona sísmica
    Fa = Fa_valores[tipo_suelo][zona_sismica]
    Fd = Fd_valores[tipo_suelo][zona_sismica]
    Fs = Fs_valores[tipo_suelo][zona_sismica]
    r = r_valores[tipo_suelo]
    
    # Crear el diccionario de parámetros
    parametros = {
        'Fa': Fa,
        'Fd': Fd,
        'Fs': Fs,
        'r': r
    }

    eta_zona = {
        'Costa (Excepto Esmeralda)': 1.8,
        'Sierra, Esmeralda y Galapagos': 2.48,
        'Oriente': 2.60
    }

    Z_valores = {
        'I': 0.15, 'II': 0.25, 'III': 0.30,
        'IV': 0.35, 'V': 0.40, 'VI': 0.50
    }

    return parametros, eta_zona[region], Z_valores[zona_sismica]

def calculate_spectrum(Z, Fa, Fd, Fs, eta, R, I, phi_P, phi_E, r=1):
    """
    Calcula el espectro sísmico de diseño
    
    Args:
        Z: Factor de zona sísmica
        Fa, Fd, Fs: Factores de amplificación del suelo
        eta: Factor de región
        R: Factor de reducción de respuesta estructural
        I: Factor de importancia
        phi_P: Factor de configuración en planta
        phi_E: Factor de configuración en elevación
        r: Exponente que controla la caída del espectro (por defecto 1)
        
    Returns:
        Tupla con (T, Sa, Se, Si, T0, Tc, TL)
    """
    # Calcular períodos característicos
    T0 = 0.1 * Fs * Fd / Fa
    Tc = 0.55 * Fs * Fd / Fa
    TL = 2.4 * Fd
    
    # Generar el espectro
    T = np.linspace(0, 6, 1000)  # Rango de periodos de 0 a 6 segundos
    Sa = np.zeros_like(T)
    Se = np.zeros_like(T)
    Si = np.zeros_like(T)

    for i, t in enumerate(T):
        if t == 0:
            Sa[i] = Z*Fa
        elif t <= T0:
            Sa[i] = Z * Fa * (1 + (eta - 1) * t / T0)
        elif T0 < t <= Tc:
            Sa[i] = eta * Z * Fa
        else:
            Sa[i] = eta * Z * Fa * (Tc / t)**r 

        Se[i] = Sa[i]
        Si[i] = (I * Sa[i]) / (R * phi_P * phi_E)
    
    return T, Sa, Se, Si, T0, Tc, TL