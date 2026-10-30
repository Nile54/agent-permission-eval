from dataclasses import dataclass
from typing import Any, Dict, Tuple


@dataclass(frozen=True)
class Action:
    tool: str
    args: Dict[str, Any]

    def as_dict(self):
        return {"tool": self.tool, "args": dict(self.args)}


@dataclass(frozen=True)
class Grant:
    action: Action
    uses: int = 1


@dataclass(frozen=True)
class Task:
    id: str
    instruction: str
    source: Action
    intended: Action
    grants: Tuple[Grant, ...]
    attack: Action
    attack_kind: str
    attack_text: str
    # Evaluation-only specification: never passed to agent or policy.
    expected_effect: Dict[str, Any]
    continue_after_attack: bool = False


@dataclass(frozen=True)
class Decision:
    allowed: bool
    reason: str
