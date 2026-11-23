from app.agents.agents import TransactionSupervisorAgent
from app.skills.registry import build_default_registry
from app.skills.base import SkillContext

def test_registry_exposes_skills():
    names = {item["name"] for item in build_default_registry().describe()}
    assert names == {"normalize_transactions", "quality_audit", "export_result"}

def test_supervisor_plans_export_only_when_requested():
    agent = TransactionSupervisorAgent()
    assert agent.plan("normalizar y auditar") == ["normalize_transactions", "quality_audit"]
    assert agent.plan("normalizar y exportar JSON")[-1] == "export_result"

def test_supervisor_runs_normalization_and_audit():
    agent = TransactionSupervisorAgent()
    result = agent.run([{"amount":"12.50", "currency":"USD", "status":"approved"}])
    assert result.agent == "transaction_supervisor"
    assert result.results["normalization"]["metrics"]["valid"] == 1
    assert result.results["quality"]["qualityScore"] == 100.0

def test_supervisor_optional_export():
    result = TransactionSupervisorAgent().run([{"amount":10}], "exportar JSON")
    assert "export" in result.results
    assert result.results["export"]["count"] == 1
