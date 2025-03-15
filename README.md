# Generador de Espectro Sísmico

Este script genera el **Espectro de Diseño Sísmico**, el **Espectro Elástico** y el **Espectro Inelástico** mediante una interfaz gráfica interactiva basada en **Tkinter**.

---

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
\[
S_i = \frac{I \cdot S_a(T_a)}{R \cdot \Phi_P \cdot \Phi_E}
\]

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

### **Espectro de Diseño \( S_a \)**
- Para \( T \leq T_0 \)
\[
S_a = Z \cdot F_a \cdot \left( 1 + (\eta - 1) \frac{T}{T_0} \right)
\]

- Para \( T_0 < T \leq T_c \)
\[
S_a = \eta \cdot Z \cdot F_a
\]

- Para \( T_c < T \leq T_L \)
\[
S_a = \eta \cdot Z \cdot F_a \cdot \left( \frac{T_c}{T} \right)^r
\]

- Para \( T > T_L \)
\[
S_a = S_a(T_L)
\]

### **Espectro Inelástico \( S_i \)**
\[
S_i = \frac{I \cdot S_a(T_a)}{R \cdot \Phi_P \cdot \Phi_E}
\]

---

## 📌 Valores Clave

- **`I`**: Coeficiente de importancia (según tipo de edificio: esenciales, especiales u ordinarios).
- **`R`**: Factor de redundancia sísmica (según el tipo de estructura).
- **`Φ_P`** y **`Φ_E`**: Factores de regularidad estructural (valores entre **0.9** y **1.0**).

---

## 🛠️ Posibles Mejoras

🔹 Agregar una opción para exportar el gráfico en formato **PDF** o **PNG**.  
🔹 Incluir una tabla de resultados que muestre valores calculados de \( T_0 \), \( T_c \) y \( T_L \).  
🔹 Permitir al usuario seleccionar directamente los coeficientes **`R`**, **`I`**, **`Φ_P`** y **`Φ_E`**.  

---

## 📞 Soporte
Si tienes dudas o deseas agregar nuevas funcionalidades, ¡no dudes en ponerte en contacto! 😊
