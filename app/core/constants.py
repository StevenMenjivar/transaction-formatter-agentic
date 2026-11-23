FIELD_ALIASES = {
    "amount": {
        "total": 0, "transactiontotal": 0, "totalamount": 0, "totaltransaccion": 0,
        "amount": 10, "transactionamount": 10, "monto": 10, "montotransaccion": 10,
        "importe": 15, "importetotal": 15, "valortransaccion": 20, "valor": 25,
    },
    "currency": {
        "currency": 0, "currencycode": 0, "transactioncurrency": 5,
        "moneda": 0, "codigomoneda": 0, "monedatransaccion": 5, "divisa": 10,
    },
    "transactionDate": {
        "transactiondate": 0, "transactiondatetime": 0, "date": 5, "createdat": 5,
        "created": 10, "timestamp": 10, "operationdate": 10, "fecha": 5,
        "fechatransaccion": 0, "fechaoperacion": 5, "fechacreacion": 10,
        "fecharegistro": 10, "datecreated": 10,
    },
    "status": {
        "transactionstatus": 0, "status": 5, "state": 10, "result": 10,
        "responsestatus": 15, "estadotransaccion": 0, "estado": 5,
        "resultado": 10, "estadooperacion": 10,
    },
    "originalReference": {
        "transactionid": 0, "transactionreference": 5, "transactionref": 5,
        "referenceid": 10, "reference": 15, "ref": 20, "idtransaccion": 0,
        "codigotransaccion": 5, "referenciatransaccion": 5, "referencia": 15,
        "id": 25,
    },
    "concept": {
        "concept": 0, "transactionconcept": 0, "description": 5,
        "transactiondescription": 5, "detail": 10, "details": 10,
        "purpose": 10, "memo": 10, "concepto": 0, "descripcion": 5,
        "detalle": 10, "motivo": 10, "glosa": 10,
    },
}

STATUS_MAP = {
    "SUCCESS": {
        "success", "ok", "completed", "processed", "approved", "applied",
        "processed successfully", "exitosa", "exitoso", "aprobada", "aprobado",
        "procesada", "procesado", "aplicada", "aplicado", "successful",
    },
    "FAILED": {
        "failed", "failure", "error", "rejected", "declined", "not processed",
        "fallida", "fallido", "rechazada", "rechazado", "no procesada", "no procesado",
    },
    "PENDING": {
        "pending", "processing", "in process", "in progress", "waiting", "under review",
        "pendiente", "en proceso", "en espera", "en revision",
    },
}

CURRENCY_SYMBOLS = {
    "€": "EUR", "£": "GBP", "¥": None, "￥": None,
    "₡": "CRC", "₲": "PYG", "₱": None, "₹": "INR",
    "₩": "KRW", "₺": "TRY", "₽": "RUB", "฿": "THB",
}
