# Generador de Espectro de Diseño Sísmico - NEC

Herramienta de escritorio para generar espectros de diseño sísmico de acuerdo a la Norma Ecuatoriana de la Construcción (NEC).

<!-- El usuario agregará una captura de pantalla aquí -->

## Cómo Ejecutar la Aplicación

### Requisitos

- Python 3.10, 3.11, o 3.12

### Instrucciones

1.  **Clona o descarga el repositorio.**

2.  **Abre una terminal en el directorio del proyecto.**

3.  **Ejecuta el siguiente comando:**

    ```powershell
    py -3.11 .\run_app.py
    ```

    La primera vez que se ejecute, el script instalará automáticamente las dependencias necesarias desde `requirements.txt`. Las ejecuciones posteriores iniciarán la aplicación directamente.

## Cómo Construir el Archivo Ejecutable (.EXE)

Si deseas compilar la aplicación en un único archivo `.EXE` para distribuirla fácilmente, puedes usar el script de compilación incluido.

1.  **Abre una terminal de PowerShell en el directorio del proyecto.**

2.  **Ejecuta el siguiente comando:**

    ```powershell
    .\build_exe.ps1
    ```

    El archivo ejecutable se encontrará en el directorio `dist`.

## Funcionalidades Principales

-   Cálculo del espectro de diseño sísmico elástico e inelástico.
-   Interfaz gráfica de usuario moderna y fácil de usar.
-   Exportación de datos a múltiples formatos:
    -   Excel (`.xlsx`)
    -   ETABS (`.txt`)
    -   Gráfico (`.png`)
    -   Reporte completo (`.pdf`)
-   Visualización interactiva del gráfico del espectro.