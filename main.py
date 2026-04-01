from datetime import date, time

from pawpal_system import Owner, Pet, Scheduler, Task


def format_schedule(tasks: list[Task], title: str) -> str:
    lines = [title]
    lines.extend(task.format_for_schedule() for task in tasks)
    return "\n".join(lines)


def main() -> None:
    owner = Owner(name="Alex", time_available_minutes=120)

    luna = Pet(name="Luna", species="Dog", age_years=4)
    milo = Pet(name="Milo", species="Cat", age_years=2)

    luna.add_task(Task(description="Evening walk", scheduled_time=time(18, 0), frequency="daily"))
    luna.add_task(Task(description="Morning walk", scheduled_time=time(7, 30), frequency="daily"))
    luna.add_task(Task(description="Vet check-in", scheduled_time=time(7, 30), frequency="weekly"))
    milo.add_task(Task(description="Wet food", scheduled_time=time(8, 0), frequency="daily"))

    owner.add_pet(luna)
    owner.add_pet(milo)

    scheduler = Scheduler(owner)
    today = date.today()
    schedule = scheduler.build_daily_schedule(today)

    print(format_schedule(schedule, "Today's Schedule"))

    conflicts = scheduler.detect_conflicts(schedule)
    if conflicts:
        print("\nConflicts")
        for warning in conflicts:
            print(f"- {warning}")

    luna_tasks = scheduler.filter_tasks(pet_name="Luna", for_date=today)
    print("\nLuna's Tasks")
    for task in luna_tasks:
        print(f"- {task.format_for_schedule()}")

    next_task = scheduler.mark_task_complete("Luna", "Morning walk")
    if next_task:
        print("\nNext occurrence created:")
        print(f"- {next_task.description} on {next_task.due_date.isoformat()}")


if __name__ == "__main__":
    main()
