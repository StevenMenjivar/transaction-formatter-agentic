"""Contrato mínimo para skills ejecutables y registrables."""
from dataclasses import dataclass, field
from typing import Any, Protocol

@dataclass
class SkillContext:
    payload: Any = None
    result: dict | None = None
    options: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

@dataclass(frozen=True)
class SkillResult:
    skill: str
    output: dict
    observations: list[str] = field(default_factory=list)

class Skill(Protocol):
    name: str
    description: str
    def execute(self, context: SkillContext) -> SkillResult: ...
