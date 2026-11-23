---
name: export_result
description: Serializa transacciones canónicas en JSON preservando precisión decimal.
version: 1.0.0
---

# Export Result

## Cuándo usarla
Solo cuando el objetivo solicite exportar, descargar o generar JSON normalizado.

## Entradas
Resultado producido por `normalize_transactions`.

## Salida
Cadena JSON indentada y cantidad de transacciones exportadas.

## Restricciones
No exportar el documento original ni convertir `Decimal` a punto flotante binario.
