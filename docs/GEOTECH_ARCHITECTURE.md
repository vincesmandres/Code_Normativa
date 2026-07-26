# Arquitectura geotecnica y criterio normativo

## Alcance implementado

La version `codenormative.geotech.v2` separa el motor de evaluacion, el registro de perforaciones y la presentacion. Un proyecto admite multiples sondeos con coordenadas, cota, nivel freatico, profundidad y estratos. La vista 3D es una correlacion conceptual de columnas; no interpola superficies de diseno ni reemplaza el modelo geologico del profesional.

El expediente integral conserva una instantanea fechada de entradas y resultados de espectro, revision estructural y geotecnia. El PDF se identifica expresamente como pre-revision.

## Jerarquia de referencias

1. NEC-SE-GC y NEC-SE-DS, como normativa nacional primaria del producto.
2. EN 1997-1/2 (Eurocode 7), como referencia internacional para reglas generales, investigacion y ensayos.
3. FHWA GEC 5 y guias de informes geotecnicos, para calidad, caracterizacion y trazabilidad del modelo del terreno.
4. Terzaghi, Peck y Mesri, como referencia teorica; sus correlaciones no deben aplicarse sin documentar hipotesis, unidades, drenaje, geometria y dominio de validez.

Referencias oficiales consultadas:

- https://www.habitatyvivienda.gob.ec/wp-content/uploads/2023/03/7.-NEC-SE-GC-Geotecnia-y-Cimentaciones.pdf
- https://eurocodes.jrc.ec.europa.eu/EN-Eurocodes/eurocode-7-geotechnical-design
- https://www.fhwa.dot.gov/engineering/geotech/subsurface/

## Integracion de inferencia

La API futura debe recibir resultados ya calculados y devolver JSON validado. El modelo puede explicar hallazgos, detectar contradicciones y solicitar datos faltantes. No puede inventar parametros, recalcular capacidad portante, seleccionar una cimentacion como definitiva ni declarar cumplimiento. Cada afirmacion debe incluir evidencia, referencia, confianza y banderas de datos insuficientes.

Contrato propuesto: `POST /api/v1/interpretations/foundation`. Deben registrarse version del motor determinista, version normativa, modelo, prompt, respuesta, usuario y fecha. La salida requiere aprobacion profesional antes de incorporarse al reporte firmado.
