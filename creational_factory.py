"""Creational Design Pattern: Factory."""

from __future__ import annotations

from typing import Any, Dict

from .behavioral_command import AlgorithmCommand, Command
from .structural_facade import AlgorithmsFacade


class CommandFactory:
    def __init__(self, facade: AlgorithmsFacade) -> None:
        self.facade = facade

    def create(self, algorithm_name: str, params: Dict[str, Any]) -> Command:
        return AlgorithmCommand(facade=self.facade, name=algorithm_name, params=params)
