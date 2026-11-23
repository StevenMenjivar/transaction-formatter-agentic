import json
import uuid
from collections import OrderedDict
from fastapi import APIRouter, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse, Response
from app.utils.json_encoder import dumps_decimal
from app.core.config import settings
from app.services.transaction_processor import process_payload
from app.agents.agents import TransactionSupervisorAgent

router = APIRouter(prefix="/api", tags=["transactions"])
# Volatile in-memory cache only; a new run replaces previous data.
_RESULTS = OrderedDict()

class DecimalJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        return dumps_decimal(content, indent=None).encode("utf-8")


@router.post("/agent/run")
async def run_agent(request: Request):
    """Ejecuta el supervisor agentico: normalización, auditoría y exportación opcional."""
    try:
        body = await request.json()
        if not isinstance(body, dict) or "payload" not in body:
            raise HTTPException(400, "El cuerpo debe incluir la propiedad payload.")
        objective = str(body.get("objective") or "normalizar y auditar")
        options = {"timezone": body.get("timezone") or settings.timezone, "date_order": body.get("date_order") or settings.date_order}
        agent = TransactionSupervisorAgent()
        response = agent.run(body["payload"], objective, options)
        return {"agent": response.agent, "plan": response.plan, **response.results}
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(500, "El agente no pudo completar el flujo solicitado.") from exc

@router.get("/agent/skills")
async def list_agent_skills():
    from app.skills.registry import build_default_registry
    return {"skills": build_default_registry().describe()}

@router.get("/health")
async def health():
    return {"status": "ok", "service": "transaction-normalizer"}

@router.post("/process")
async def process(request: Request):
    content_type = request.headers.get("content-type", "")
    try:
        if "multipart/form-data" in content_type:
            form = await request.form()
            upload = form.get("file")
            raw_text = form.get("json_text")
            timezone_name = form.get("timezone") or settings.timezone
            date_order = form.get("date_order") or settings.date_order
            if upload is not None and hasattr(upload, "read"):
                content = await upload.read(settings.max_file_bytes + 1)
                if len(content) > settings.max_file_bytes:
                    raise HTTPException(413, f"El archivo supera el límite de {settings.max_file_bytes} bytes.")
                try:
                    payload = json.loads(content.decode("utf-8-sig"))
                except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                    raise HTTPException(400, f"El archivo no contiene JSON UTF-8 válido: {exc}") from exc
            elif raw_text:
                if len(raw_text.encode("utf-8")) > settings.max_file_bytes:
                    raise HTTPException(413, "El contenido supera el tamaño máximo permitido.")
                try:
                    payload = json.loads(raw_text)
                except json.JSONDecodeError as exc:
                    raise HTTPException(400, f"JSON inválido en línea {exc.lineno}, columna {exc.colno}: {exc.msg}") from exc
            else:
                raise HTTPException(400, "Debe cargar un archivo JSON o pegar su contenido.")
        else:
            raw = await request.body()
            if len(raw) > settings.max_file_bytes:
                raise HTTPException(413, "El contenido supera el tamaño máximo permitido.")
            try:
                payload = json.loads(raw.decode("utf-8-sig"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise HTTPException(400, f"JSON inválido: {exc}") from exc
            timezone_name, date_order = settings.timezone, settings.date_order
        result = process_payload(payload, timezone_name, date_order)
        processing_id = str(uuid.uuid4())
        _RESULTS.clear()
        _RESULTS[processing_id] = result
        response = {"processingId": processing_id, **result}
        return DecimalJSONResponse(response)
    except HTTPException:
        raise
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    except Exception as exc:
        raise HTTPException(500, "Ocurrió un error interno durante el procesamiento.") from exc

@router.get("/results/{processing_id}")
async def get_results(processing_id: str):
    result = _RESULTS.get(processing_id)
    if result is None:
        raise HTTPException(404, "El resultado no existe o fue reemplazado por un procesamiento posterior.")
    return DecimalJSONResponse({"transactions": result["transactions"]})

@router.get("/export/{processing_id}")
async def export_results(processing_id: str):
    result = _RESULTS.get(processing_id)
    if result is None:
        raise HTTPException(404, "El resultado no existe o fue reemplazado.")
    payload = dumps_decimal(result["transactions"], indent=2)
    return Response(content=payload, media_type="application/json; charset=utf-8", headers={"Content-Disposition": "attachment; filename=transacciones_normalizadas.json"})

@router.get("/metrics/{processing_id}")
async def get_metrics(processing_id: str):
    result = _RESULTS.get(processing_id)
    if result is None:
        raise HTTPException(404, "El resultado no existe o fue reemplazado.")
    return result["metrics"]

@router.get("/transactions/{processing_id}")
async def get_transactions(processing_id: str, kind: str = "valid"):
    result = _RESULTS.get(processing_id)
    if result is None:
        raise HTTPException(404, "El resultado no existe o fue reemplazado.")
    if kind == "valid":
        return DecimalJSONResponse({"items": result["transactions"]})
    if kind == "invalid":
        return {"items": result["invalidTransactions"]}
    raise HTTPException(400, "El parámetro kind debe ser valid o invalid.")

@router.get("/transactions/{processing_id}/{transaction_id}")
async def get_transaction_detail(processing_id: str, transaction_id: int):
    result = _RESULTS.get(processing_id)
    if result is None:
        raise HTTPException(404, "El resultado no existe o fue reemplazado.")
    detail = next((x for x in result["details"] if x["id"] == transaction_id), None)
    if detail is None:
        raise HTTPException(404, "No se encontró la transacción solicitada.")
    transaction = next(x for x in result["transactions"] if x["id"] == transaction_id)
    return DecimalJSONResponse({"original": detail["original"], "normalized": transaction, "trace": detail["trace"], "warnings": detail["warnings"]})
