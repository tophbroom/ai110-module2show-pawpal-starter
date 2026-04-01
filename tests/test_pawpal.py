from datetime import date, time, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_completion_updates_status() -> None:
    task = Task(description="Grooming", scheduled_time=time(9, 0), frequency="weekly")
    task.mark_complete()

    assert task.is_complete is True


def test_pet_add_task_increases_count() -> None:
    pet = Pet(name="Luna", species="Dog", age_years=4)

    pet.add_task(Task(description="Walk", scheduled_time=time(7, 0), frequency="daily"))

    assert len(pet.tasks) == 1


def test_schedule_sorts_tasks_by_time() -> None:
    owner = Owner(name="Alex")
    pet = Pet(name="Luna", species="Dog", age_years=4)
    today = date.today()

    pet.add_task(
        Task(
            description="Evening walk",
            scheduled_time=time(18, 0),
            frequency="daily",
            due_date=today,
        )
    )
    pet.add_task(
        Task(
            description="Morning walk",
            scheduled_time=time(7, 30),
            frequency="daily",
            due_date=today,
        )
    )
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    schedule = scheduler.build_daily_schedule(today)

    assert [task.description for task in schedule] == ["Morning walk", "Evening walk"]


def test_recurring_task_creates_next_occurrence() -> None:
    owner = Owner(name="Alex")
    pet = Pet(name="Luna", species="Dog", age_years=4)
    owner.add_pet(pet)

    today = date.today()
    pet.add_task(
        Task(
            description="Morning walk",
            scheduled_time=time(7, 30),
            frequency="daily",
            due_date=today,
        )
    )

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete("Luna", "Morning walk")

    assert next_task is not None
    assert next_task.due_date == today + timedelta(days=1)
    assert len(pet.tasks) == 2


def test_conflict_detection_flags_same_time() -> None:
    owner = Owner(name="Alex")
    pet = Pet(name="Luna", species="Dog", age_years=4)
    owner.add_pet(pet)
    today = date.today()

    pet.add_task(
        Task(
            description="Breakfast",
            scheduled_time=time(8, 0),
            frequency="daily",
            due_date=today,
        )
    )
    pet.add_task(
        Task(
            description="Meds",
            scheduled_time=time(8, 0),
            frequency="daily",
            due_date=today,
        )
    )

    scheduler = Scheduler(owner)
    schedule = scheduler.build_daily_schedule(today)
    warnings = scheduler.detect_conflicts(schedule)

    assert len(warnings) == 1
    assert "Conflict at" in warnings[0]


def test_filter_tasks_by_pet_and_status() -> None:
    owner = Owner(name="Alex")
    luna = Pet(name="Luna", species="Dog", age_years=4)
    milo = Pet(name="Milo", species="Cat", age_years=2)
    owner.add_pet(luna)
    owner.add_pet(milo)

    luna.add_task(Task(description="Walk", scheduled_time=time(7, 0), frequency="daily"))
    milo_task = Task(description="Wet food", scheduled_time=time(8, 0), frequency="daily")
    milo_task.mark_complete()
    milo.add_task(milo_task)

    scheduler = Scheduler(owner)
    luna_tasks = scheduler.filter_tasks(pet_name="Luna")
    complete_tasks = scheduler.filter_tasks(status="complete")

    assert len(luna_tasks) == 1
    assert luna_tasks[0].description == "Walk"
    assert len(complete_tasks) == 1
    assert complete_tasks[0].description == "Wet food"


def test_daily_schedule_uses_due_date() -> None:
    owner = Owner(name="Alex")
    pet = Pet(name="Luna", species="Dog", age_years=4)
    owner.add_pet(pet)

    today = date.today()
    tomorrow = today + timedelta(days=1)
    pet.add_task(
        Task(
            description="Morning walk",
            scheduled_time=time(7, 30),
            frequency="daily",
            due_date=today,
        )
    )
    pet.add_task(
        Task(
            description="Checkup",
            scheduled_time=time(9, 0),
            frequency="weekly",
            due_date=tomorrow,
        )
    )

    scheduler = Scheduler(owner)
    schedule = scheduler.build_daily_schedule(today)

    assert len(schedule) == 1
    assert schedule[0].description == "Morning walk"


def test_as_needed_tasks_do_not_recur() -> None:
    owner = Owner(name="Alex")
    pet = Pet(name="Luna", species="Dog", age_years=4)
    owner.add_pet(pet)

    pet.add_task(
        Task(
            description="Brush fur",
            scheduled_time=time(10, 0),
            frequency="as needed",
        )
    )

    scheduler = Scheduler(owner)
    next_task = scheduler.mark_task_complete("Luna", "Brush fur")

    assert next_task is None
    assert len(pet.tasks) == 1
