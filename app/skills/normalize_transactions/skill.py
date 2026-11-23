"""Skill determinista que normaliza payloads JSON multifuente."""
from app.skills.base import SkillContext, SkillResult
from app.services.transaction_processor import process_payload

class NormalizeTransactionsSkill:
    name = "normalize_transactions"
    description = "Detecta registros y los transforma al esquema canónico sin inventar datos."
    def execute(self, context: SkillContext) -> SkillResult:
        if context.payload is None: raise ValueError("La skill requiere un payload JSON.")
        result = process_payload(context.payload, context.options.get("timezone"), context.options.get("date_order"))
        context.result = result
        return SkillResult(self.name, result, ["Normalización determinista completada."])
