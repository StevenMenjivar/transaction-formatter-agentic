"""Agentes especializados y supervisor con planificación basada en políticas."""
from dataclasses import dataclass
from app.skills.base import SkillContext
from app.skills.registry import build_default_registry

@dataclass(frozen=True)
class AgentResponse:
    agent: str
    plan: list[str]
    results: dict

class NormalizationAgent:
    name = "normalization_agent"
    def __init__(self, registry): self.registry = registry
    def run(self, payload, options=None):
        ctx = SkillContext(payload=payload, options=options or {})
        normalized = self.registry.get("normalize_transactions").execute(ctx)
        audited = self.registry.get("quality_audit").execute(ctx)
        return AgentResponse(self.name, ["normalize_transactions", "quality_audit"], {"normalization":normalized.output, "quality":audited.output})

class ExportAgent:
    name = "export_agent"
    def __init__(self, registry): self.registry = registry
    def run(self, normalized_result):
        ctx = SkillContext(result=normalized_result)
        exported = self.registry.get("export_result").execute(ctx)
        return AgentResponse(self.name, ["export_result"], {"export":exported.output})

class TransactionSupervisorAgent:
    """Supervisor policy-first. Planner can be replaced without changing skills or API."""
    name = "transaction_supervisor"
    def __init__(self, registry=None):
        self.registry = registry or build_default_registry()
        self.normalizer = NormalizationAgent(self.registry)
        self.exporter = ExportAgent(self.registry)
    def plan(self, objective: str) -> list[str]:
        text = (objective or "normalizar y auditar").lower()
        plan = ["normalize_transactions", "quality_audit"]
        if any(word in text for word in ("exportar", "descargar", "json normalizado", "export")):
            plan.append("export_result")
        return plan
    def run(self, payload, objective="normalizar y auditar", options=None):
        plan = self.plan(objective)
        response = self.normalizer.run(payload, options)
        results = dict(response.results)
        if "export_result" in plan:
            results.update(self.exporter.run(results["normalization"]).results)
        return AgentResponse(self.name, plan, results)
