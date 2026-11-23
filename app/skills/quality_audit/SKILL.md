---
name: quality_audit
description: Evalúa métricas y señales de calidad sin modificar los datos normalizados.
version: 1.0.0
---

# Quality Audit

## Cuándo usarla
Después de normalizar o cuando se solicita un resumen de calidad.

## Procedimiento
1. Leer métricas de validez, monedas y fechas.
2. Contar detalles que contienen advertencias.
3. Generar hallazgos con código, severidad, cantidad y explicación.
4. Calcular `qualityScore` como porcentaje de registros válidos sobre procesados.

## Restricciones
No modificar ni descartar transacciones. No presentar el score como certificación financiera o regulatoria.

## Salida
`findings`, `qualityScore` y `checked`.
