# CodeNormative

Plataforma para generar espectros de diseno sismico segun la Norma Ecuatoriana de la Construccion (NEC).

Actualmente el proyecto funciona como una aplicacion de escritorio en Python. El objetivo natural del producto es evolucionar hacia una plataforma web para que ingenieros, estudiantes y equipos tecnicos puedan calcular, revisar, exportar y compartir espectros sin depender de una instalacion local en Windows.

## Que hace

CodeNormative calcula el espectro de diseno sismico a partir de parametros normativos de la NEC:

- Zona sismica: I, II, III, IV, V o VI.
- Region: Costa, Sierra/Esmeraldas/Galapagos u Oriente.
- Tipo de suelo: A, B, C, D o E.
- Factor de reduccion estructural `R`.
- Factor de importancia `I`.
- Factores de configuracion `phiP` y `phiE`.

Con esos datos, la aplicacion calcula:

- Factores de suelo `Fa`, `Fd` y `Fs`.
- Factor regional `eta`.
- Factor de zona `Z`.
- Periodos caracteristicos `T0`, `Tc` y `TL`.
- Espectro elastico `Sa` / `Se`.
- Espectro inelastico `Si`.

## Salidas disponibles

La version de escritorio permite generar y exportar:

- Grafico del espectro de diseno.
- Tabla de periodos y aceleraciones.
- Archivo Excel `.xlsx`.
- Archivo `.txt` compatible con ETABS.
- Imagen del grafico `.png`, `.jpg` o `.pdf`.
- Reporte tecnico en PDF.

## Estado actual del proyecto

El repositorio contiene una aplicacion Python con interfaz grafica basada en Tkinter y ttkbootstrap.

Estructura principal:

```text
Code_Normativa/
+-- run_app.py
+-- build_exe.ps1
+-- requirements.txt
+-- requirements-build.txt
+-- pyproject.toml
+-- src/
    +-- espectro_nec/
        +-- app.py
        +-- constants.py
        +-- export_utilities.py
        +-- main.py
        +-- seismic_calculations.py
        +-- ui_components.py
```

Responsabilidades principales:

- `seismic_calculations.py`: logica normativa y calculo del espectro.
- `constants.py`: opciones de zona, region, suelo, R e I.
- `app.py`: coordinacion de la interfaz grafica y acciones del usuario.
- `ui_components.py`: construccion de controles visuales.
- `export_utilities.py`: exportaciones a Excel, ETABS, imagen y PDF.
- `run_app.py`: runner local que valida version de Python e instala dependencias si faltan.

## Ejecucion local

### Requisitos

- Python 3.10, 3.11 o 3.12.
- Windows recomendado para la version actual de escritorio.

### Iniciar la aplicacion

```powershell
py -3.11 .\run_app.py
```

La primera ejecucion instala las dependencias de `requirements.txt` si no estan disponibles.

### Construir ejecutable

```powershell
.\build_exe.ps1
```

El ejecutable se genera en la carpeta `dist`.

## Limitaciones de la version actual

- La experiencia depende de una instalacion local de Python o de un ejecutable generado.
- La interfaz esta pensada para escritorio, no para navegador.
- No hay persistencia de proyectos/calculos.
- No hay usuarios, historial, colaboracion ni enlaces compartibles.
- La logica de calculo esta acoplada parcialmente a la experiencia de escritorio.
- No hay API reutilizable para integraciones externas.

## Vision de plataforma web

La migracion recomendada es convertir CodeNormative en una plataforma web tecnica:

- Calculadora NEC accesible desde navegador.
- Grafico interactivo del espectro.
- Exportaciones desde la web.
- Guardado de proyectos y escenarios.
- Historial de calculos por usuario.
- Comparacion entre alternativas de suelo, zona o sistema estructural.
- Generacion de reportes tecnicos listos para entregar.
- API para integrarse con flujos de diseno estructural.

## Roadmap de migracion a web

### Fase 1: Separar el motor de calculo

Objetivo: dejar la logica normativa independiente de Tkinter.

Tareas:

- Mantener `seismic_calculations.py` como nucleo reutilizable.
- Crear modelos de entrada/salida claros para un calculo.
- Agregar pruebas unitarias para valores representativos de NEC.
- Validar errores de entrada sin depender de mensajes de interfaz grafica.

Resultado esperado:

- Un motor Python confiable que pueda usarse desde escritorio, API o tests.

### Fase 2: Crear una API

Objetivo: exponer el calculo por HTTP.

Stack sugerido:

- Backend: FastAPI.
- Validacion: Pydantic.
- Graficos/exportaciones: mantener Python para Excel, PDF y ETABS.

Endpoints iniciales:

```text
POST /api/spectrum
GET  /api/options
POST /api/export/excel
POST /api/export/etabs
POST /api/export/pdf
```

Resultado esperado:

- El calculo deja de depender de la app de escritorio y queda disponible para una futura web.

### Fase 3: Construir la interfaz web

Objetivo: reemplazar la pantalla de escritorio por una experiencia web.

Stack sugerido:

- Frontend: Next.js o React.
- Graficos: Plotly, Recharts o ECharts.
- UI: componentes propios o shadcn/ui.

Pantallas iniciales:

- Calculadora de espectro.
- Vista de resultados.
- Exportaciones.
- Comparacion de escenarios.

Resultado esperado:

- Una primera version web funcional que replica lo que hoy hace el software de PC.

### Fase 4: Convertirlo en plataforma

Objetivo: agregar funcionalidades que justifican el cambio de software local a producto web.

Funciones recomendadas:

- Cuentas de usuario.
- Guardado de proyectos.
- Historial de calculos.
- Duplicar escenarios.
- Compartir calculos por enlace.
- Plantillas de reporte.
- Branding institucional en PDF.
- Auditoria de parametros usados.

Resultado esperado:

- CodeNormative pasa de ser una calculadora aislada a una plataforma de trabajo.

### Fase 5: Despliegue y operacion

Objetivo: publicar la web y asegurar mantenimiento.

Opciones:

- Frontend en Vercel.
- Backend FastAPI en Render, Railway, Fly.io, Azure, AWS o un VPS.
- Base de datos PostgreSQL.
- Almacenamiento de reportes en S3 compatible o Blob Storage.

Resultado esperado:

- Plataforma accesible publicamente, con versionado, respaldos y posibilidad de crecer.

## Primeros pasos recomendados

1. Agregar tests al motor de calculo actual.
2. Crear una carpeta `api/` con FastAPI.
3. Exponer `POST /api/spectrum`.
4. Crear una primera interfaz web que consuma ese endpoint.
5. Mantener la app de escritorio funcionando mientras la web madura.
6. Migrar exportaciones una por una: Excel, ETABS, imagen y PDF.

## Propuesta de arquitectura futura

```text
code-normative/
+-- packages/
|   +-- engine/             # Motor de calculo NEC reutilizable
+-- apps/
|   +-- desktop/            # App actual o version mantenida
|   +-- api/                # FastAPI
|   +-- web/                # Next.js / React
+-- tests/
+-- docs/
```

Esta separacion permite mantener una unica fuente de verdad para los calculos, mientras la experiencia puede vivir en escritorio, API o web.

## Licencia

MIT.
