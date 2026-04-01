from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, time, timedelta
from typing import List, Optional


@dataclass
class Task:
    description: str
    scheduled_time: time
    frequency: str
    due_date: date = field(default_factory=date.today)
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

    def next_occurrence(self) -> Optional["Task"]:
        """Create the next occurrence for recurring tasks."""
        if self.frequency == "daily":
            next_date = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = self.due_date + timedelta(days=7)
        else:
            return None

        return Task(
            description=self.description,
            scheduled_time=self.scheduled_time,
            frequency=self.frequency,
            due_date=next_date,
            notes=self.notes,
        )


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

    def tasks_for_date(self, for_date: date) -> List[Task]:
        """Return tasks scheduled for a specific date."""
        return [task for task in self.tasks if task.due_date == for_date]


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

    def get_tasks_for_date(self, for_date: date) -> List[Task]:
        """Return all tasks across pets scheduled for a date."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks_for_date(for_date))
        return tasks

    def find_pet(self, pet_name: str) -> Optional[Pet]:
        """Return a pet by name if present."""
        for pet in self.pets:
            if pet.name == pet_name:
                return pet
        return None


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for the given owner."""
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Return tasks sorted by their scheduled time."""
        return sorted(tasks, key=lambda task: task.scheduled_time)

    def filter_tasks(
        self,
        pet_name: Optional[str] = None,
        status: Optional[str] = None,
        for_date: Optional[date] = None,
    ) -> List[Task]:
        """Filter tasks by pet, completion status, or date."""
        tasks = self.owner.get_all_tasks()
        if pet_name:
            tasks = [task for pet in self.owner.pets if pet.name == pet_name for task in pet.tasks]
        if for_date:
            tasks = [task for task in tasks if task.due_date == for_date]
        if status == "complete":
            tasks = [task for task in tasks if task.is_complete]
        elif status == "incomplete":
            tasks = [task for task in tasks if not task.is_complete]
        return tasks

    def build_daily_schedule(self, for_date: Optional[date] = None) -> List[Task]:
        """Return tasks sorted by time for a given date."""
        if for_date is None:
            for_date = date.today()
        tasks = self.owner.get_tasks_for_date(for_date)
        return self.sort_by_time(tasks)

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return warnings for tasks that share the same time."""
        warnings: List[str] = []
        seen: dict[time, List[Task]] = {}
        for task in tasks:
            seen.setdefault(task.scheduled_time, []).append(task)

        for scheduled_time, grouped in seen.items():
            if len(grouped) > 1:
                time_str = scheduled_time.strftime("%I:%M %p").lstrip("0")
                descriptions = ", ".join(task.description for task in grouped)
                warnings.append(f"Conflict at {time_str}: {descriptions}")
        return warnings

    def mark_task_complete(self, pet_name: str, description: str) -> Optional[Task]:
        """Mark a task complete and return a new recurring task if created."""
        pet = self.owner.find_pet(pet_name)
        if not pet:
            return None

        for task in pet.tasks:
            if task.description == description and not task.is_complete:
                task.mark_complete()
                next_task = task.next_occurrence()
                if next_task:
                    pet.add_task(next_task)
                return next_task
        return None
