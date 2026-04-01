from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
else:
    st.session_state.owner.name = owner_name

pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    st.session_state.owner.add_pet(Pet(name=pet_name, species=species, age_years=1))

st.markdown("### Tasks")
st.caption("Add a few tasks. These feed into the scheduler via your classes.")

selected_date = st.date_input("Schedule date", value=date.today())

pet_names = [pet.name for pet in st.session_state.owner.pets]
selected_pet = st.selectbox("Assign task to pet", pet_names) if pet_names else None

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_description = st.text_input("Task description", value="Morning walk")
with col2:
    scheduled_time = st.time_input("Time", value=time(7, 30))
with col3:
    frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"], index=0)
with col4:
    task_date = st.date_input("Due date", value=selected_date)

if st.button("Add task"):
    if not selected_pet:
        st.warning("Add a pet first so tasks can be assigned.")
    else:
        for pet in st.session_state.owner.pets:
            if pet.name == selected_pet:
                pet.add_task(
                    Task(
                        description=task_description,
                        scheduled_time=scheduled_time,
                        frequency=frequency,
                        due_date=task_date,
                    )
                )
                break

all_tasks = st.session_state.owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": pet.name,
                "description": task.description,
                "time": task.scheduled_time.strftime("%I:%M %p").lstrip("0"),
                "frequency": task.frequency,
                "status": "done" if task.is_complete else "todo",
            }
            for pet in st.session_state.owner.pets
            for task in pet.tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.markdown("### Filters")
filter_pet = st.selectbox("Filter by pet", ["All pets", *pet_names])
filter_status = st.selectbox("Filter by status", ["all", "complete", "incomplete"], index=0)

if st.button("Apply filters"):
    scheduler = Scheduler(st.session_state.owner)
    tasks = scheduler.filter_tasks(
        pet_name=None if filter_pet == "All pets" else filter_pet,
        status=None if filter_status == "all" else filter_status,
        for_date=selected_date,
    )
    if tasks:
        st.table(
            [
                {
                    "description": task.description,
                    "time": task.scheduled_time.strftime("%I:%M %p").lstrip("0"),
                    "frequency": task.frequency,
                    "status": "done" if task.is_complete else "todo",
                }
                for task in tasks
            ]
        )
    else:
        st.info("No tasks matched those filters.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

if st.button("Generate schedule"):
    scheduler = Scheduler(st.session_state.owner)
    schedule = scheduler.build_daily_schedule(selected_date)
    if not schedule:
        st.info("No tasks to schedule yet.")
    else:
        st.success("Schedule ready.")
        st.write("Schedule")
        st.code("\n".join(task.format_for_schedule() for task in schedule))

        conflicts = scheduler.detect_conflicts(schedule)
        if conflicts:
            st.warning("Potential conflicts detected:")
            for conflict in conflicts:
                st.warning(conflict)
