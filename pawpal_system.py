from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional
from uuid import uuid4


@dataclass
class Pet:
    name: str
    species: str
    age_years: int
    notes: Optional[str] = None

    def profile_summary(self) -> str:
        raise NotImplementedError()


@dataclass
class Task:
    task_id: str = field(default_factory=lambda: str(uuid4()))
    title: str
    duration_minutes: int
    priority: int
    pet_name: Optional[str] = None
    due_date: Optional[date] = None
    notes: Optional[str] = None

    def is_due_today(self, today: date) -> bool:
        raise NotImplementedError()


@dataclass
class Owner:
    name: str
    time_available_minutes: int
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError()

    def remove_pet(self, pet_name: str) -> None:
        raise NotImplementedError()


class Planner:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        raise NotImplementedError()

    def edit_task(self, task_id: str, updated_task: Task) -> None:
        raise NotImplementedError()

    def generate_daily_plan(self, today: date) -> List[Task]:
        raise NotImplementedError()
