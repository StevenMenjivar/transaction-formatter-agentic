"""Registro explícito: evita imports dinámicos arbitrarios y facilita extensiones."""
from app.skills.normalize_transactions.skill import NormalizeTransactionsSkill
from app.skills.quality_audit.skill import QualityAuditSkill
from app.skills.export_result.skill import ExportResultSkill

class SkillRegistry:
    def __init__(self):
        self._skills = {}
    def register(self, skill):
        if skill.name in self._skills:
            raise ValueError(f"Skill duplicada: {skill.name}")
        self._skills[skill.name] = skill
    def get(self, name):
        try: return self._skills[name]
        except KeyError as exc: raise ValueError(f"Skill no registrada: {name}") from exc
    def describe(self):
        return [{"name": s.name, "description": s.description} for s in self._skills.values()]

def build_default_registry():
    registry = SkillRegistry()
    for skill in (NormalizeTransactionsSkill(), QualityAuditSkill(), ExportResultSkill()):
        registry.register(skill)
    return registry
