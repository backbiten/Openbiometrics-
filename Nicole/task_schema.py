"""Nicole task schema.

Nicole is an orchestrator that turns requirements into bounded tasks.
This module defines the minimal JSON schema for a task plus a scoped
capability token ("coin bits").

Design goals:
- No network access
- No secret storage
- Deterministic validation
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


class TaskValidationError(ValueError):
    pass


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class CoinBitsToken:
    """A scoped capability token that authorizes a task.

    This is intentionally simple and dependency-free.
    """

    token_id: str
    issued_at: str  # ISO-8601
    expires_at: str  # ISO-8601
    allowed_paths: List[str]
    allowed_ops: List[str]  # e.g. ["read", "plan", "propose_patch"]

    def validate(self) -> None:
        if not self.token_id.strip():
            raise TaskValidationError("token_id must be non-empty")
        if not self.allowed_paths:
            raise TaskValidationError("allowed_paths must be non-empty")
        if not self.allowed_ops:
            raise TaskValidationError("allowed_ops must be non-empty")

        try:
            issued = datetime.fromisoformat(self.issued_at.replace("Z", "+00:00"))
            expires = datetime.fromisoformat(self.expires_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise TaskValidationError(f"invalid issued_at/expires_at datetime: {exc}") from exc

        if expires <= issued:
            raise TaskValidationError("expires_at must be after issued_at")
        if expires <= _utcnow():
            raise TaskValidationError("token is expired")


@dataclass(frozen=True)
class NicoleTask:
    """A task Nicole hands to an executor AI."""

    task_id: str
    title: str
    description: str
    token: CoinBitsToken
    inputs: Dict[str, Any]
    acceptance_criteria: List[str]

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "NicoleTask":
        try:
            token_dict = data["token"]
            token = CoinBitsToken(**token_dict)
            token.validate()

            task = NicoleTask(
                task_id=str(data["task_id"]),
                title=str(data.get("title", "")),
                description=str(data.get("description", "")),
                token=token,
                inputs=dict(data.get("inputs", {})),
                acceptance_criteria=list(data.get("acceptance_criteria", [])),
            )
        except KeyError as exc:
            raise TaskValidationError(f"missing required field: {exc}") from exc
        except TypeError as exc:
            raise TaskValidationError(f"invalid field types: {exc}") from exc

        if not task.task_id.strip():
            raise TaskValidationError("task_id must be non-empty")
        if not task.title.strip():
            raise TaskValidationError("title must be non-empty")
        if not task.description.strip():
            raise TaskValidationError("description must be non-empty")
        if not task.acceptance_criteria:
            raise TaskValidationError("acceptance_criteria must be non-empty")

        return task
