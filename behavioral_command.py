"""Behavioral Design Pattern: Command."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict

from .structural_facade import AlgorithmsFacade


class Command:
    def execute(self) -> str:
        raise NotImplementedError


@dataclass
class AlgorithmCommand(Command):
    facade: AlgorithmsFacade
    name: str
    params: Dict[str, Any]

    def execute(self) -> str:
        return self.facade.run(self.name, self.params)
