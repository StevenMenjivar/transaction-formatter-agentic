---
name: normalize_transactions
description: Detecta registros de transacciones y los convierte al esquema canónico.
version: 1.0.0
---

# Normalize Transactions

## Cuándo usarla
Cuando el usuario proporciona un JSON que puede contener una o varias transacciones en estructuras anidadas.

## Entradas
- `payload`: objeto, arreglo o documento JSON.
- `options.timezone`: zona IANA para normalización de fechas.
- `options.date_order`: `DMY` o `MDY`.

## Procedimiento
1. Descubrir colecciones respetando el orden y la profundidad máxima.
2. Detectar campos por alias y coincidencia aproximada conservadora.
3. Normalizar monto, moneda, fecha y estado.
4. Preservar originales, errores, advertencias y trazabilidad.

## Restricciones
No inventar campos, no interpretar enteros como centavos y no convertir un registro inválido en válido por inferencia.

## Salida
`transactions`, `invalidTransactions`, `details` y `metrics`.

## Ejemplo
Entrada: `[{"amount":"12.50","currency":"USD","status":"approved"}]`.
Salida: una transacción con `amount=12.50`, `currency=USD`, `status=SUCCESS`.
