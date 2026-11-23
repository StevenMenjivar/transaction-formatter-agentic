"""Skill de serialización para exportaciones reutilizables."""
from app.skills.base import SkillContext, SkillResult
from app.utils.json_encoder import dumps_decimal

class ExportResultSkill:
    name = "export_result"
    description = "Serializa las transacciones normalizadas a JSON conservando decimales."
    def execute(self, context: SkillContext) -> SkillResult:
        if not context.result: raise ValueError("La exportación requiere un resultado normalizado.")
        return SkillResult(self.name, {"json":dumps_decimal(context.result["transactions"], indent=2), "count":len(context.result["transactions"])})
