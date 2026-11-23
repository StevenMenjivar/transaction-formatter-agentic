# Política de detección de campos

- Los alias exactos tienen prioridad sobre coincidencias aproximadas.
- `total` tiene prioridad sobre `amount` y `monto`.
- Si hay candidatos contradictorios, se selecciona el de mayor prioridad y se emite `FIELD_CONFLICT`.
- El umbral fuzzy se configura con `FUZZY_THRESHOLD`; el valor inicial es 0.91.
