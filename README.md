# Transaction Normalizer — Agentic Edition

Sistema local de normalización de transacciones JSON con arquitectura modular y agentes especializados. Conserva el dashboard FastAPI y añade un supervisor que coordina skills deterministas, auditoría de calidad y exportación bajo demanda. Esta versión es una refactorización del proyecto https://github.com/StevenMenjivar/transaction-formatter. Con lo que se pretende reestructurar el proyecto mediante la integración de skills con propósitos específicos. 

## Contenido

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación en Windows](#instalación-en-windows)
- [Instalación en Linux y macOS](#instalación-en-linux-y-macos)
- [Ejecución](#ejecución)
- [Guía práctica del dashboard](#guía-práctica-del-dashboard)
- [Configuración](#configuración)
- [API](#api)
- [Reglas de normalización](#reglas-de-normalización)
- [Pruebas](#pruebas)
- [Solución de problemas](#solución-de-problemas)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Limitaciones](#limitaciones)

## Características

- Carga de archivos `.json` o ingreso directo del contenido JSON.
- Acepta objetos individuales, arreglos y arreglos de transacciones dentro de contenedores anidados.
- Reconocimiento de campos en inglés y español mediante alias y coincidencia aproximada conservadora.
- Prioridad explícita de `total` sobre `amount` y `monto`.
- Conversión monetaria con `Decimal`; los enteros no se convierten automáticamente a centavos.
- Identificación conservadora de monedas ISO-4217.
- Normalización de fechas ISO-8601 y zonas horarias configurables.
- Normalización de estados a `SUCCESS`, `FAILED`, `PENDING` o `UNKNOWN`.
- Separación de transacciones válidas, inválidas, advertencias y trazabilidad.
- Dashboard con métricas, gráficos, tablas, inspección y descarga del JSON normalizado.
- Navegación lateral hacia procesamiento, configuración y documentación.
- Al seleccionar **Ver** en una tabla, la interfaz desplaza la página a la inspección de la transacción elegida.
- Sin base de datos ni almacenamiento persistente. El backend conserva temporalmente el último resultado en memoria.

## Requisitos

- Python **3.11 a 3.14 recomendado**. Python 3.10 o superior puede funcionar, pero las versiones más recientes de Python pueden tardar en recibir wheels de todas las dependencias.
- `pip` actualizado.
- Navegador moderno (Chrome, Edge o Firefox).
- Conexión a Internet para cargar Chart.js desde CDN y mostrar los gráficos. El procesamiento principal se ejecuta localmente.

> **Nota para Windows:** se recomienda crear un entorno virtual dentro de la carpeta del proyecto. Los comandos siguientes utilizan `python -m pip` para asegurar que `pip` corresponda al intérprete activo.

## Instalación en Windows

Abre PowerShell en la carpeta raíz del proyecto, donde se encuentran `requirements.txt` y `run.py`.

### 1. Comprobar Python

```powershell
py --version
py -0p
```

Si tienes varias versiones instaladas y deseas seleccionar Python 3.14, puedes crear el entorno así:

```powershell
py -3.14 -m venv .venv
```

Si el comando `py -3.14` no está disponible, instala una versión compatible de Python o utiliza el ejecutable `python` que tengas configurado:

```powershell
python -m venv .venv
```

### 2. Activar el entorno virtual

```powershell
.\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la activación por la política de ejecución, permite scripts únicamente en la sesión actual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Esta modificación se limita a la ventana actual de PowerShell.

### 3. Actualizar pip e instalar dependencias

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

Si `pip check` no reporta dependencias incompatibles, la instalación está lista.

### 4. Ejecutar

```powershell
python run.py
```

Abre en el navegador: <http://127.0.0.1:8000>

## Instalación en Linux y macOS

Desde la carpeta raíz del proyecto:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
python run.py
```

Abre <http://127.0.0.1:8000> en el navegador.

## Ejecución

El servidor se inicia desde la raíz del proyecto:

```bash
python run.py
```

Direcciones disponibles:

- Dashboard: <http://127.0.0.1:8000>
- Documentación interactiva de la API (Swagger UI): <http://127.0.0.1:8000/docs>
- Especificación OpenAPI: <http://127.0.0.1:8000/openapi.json>

Para detener el servidor, vuelve a la terminal y presiona `Ctrl + C`.

## Guía práctica del dashboard

Esta sección describe un flujo de trabajo recomendado para procesar y revisar un conjunto de transacciones.

### 1. Abrir el dashboard y localizar sus secciones

Al iniciar la aplicación se muestra el área principal. El menú lateral permite navegar entre **Normalización**, **Procesamiento JSON**, **Configuración** y **Documentación**. Las opciones desplazan la página hasta la sección correspondiente.

### 2. Cargar datos JSON

En **Fuente de datos** puedes:

- Pulsar **Seleccionar archivo** para elegir un archivo `.json` de tu equipo.
- Arrastrar un archivo JSON hasta el área de carga.
- Pegar el contenido JSON directamente en el editor.
- Pulsar **Cargar ejemplo** para completar el editor con registros de demostración.

El tamaño máximo predeterminado de entrada es de 10 MB.

### 3. Configurar el procesamiento

Antes de normalizar, selecciona:

- **Zona horaria:** define cómo interpretar las fechas sin zona horaria y a qué zona convertir las fechas que sí incluyen zona.
- **Fechas ambiguas:** selecciona `DD/MM/YYYY` (DMY) o `MM/DD/YYYY` (MDY) para fechas numéricas que puedan interpretarse de ambas maneras.

Por ejemplo, `10/03/2025` puede representar el 10 de marzo o el 3 de octubre, dependiendo de la opción elegida.

### 4. Ejecutar la normalización

Pulsa **Normalizar transacciones**. La aplicación enviará el contenido al backend y presentará el resumen del procesamiento.

Si el JSON no puede interpretarse o no contiene transacciones detectables, se mostrará un mensaje con el motivo. Corrige el contenido y vuelve a intentarlo.

### 5. Interpretar el resumen

El dashboard presenta indicadores como:

- **Procesadas:** cantidad total de elementos detectados.
- **Válidas:** registros que contienen un monto interpretable.
- **Inválidas:** registros que no pudieron normalizarse, por ejemplo, por falta de monto.
- **Con advertencias:** transacciones válidas que requieren atención en uno o más campos.
- **Monedas desconocidas** y **fechas no disponibles:** indicadores de calidad de datos.
- **Distribución por estado y moneda:** gráficos que resumen los registros válidos.

### 6. Consultar transacciones válidas e inválidas

Las tablas permiten revisar los registros de cada categoría:

- En **Transacciones válidas**, revisa el monto, moneda, fecha y estado normalizados.
- En **Transacciones inválidas**, revisa la posición, ruta de origen y motivo del rechazo.
- Pulsa **Ver** para abrir la inspección del registro seleccionado. La página se desplaza automáticamente a **Inspección de transacción**.

La inspección permite comparar el JSON original con el resultado normalizado y consultar la trazabilidad, los campos detectados, las advertencias o los errores.

### 7. Exportar el resultado

En **Resultado estandarizado**:

- **Copiar JSON:** copia el resultado normalizado al portapapeles. El navegador puede solicitar permiso para utilizarlo.
- **Descargar JSON:** descarga el resultado como `transacciones_normalizadas.json`.

### 8. Reiniciar la entrada

Pulsa **Limpiar** para borrar la entrada actual y ocultar los resultados de la interfaz. El procesamiento nuevo sustituye al resultado anterior almacenado temporalmente en el backend.

## Configuración

Las siguientes variables de entorno permiten ajustar los límites y valores predeterminados:

| Variable | Valor predeterminado | Descripción |
|---|---:|---|
| `MAX_FILE_BYTES` | `10485760` | Tamaño máximo de entrada en bytes (10 MB). |
| `MAX_TRANSACTIONS` | `50000` | Máximo de elementos transaccionales detectados. |
| `MAX_DEPTH` | `10` | Profundidad máxima de exploración de estructuras JSON. |
| `DEFAULT_TIMEZONE` | `UTC` | Zona horaria predeterminada (identificador IANA). |
| `DEFAULT_DATE_ORDER` | `DMY` | Orden predeterminado de fechas ambiguas: `DMY` o `MDY`. |
| `FUZZY_THRESHOLD` | `0.91` | Umbral de similitud textual para detectar campos. |

Ejemplo en PowerShell:

```powershell
$env:DEFAULT_TIMEZONE="America/El_Salvador"
$env:DEFAULT_DATE_ORDER="DMY"
python run.py
```

La interfaz también permite seleccionar la zona horaria y el orden de fechas para cada ejecución.

## API

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/api/health` | Estado del servicio. |
| `POST` | `/api/process` | Procesa un archivo multipart (`file` o `json_text`) o un cuerpo JSON. |
| `GET` | `/api/results/{processing_id}` | Devuelve el JSON normalizado. |
| `GET` | `/api/metrics/{processing_id}` | Devuelve las métricas del procesamiento. |
| `GET` | `/api/transactions/{processing_id}?kind=valid\|invalid` | Lista transacciones válidas o inválidas. |
| `GET` | `/api/transactions/{processing_id}/{transaction_id}` | Devuelve el detalle de una transacción válida. |
| `GET` | `/api/export/{processing_id}` | Descarga el resultado normalizado. |

El último procesamiento se conserva temporalmente en memoria. Una nueva ejecución reemplaza el resultado anterior y reiniciar el servidor elimina los resultados. No se utiliza una base de datos.

## Reglas de normalización

### Monto

`total`, `transactionTotal`, `totalAmount` y `totalTransaccion` tienen prioridad sobre `amount`, `transactionAmount`, `monto` y `montoTransaccion`. Los enteros conservan su escala: `10050` no se transforma en `100.50`. Se aceptan montos negativos y cero. Se utiliza `Decimal` internamente.

### Moneda

Una propiedad explícita válida prevalece sobre el código ISO embebido en el importe. Los símbolos ambiguos no se utilizan para adivinar la moneda. La lista de símbolos inequívocos soportados está en `app/core/constants.py`.

### Fechas

Las fechas sin zona se interpretan en la zona configurada. Las fechas con zona se convierten a la zona configurada. La ausencia de fecha se representa como `null` sin invalidar ni advertir; una fecha presente pero no interpretable genera una advertencia. El resultado incluye el offset ISO-8601. Para fechas como `10/03/2025`, la interfaz permite elegir DMY o MDY.

### Estado

Las equivalencias iniciales se encuentran en `app/core/constants.py` y pueden ampliarse. Un estado no reconocido se convierte en `UNKNOWN`.

### Transacciones inválidas

La falta de monto o un monto no convertible invalida el registro. Fecha, moneda, referencia y concepto pueden ser `null`. Los elementos que no sean objetos se reportan como inválidos.

## Pruebas

Desde la raíz del proyecto y con el entorno virtual activado:

```powershell
python -m pytest -q
```

## Solución de problemas

### `python` o `py` no se reconoce como comando

Python no está instalado o no está agregado al `PATH`.

- Comprueba si el lanzador de Windows está disponible: `py --version`.
- Comprueba las versiones detectadas: `py -0p`.
- Si ninguno funciona, instala Python desde <https://www.python.org/downloads/> y habilita la opción para agregar Python al `PATH` durante la instalación.
- Cierra y vuelve a abrir PowerShell después de instalarlo.

### `pip` no se reconoce o instala paquetes en otro Python

Evita ejecutar `pip` directamente. Utiliza siempre:

```powershell
python -m pip --version
python -m pip install -r requirements.txt
```

La ruta que muestra `python -m pip --version` debe corresponder al entorno virtual activo (`.venv`). Si no corresponde, activa el entorno desde la carpeta del proyecto y vuelve a ejecutar el comando.

### PowerShell no permite activar `.venv`

Ejecuta en la misma ventana:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### `Microsoft Visual C++ 14.0 or greater is required` o `Failed building wheel for PyYAML`

La configuración actual utiliza `uvicorn` sin el extra `[standard]`, por lo que PyYAML no es una dependencia necesaria para ejecutar esta aplicación. Comprueba que `requirements.txt` contenga:

```text
uvicorn>=0.30,<1.0
```

No debe decir `uvicorn[standard]` ni incluir PyYAML si no se necesita por otra razón. Después, con el entorno virtual activado, ejecuta:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip check
```

Si el error persiste, revisa qué paquete solicita PyYAML en el mensaje completo de instalación. En Python muy reciente puede que alguna dependencia todavía no publique wheels compatibles; prueba con Python 3.14 o 3.13 en un entorno virtual nuevo. No instales paquetes de compilación de terceros como primera solución.

### `ModuleNotFoundError: No module named 'jinja2'`

Jinja2 es necesario para renderizar `index.html`. Instálalo en el entorno activo y verifica que esté declarado en `requirements.txt`:

```powershell
python -m pip install "Jinja2>=3.1,<4.0"
python -m pip check
```

### `ModuleNotFoundError` para otra dependencia

Comprueba que el entorno virtual esté activo y reinstala las dependencias declaradas:

```powershell
python -m pip install -r requirements.txt
python -m pip check
```

Si el módulo sigue faltando, confirma que `python` y `pip` pertenecen al mismo entorno:

```powershell
where.exe python
python -m pip --version
```

### Error de plantilla `TypeError: cannot use 'tuple' as a dict key`

Comprueba que el endpoint principal en `app/main.py` use la llamada compatible con las versiones actuales de Starlette:

```python
return templates.TemplateResponse(
    request=request,
    name="index.html"
)
```

Y que `Request` esté importado desde FastAPI:

```python
from fastapi import FastAPI, Request
```

### `Address already in use` o el puerto 8000 está ocupado

Otra aplicación está utilizando el puerto 8000. Cierra el proceso que lo ocupa o cambia el puerto en `run.py`. Por ejemplo, para utilizar el puerto 8001, modifica la llamada de Uvicorn a:

```python
uvicorn.run("app.main:app", host="127.0.0.1", port=8001, reload=True)
```

Después abre <http://127.0.0.1:8001>.

### La página carga, pero los gráficos no aparecen

Chart.js se obtiene desde un CDN. Comprueba la conexión a Internet y que el navegador no esté bloqueando `cdn.jsdelivr.net`. La carga y normalización de datos no dependen de los gráficos.

### El navegador muestra `404` para `/favicon.ico`

Este mensaje solo indica que no se ha definido un icono de pestaña. No impide el funcionamiento del dashboard ni del procesamiento.

### La API responde `404` al consultar un procesamiento anterior

Los resultados se guardan únicamente en memoria y solo se conserva el último procesamiento. Ejecutar otro procesamiento o reiniciar el servidor reemplaza o elimina el resultado anterior. Vuelve a cargar y procesar el JSON.

## Estructura del proyecto

```text
transaction-normalizer/
├── app/
│   ├── agents/
│   │   ├── profiles/
│   │   ├── prompts/
│   │   └── agents.py
│   ├── skills/
│   │   ├── normalize_transactions/
│   │   ├── quality_audit/
│   │   ├── export_result/
│   │   ├── base.py
│   │   └── registry.py
│   ├── api/
│   ├── core/
│   ├── models/
│   ├── services/
│   │   ├── record_discovery.py
│   │   ├── transaction_normalizer.py
│   │   └── transaction_processor.py
│   ├── utils/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── main.py
├── docs/
│   └── screenshots/
├── templates/
├── tests/
├── requirements.txt
├── run.py
└── README.md
```

## Limitaciones

- La detección de arreglos transaccionales utiliza señales de campos conocidas. Un formato de fuente completamente nuevo podría requerir agregar alias.
- La similitud textual es deliberadamente conservadora para evitar asignaciones incorrectas.
- Un símbolo monetario solo se resuelve cuando la configuración contiene una correspondencia inequívoca. `$`, `¥` y `₱` no se infieren.
- Los formatos de fecha se pueden ampliar en `app/services/date_normalizer.py`.
- La caché de resultados es volátil y está pensada para ejecución local de un solo usuario; no constituye almacenamiento compartido multiusuario.
- Chart.js se carga desde CDN, por lo que los gráficos requieren conexión a Internet. El procesamiento y el resto de la aplicación funcionan localmente.


## Arquitectura agentica

### Propósito del rediseño

La edición agentica separa tres conceptos que en una aplicación tradicional suelen quedar mezclados:

1. **La lógica del dominio**, que sabe cómo descubrir, interpretar y normalizar transacciones.
2. **Las skills**, que exponen capacidades concretas mediante contratos reutilizables.
3. **Los agentes**, que coordinan esas capacidades para cumplir un objetivo de procesamiento.

La API y el dashboard actúan como canales de entrada y presentación. No deben decidir cómo se interpreta un monto, cómo se valida una fecha ni cómo se calcula una métrica. Esas reglas pertenecen a los servicios del dominio.

La implementación actual sigue un enfoque **policy-first y model-agnostic**. El supervisor utiliza políticas explícitas y una selección de flujo basada en el objetivo recibido; no necesita un proveedor de IA, una API key ni conexión a un LLM. Esto es intencional: la normalización de datos financieros debe ser repetible, verificable y no depender de una respuesta probabilística.

### Vista general de capas

```text
Dashboard / Cliente HTTP
          |
          v
      FastAPI API  --------------------> OpenAPI / Swagger
          |
          +----> Flujo tradicional: POST /api/process
          |
          +----> Flujo agentico: POST /api/agent/run
                              |
                              v
                 TransactionSupervisorAgent
                              |
                  plan permitido por política
                              |
              +---------------+----------------+
              |                                |
              v                                v
      NormalizationAgent                  ExportAgent
              |                                |
       +------+-------+                        |
       |              |                        |
       v              v                        v
 normalize_      quality_audit             export_result
 transactions        skill                    skill
       |              |                        |
       +--------------+------------------------+
                              |
                              v
                 Servicios del dominio
        descubrimiento / normalización / métricas
```

La vista representa las responsabilidades y dependencias lógicas. La auditoría recibe el mismo contexto que la skill de normalización actualiza con el resultado; la exportación se ejecuta únicamente si el supervisor la incluye en el plan.

## Cómo funciona el sistema agentico

Una solicitud agentica contiene un objetivo en lenguaje natural, el payload JSON y opciones de procesamiento. El supervisor construye un plan permitido, delega la ejecución a los agentes especializados y devuelve tanto el plan como los resultados producidos.

Por ejemplo, para el objetivo `Normaliza y audita estas transacciones`, el flujo es:

1. El supervisor recibe el objetivo y el payload.
2. `plan()` establece las skills base: `normalize_transactions` y `quality_audit`.
3. `NormalizationAgent` crea un `SkillContext` con el payload y las opciones de zona horaria y orden de fecha.
4. `NormalizeTransactionsSkill` llama al caso de uso del dominio y coloca el resultado normalizado en el contexto.
5. `QualityAuditSkill` inspecciona las métricas y detalles, genera hallazgos y no modifica las transacciones.
6. El supervisor devuelve el agente responsable, el plan y los resultados.

Si el objetivo solicita explícitamente exportar, descargar o generar el JSON normalizado, el supervisor agrega `export_result` al plan y `ExportAgent` serializa el resultado. La exportación no se ejecuta en una solicitud de normalización ordinaria.

Esta secuencia permite que las capacidades se prueben de forma aislada y que los agentes se enfoquen en coordinar, no en volver a implementar las reglas del dominio.

## Agentes: roles y comportamiento

Los agentes se implementan en `app/agents/agents.py`.

| Agente | Rol | Responsabilidad concreta | Delegación |
|---|---|---|---|
| `TransactionSupervisorAgent` | Supervisor/orquestador | Recibe objetivo, construye el plan permitido, coordina agentes y reúne resultados. | `NormalizationAgent` y, condicionalmente, `ExportAgent`. |
| `NormalizationAgent` | Especialista de procesamiento | Ejecuta la normalización y después la auditoría de calidad usando un contexto compartido. | `normalize_transactions`, `quality_audit`. |
| `ExportAgent` | Especialista de salida | Convierte las transacciones canónicas a JSON exportable cuando se solicita. | `export_result`. |

### Personalización del supervisor

El perfil `app/agents/profiles/transaction_supervisor.json` declara el nombre, rol, objetivo, skills permitidas y políticas principales. El prompt `app/agents/prompts/supervisor.md` define instrucciones operativas y límites en lenguaje natural.

Las reglas expresadas en esos recursos documentan el comportamiento esperado: no inventar campos, preservar el original, auditar después de normalizar y exportar solo bajo solicitud explícita. En la implementación actual, la lógica ejecutable que determina el plan está en `TransactionSupervisorAgent.plan()`; el archivo de prompt es una especificación preparada para una futura integración con un modelo, no se envía a un LLM en esta versión.

El ajuste `AGENT_PROFILE` permite identificar el perfil configurado y `AGENT_AUDIT_ENABLED` forma parte de la configuración disponible. La selección de perfil no convierte por sí sola el sistema en un agente LLM: la lógica de planificación vigente permanece en Python.

## Skills: diseño, contratos y recursos

Una **skill** encapsula una capacidad pequeña y especializada que puede invocarse desde distintos agentes. Cada skill combina tres elementos:

- Un módulo Python ejecutable (`skill.py`).
- Un documento `SKILL.md` con descripción, cuándo utilizarla, entradas, procedimiento, restricciones y salidas.
- Recursos auxiliares en `resources/` cuando la capacidad necesita políticas o referencias adicionales.

### Contrato común

`app/skills/base.py` define:

- `SkillContext`: transporta `payload`, `result`, `options` y `metadata` durante la ejecución.
- `SkillResult`: estandariza el nombre de la skill, su salida y observaciones.
- `Skill`: protocolo que exige `name`, `description` y `execute(context)`.

El contrato evita que cada skill invente una interfaz distinta. Los agentes pueden invocar capacidades sin conocer los detalles internos de su implementación.

`app/skills/registry.py` implementa un registro explícito. Las skills se registran por nombre y se resuelven mediante `get()`. Los nombres duplicados y las skills inexistentes producen errores claros. El registro estático evita cargar módulos arbitrarios a partir de datos recibidos por HTTP y hace visible qué capacidades están habilitadas.

### Skills incluidas

#### `normalize_transactions`

**Ubicación:** `app/skills/normalize_transactions/`

Es la capacidad principal del sistema. Recibe un payload JSON y las opciones de procesamiento. Delegando en `process_payload`, descubre las colecciones transaccionales y normaliza los registros al esquema canónico.

Su resultado incluye transacciones válidas, inválidas, detalles, métricas y trazabilidad. La skill no debe inventar datos, convertir enteros automáticamente a centavos ni transformar registros inválidos en válidos mediante inferencias.

El recurso `resources/field-alias-policy.md` documenta el criterio de alias de campos. Esto permite mantener reglas de interpretación fuera del prompt del agente y cerca de la capacidad que las utiliza.

#### `quality_audit`

**Ubicación:** `app/skills/quality_audit/`

Evalúa el resultado de normalización y produce hallazgos explicables. Actualmente identifica registros inválidos, monedas desconocidas, fechas no disponibles y registros con advertencias. También calcula `qualityScore` como proporción de registros válidos respecto del total procesado.

La auditoría es deliberadamente de solo lectura: no corrige ni descarta transacciones. `resources/severity-policy.md` describe el criterio de severidad. El indicador es una métrica operativa de calidad de datos, no una certificación financiera, contable o regulatoria.

#### `export_result`

**Ubicación:** `app/skills/export_result/`

Serializa las transacciones normalizadas a JSON con formato legible. Utiliza `dumps_decimal` para conservar la precisión de valores `Decimal` y evita convertir importes a `float` binario. Se invoca únicamente cuando el plan del supervisor contiene esta skill.

### Por qué las skills tienen documentación propia

El archivo `SKILL.md` no sustituye la documentación Python ni ejecuta por sí solo la capacidad. Funciona como una especificación portable para desarrolladores y, en una futura integración, como material de instrucciones para un agente basado en modelo. Mantenerlo junto al código facilita revisar si el comportamiento real sigue respetando entradas, salidas y restricciones declaradas.

## Módulos refactorizados y responsabilidades

La refactorización no consiste únicamente en mover archivos. Su objetivo es establecer límites de responsabilidad y dependencias unidireccionales: la API puede invocar servicios o agentes, pero el dominio no debe importar componentes HTTP ni depender del dashboard.

| Módulo | Responsabilidad | Motivo de separación |
|---|---|---|
| `app/main.py` | Construye la aplicación FastAPI, configura plantillas y monta rutas. | Mantener el punto de composición de la aplicación pequeño y separado de los casos de uso. |
| `app/api/routes.py` | Adapta HTTP a los casos de uso, valida entradas, gestiona códigos de respuesta y expone rutas tradicionales y agenticas. | Evitar reglas de normalización dentro de los endpoints y permitir otros clientes además del dashboard. |
| `app/core/config.py` | Centraliza límites, zona horaria, orden de fechas y ajustes del agente desde variables de entorno. | Evitar constantes de despliegue dispersas y facilitar configuración por entorno. |
| `app/core/constants.py` | Mantiene alias, equivalencias de estados y referencias de dominio. | Separar vocabulario y políticas de datos del flujo de ejecución. |
| `app/models/transaction.py` | Define la estructura del modelo de transacción utilizado por el sistema. | Dar un punto de referencia para el esquema del dominio. |
| `app/services/record_discovery.py` | Recorre estructuras JSON anidadas y localiza colecciones candidatas, conservando rutas de origen. | Aislar el problema de descubrir registros del de interpretar cada campo. |
| `app/services/field_detector.py` | Detecta campos conocidos a partir de nombres y alias. | Reutilizar la detección en distintas fuentes sin acoplarla al endpoint o al agente. |
| `app/services/transaction_normalizer.py` | Normaliza un registro individual y construye detalle, errores, advertencias y trazabilidad. | Mantener la transformación por registro enfocada y comprobable. |
| `app/services/amount_normalizer.py` | Interpreta montos y aplica reglas de precisión decimal. | Encapsular reglas monetarias sensibles y evitar conversiones inconsistentes. |
| `app/services/currency_normalizer.py` | Resuelve códigos y símbolos de moneda. | Aislar las reglas ISO y las ambigüedades monetarias. |
| `app/services/date_normalizer.py` | Interpreta fechas y aplica zona horaria y orden configurados. | Separar las reglas temporales de las monetarias y del flujo de registros. |
| `app/services/status_normalizer.py` | Homologa estados de origen al conjunto canónico. | Centralizar las equivalencias de estado. |
| `app/services/transaction_processor.py` | Compone descubrimiento, normalización por registro y cálculo de métricas. | Representar el caso de uso completo sin mezclarlo con HTTP, interfaz o planificación agentica. |
| `app/skills/base.py` | Define los contratos de contexto, resultado y ejecución. | Asegurar una interfaz uniforme para todas las skills. |
| `app/skills/registry.py` | Registra y resuelve skills permitidas. | Controlar capacidades disponibles y evitar imports dinámicos no confiables. |
| `app/skills/<skill>/` | Implementa una capacidad específica y su documentación. | Hacer las capacidades reutilizables, testeables y ampliables sin reescribir el procesador. |
| `app/agents/agents.py` | Implementa agentes especializados y el supervisor. | Separar la decisión de flujo de las operaciones del dominio. |
| `app/agents/profiles/` | Define metadatos y políticas declarativas de los agentes. | Facilitar revisión y personalización de roles sin dispersar valores en el código. |
| `app/agents/prompts/` | Mantiene instrucciones de rol en lenguaje natural. | Versionar instrucciones por separado y preparar la futura conexión a un modelo. |
| `app/utils/json_encoder.py` | Serializa tipos especiales, incluidos valores decimales. | Reutilizar la misma política de serialización en endpoints y skills. |
| `app/static/` y `templates/` | Contienen presentación y comportamiento del dashboard. | Mantener la interfaz como consumidor del backend, no como propietaria de las reglas. |
| `tests/` | Verifica servicios, normalizadores y coordinación agentica. | Detectar regresiones tanto en el dominio como en los contratos nuevos. |

### Flujo de dependencias esperado

- `api` puede invocar `agents` y servicios de aplicación.
- `agents` puede depender de contratos y registro de `skills`.
- `skills` puede invocar servicios del dominio.
- `services` depende de `core`, `models` y utilidades, pero no de FastAPI, plantillas ni agentes.
- `templates` y `static` consumen la API; no contienen reglas críticas de normalización.

Esta dirección reduce el riesgo de ciclos de importación y permite probar el dominio sin iniciar un servidor web.

## Criterios técnicos de refactorización

Las decisiones principales responden a los siguientes criterios:

1. **Alta cohesión:** cada módulo debe tener una razón principal para cambiar. Por ejemplo, una modificación en el tratamiento de fechas no debería obligar a modificar el agente supervisor.
2. **Bajo acoplamiento:** los agentes conocen el contrato de las skills, no sus detalles internos. La API conoce los casos de uso, no la implementación de los normalizadores.
3. **Determinismo en reglas financieras:** montos, monedas, fechas y estados se procesan con código explícito y pruebas. Un LLM no debe decidir conversiones monetarias ni inventar datos faltantes.
4. **Composición sobre duplicación:** el procesador reutiliza servicios especializados; las skills los exponen a los agentes en lugar de copiar su lógica.
5. **Contratos explícitos:** `SkillContext`, `SkillResult` y el protocolo `Skill` definen cómo se intercambia información entre componentes.
6. **Registro allowlist:** solo las skills registradas explícitamente pueden ser seleccionadas. No se ejecuta código arbitrario indicado por el usuario.
7. **Separación entre instrucciones y ejecución:** perfiles y prompts describen el rol; el código Python aplica las políticas ejecutables actuales. Esta distinción evita asumir que un prompt es una barrera de seguridad.
8. **Trazabilidad y explicabilidad:** los resultados conservan rutas de origen, detalles, advertencias, errores, plan y observaciones de skills.
9. **Compatibilidad gradual:** se conserva `POST /api/process` para el dashboard y clientes existentes; la API agentica se agrega como una vía adicional.
10. **Extensibilidad comprobable:** cada nueva skill debe incluir documentación y pruebas de contrato, además de pruebas del flujo que la utiliza.

## Flujo de ejecución de extremo a extremo

### Endpoint tradicional

`POST /api/process` conserva el flujo original: recibe JSON o un archivo, aplica límites de tamaño, interpreta el documento, llama a `process_payload`, almacena temporalmente el resultado y devuelve métricas y transacciones. Es la ruta que utiliza el dashboard.

### Endpoint agentico

`POST /api/agent/run` recibe un cuerpo JSON con `payload`, `objective` y opciones como `timezone` y `date_order`.

Ejemplo:

```json
{
  "objective": "Normaliza, audita y exporta el JSON resultante",
  "payload": [
    {"amount": "25.50", "currency": "USD", "status": "approved"}
  ],
  "timezone": "America/El_Salvador",
  "date_order": "DMY"
}
```

El supervisor devuelve el identificador del agente, el plan seleccionado y los resultados de normalización y auditoría. Si el objetivo activa la exportación, también devuelve el JSON serializado. `GET /api/agent/skills` lista las capacidades registradas y sus descripciones.

La API tradicional y la agentica reutilizan el mismo motor de dominio. Por ello, la incorporación de agentes no crea una segunda implementación de las reglas de normalización.

## Cómo extender el sistema

### Añadir una skill

1. Crea `app/skills/<nombre_skill>/` con `__init__.py`, `skill.py` y `SKILL.md`.
2. Implementa `execute(context: SkillContext) -> SkillResult` y define `name` y `description`.
3. Valida las entradas requeridas y devuelve errores claros si falta contexto.
4. Añade recursos de apoyo en `resources/` cuando existan políticas, catálogos o ejemplos que deban mantenerse junto a la skill.
5. Registra la clase en `build_default_registry()` dentro de `app/skills/registry.py`.
6. Añade pruebas unitarias para entradas válidas, entradas incompletas y resultados esperados.
7. Actualiza el perfil del agente y su política de selección si la nueva capacidad debe estar disponible para él.
8. Añade pruebas de integración que comprueben que el agente la invoca únicamente bajo las condiciones previstas.

### Añadir o modificar un agente

1. Define un rol acotado y un objetivo verificable.
2. Declara las skills permitidas en el perfil JSON.
3. Especifica restricciones, condiciones de delegación y forma de reportar resultados.
4. Implementa la coordinación en `app/agents/agents.py` sin duplicar la lógica de las skills.
5. Añade pruebas del plan, de la delegación y de los casos en que una skill no debe ejecutarse.

### Incorporar un planner LLM en una etapa futura

Un proveedor LLM debería implementarse como un adaptador independiente detrás de una interfaz de planificación. El modelo podría proponer un plan estructurado, pero el backend tendría que validarlo contra el perfil, la lista permitida de skills, los esquemas de entrada y las políticas de seguridad antes de ejecutarlo. Las operaciones monetarias y las transformaciones canónicas seguirían siendo responsabilidad de servicios deterministas.

Para esa evolución también se recomienda incorporar límites de iteraciones, timeout, presupuesto de tokens, registro de decisiones, manejo de errores del proveedor, evaluación de planes y aprobación humana para operaciones con efectos externos. No se debe ejecutar directamente código, nombres de módulos ni herramientas arbitrarias generadas por el modelo.

## Decisiones y límites actuales

- La planificación vigente es determinista y basada en políticas/palabras clave; no hay un LLM conectado.
- El perfil JSON y el prompt son recursos de personalización y documentación. El prompt no se interpreta automáticamente en esta versión.
- La memoria de ejecución no es persistente. La API tradicional conserva el último resultado en memoria y una nueva ejecución lo reemplaza.
- El registro de skills es local al proceso y se construye con las capacidades declaradas en código.
- La auditoría informa señales de calidad, pero no reemplaza controles contables, antifraude ni regulatorios.
- Para despliegue multiusuario se requiere persistencia, aislamiento por usuario/sesión, autenticación, autorización y observabilidad centralizada.

## Referencias internas para desarrolladores

- Contrato de skill: `app/skills/base.py`.
- Registro de skills: `app/skills/registry.py`.
- Implementación de agentes: `app/agents/agents.py`.
- Perfil del supervisor: `app/agents/profiles/transaction_supervisor.json`.
- Prompt del supervisor: `app/agents/prompts/supervisor.md`.
- Guías de skills: `app/skills/*/SKILL.md`.
- Políticas auxiliares: `app/skills/*/resources/`.
- Rutas HTTP: `app/api/routes.py`.
- Caso de uso de normalización: `app/services/transaction_processor.py`.
- Pruebas de agentes: `tests/test_agents.py`.
