from datetime import time

from pawpal_system import Owner, Pet, Scheduler, Task


def format_schedule(tasks: list[Task]) -> str:
    lines = ["Today's Schedule"]
    lines.extend(task.format_for_schedule() for task in tasks)
    return "\n".join(lines)


def main() -> None:
    owner = Owner(name="Alex", time_available_minutes=120)

    luna = Pet(name="Luna", species="Dog", age_years=4)
    milo = Pet(name="Milo", species="Cat", age_years=2)

    luna.add_task(Task(description="Morning walk", scheduled_time=time(7, 30), frequency="daily"))
    luna.add_task(Task(description="Evening walk", scheduled_time=time(18, 0), frequency="daily"))
    milo.add_task(Task(description="Wet food", scheduled_time=time(8, 0), frequency="daily"))

    owner.add_pet(luna)
    owner.add_pet(milo)

    scheduler = Scheduler(owner)
    schedule = scheduler.build_daily_schedule()

    print(format_schedule(schedule))


if __name__ == "__main__":
    main()
