"""Auditoría explicable de calidad sobre el resultado de normalización."""
from app.skills.base import SkillContext, SkillResult

class QualityAuditSkill:
    name = "quality_audit"
    description = "Resume anomalías, advertencias y métricas sin alterar transacciones."
    def execute(self, context: SkillContext) -> SkillResult:
        result = context.result
        if not result: raise ValueError("La auditoría requiere un resultado normalizado.")
        metrics = result["metrics"]
        findings = []
        if metrics.get("invalid", 0): findings.append({"severity":"warning", "code":"INVALID_RECORDS", "count":metrics["invalid"], "message":"Hay registros que no pudieron normalizarse."})
        if metrics.get("unknownCurrency", 0): findings.append({"severity":"warning", "code":"UNKNOWN_CURRENCY", "count":metrics["unknownCurrency"], "message":"Existen transacciones sin moneda identificable."})
        if metrics.get("unavailableDates", 0): findings.append({"severity":"info", "code":"MISSING_DATES", "count":metrics["unavailableDates"], "message":"Existen transacciones sin fecha normalizada."})
        warning_records = sum(1 for item in result.get("details", []) if item.get("warnings"))
        if warning_records: findings.append({"severity":"info", "code":"FIELD_WARNINGS", "count":warning_records, "message":"Hay registros válidos con advertencias o conflictos de campos."})
        output = {"findings":findings, "qualityScore": round(100 * metrics["valid"] / metrics["processed"], 2) if metrics["processed"] else 0, "checked":metrics["processed"]}
        return SkillResult(self.name, output, [f"Auditoría completada: {len(findings)} hallazgos."])
