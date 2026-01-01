# Generador de Espectro Sísmico
![Build Status](https://github.com/vincesmandres/Code_Normativa/actions/workflows/ci.yml/badge.svg) ![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Este script genera el **Espectro de Diseño Sísmico**, el **Espectro Elástico** y el **Espectro Inelástico** mediante una interfaz gráfica interactiva basada en **Tkinter**.

---

@'
# Ejecución rápida (Windows)

```powershell
# 1) Crear y activar entorno
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2) Instalar dependencias
pip install -r requirements.txt

# 3) Ejecutar la app
python app.py   # o: python main.py
"@

## 🚀 Funcionalidades

✅ Cálculo automático de los factores:
- **`Fa`**, **`Fd`**, **`Fs`** y **`r`** según el **tipo de suelo**.
- **`η` (eta)** y **`Z`** en función de la **región** y **zona sísmica**.
- Cálculo automático de los puntos clave:
  - **`T0`** → Inicio del valor máximo.
  - **`Tc`** → Fin del valor constante.
  - **`TL`** → Inicio del valor estabilizado.

✅ Generación del:
- **Espectro de Diseño** (línea negra gruesa).
- **Espectro Elástico** (línea negra delgada).
- **Espectro Inelástico** (línea gris).

✅ Incluye el cálculo del **Espectro Reducido** mediante la fórmula:
```
S_i = I * S_a(T_a) / (R * Φ_P * Φ_E)
```

✅ Interfaz gráfica interactiva que permite seleccionar:
- **Tipo de suelo** (A, B, C, D, E).
- **Zona sísmica** (I a VI).
- **Región** (Costa, Sierra, Oriente).

---

## 📋 Instrucciones de Uso

1. **Instala las bibliotecas necesarias:**
```
pip install numpy matplotlib tkinter
```

2. **Ejecuta el script**.

3. En la interfaz, selecciona:
- El **tipo de suelo**.
- La **zona sísmica**.
- La **región**.

4. Haz clic en el botón **"Generar Espectro"** para mostrar el gráfico.

---

## ⚙️ Cálculos en el Espectro

### **Espectro de Diseño (Sa)**
- Para `T ≤ T0`
```
Sa = Z * Fa * [ 1 + (η - 1) * (T / T0) ]
```

- Para `T0 < T ≤ Tc`
```
Sa = η * Z * Fa
```

- Para `Tc < T ≤ TL`
```
Sa = η * Z * Fa * (Tc / T)^r
```

- Para `T > TL`
```
Sa = η * Z * Fa * (Tc / T)^r
```

### **Espectro Inelástico (Si)**
```
Si = I * Sa(Ta) / (R * Φ_P * Φ_E)
```

---

## 📌 Valores Clave

- **`I`**: Coeficiente de importancia (según tipo de edificio: esenciales, especiales u ordinarios).
- **`R`**: Factor de redundancia sísmica (según el tipo de estructura).
- **`Φ_P`** y **`Φ_E`**: Factores de regularidad estructural (valores entre **0.9** y **1.0**).

---

## 🛠️ Posibles Mejoras

🔹 Agregar una opción para exportar el gráfico en formato **PDF** o **PNG**.  
🔹 Incluir una tabla de resultados que muestre valores calculados de `T0`, `Tc` y `TL`.  
🔹 Permitir al usuario seleccionar directamente los coeficientes **`R`**, **`I`**, **`Φ_P`** y **`Φ_E`**.  

---

## 📞 Soporte
Si tienes dudas o deseas agregar nuevas funcionalidades, ¡no dudes en ponerte en contacto! 😊
# Quick start (Windows)

```powershell
# Option A: one command (installs deps if missing)
python run_app.py

# Option B: explicit steps
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m espectro_nec.main
```

# Build EXE (Windows)

```powershell
# Option A: use the helper script
.\build_exe.ps1

# Option B: manual
python -m pip install -r requirements.txt
python -m pip install -r requirements-build.txt
pyinstaller --noconfirm --clean --windowed --name EspectroNEC --paths .\src .\run_app.py
```

The EXE will be at `dist\EspectroNEC\EspectroNEC.exe`.
# Quick start (Windows)

```powershell
# One-file EXE (build once, then copy dist\NEC15_app.exe to any PC)
.\build_exe.ps1

# Install in a venv (if you want a Python install)
.\install.ps1
```
## Supported Python

- Python 3.10, 3.11, 3.12
- For other versions, use the EXE build

## Quick start (Windows)

```powershell
# Use a supported Python
py -3.11 .\run_app.py
```

## Build EXE (Windows)

```powershell
# One-file EXE (build once, then copy dist\NEC15_app.exe to any PC)
.\build_exe.ps1
```
