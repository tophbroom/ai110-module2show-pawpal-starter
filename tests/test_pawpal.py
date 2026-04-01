from datetime import time

from pawpal_system import Pet, Task


def test_task_completion_updates_status() -> None:
    task = Task(description="Grooming", scheduled_time=time(9, 0), frequency="weekly")
    task.mark_complete()

    assert task.is_complete is True


def test_pet_add_task_increases_count() -> None:
    pet = Pet(name="Luna", species="Dog", age_years=4)

    pet.add_task(Task(description="Walk", scheduled_time=time(7, 0), frequency="daily"))

    assert len(pet.tasks) == 1
