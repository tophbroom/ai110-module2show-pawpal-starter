from __future__ import annotations

from dataclasses import dataclass, field
from datetime import time
from typing import List, Optional


@dataclass
class Task:
    description: str
    scheduled_time: time
    frequency: str
    is_complete: bool = False
    notes: Optional[str] = None

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_complete = True

    def mark_incomplete(self) -> None:
        """Mark the task as not completed."""
        self.is_complete = False

    def format_for_schedule(self) -> str:
        """Return a readable schedule line for this task."""
        status = "done" if self.is_complete else "todo"
        time_str = self.scheduled_time.strftime("%I:%M %p").lstrip("0")
        return f"{time_str} - {self.description} ({self.frequency}, {status})"


@dataclass
class Pet:
    name: str
    species: str
    age_years: int
    tasks: List[Task] = field(default_factory=list)
    notes: Optional[str] = None

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def remove_task(self, description: str) -> None:
        """Remove the first task matching a description."""
        self.tasks = [task for task in self.tasks if task.description != description]

    def list_tasks(self) -> List[Task]:
        """Return a list of this pet's tasks."""
        return list(self.tasks)


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)
    preferences: List[str] = field(default_factory=list)
    time_available_minutes: Optional[int] = None

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner profile."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> None:
        """Remove a pet by name from the owner profile."""
        self.pets = [pet for pet in self.pets if pet.name != pet_name]

    def get_all_tasks(self) -> List[Task]:
        """Return a flattened list of tasks across all pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for the given owner."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across the owner's pets."""
        return self.owner.get_all_tasks()

    def build_daily_schedule(self) -> List[Task]:
        """Return tasks sorted by scheduled time for today."""
        tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda task: task.scheduled_time)
