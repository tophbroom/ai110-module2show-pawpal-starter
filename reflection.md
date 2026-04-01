# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I started with four classes that mirror the core workflow. Owner stores the user's profile, time availability, and preferences plus their list of pets. Pet stores basic pet profile data used for planning. Task represents a single care item with time, frequency, due date, and completion status. Scheduler owns the planning logic for sorting, filtering, conflict checks, and recurrence.

Core user actions for PawPal+:

- Enter basic owner and pet info.
- Add or edit care tasks with duration and priority.
- Generate and view a daily plan that explains why tasks were scheduled.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yeah, my design did change a bit. I renamed Planner to Scheduler because it made more sense for what it actually does. I also updated Task to include a scheduled time, how often it repeats, and a due date so recurring tasks would work properly. I also moved the filtering and conflict checking into Scheduler so the logic wouldn't get mixed up with the UI stuff.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

The scheduler considers scheduled time, due date, and completion status. For now, time and due date matter most because they directly affect what appears in the daily plan and in what order; preferences and priorities can be layered on later.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler only checks for exact time collisions (same scheduled time), not overlapping durations. This keeps the logic simple and easy to explain early in the project and it is sufficient for a basic daily routine where tasks are short and usually non-overlapping by design.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used Copilot Chat to help me think through the UML and figure out what each class should do. Then I used Inline Chat to actually turn those ideas into Python code and to make small changes like adding filtering. The prompts that helped the most were really specific ones, like "sort tasks by time" or "add conflict warnings without overcomplicating the model."

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One suggestion I modified was an early idea to store tasks directly on the Scheduler. I kept tasks on each Pet and used Owner methods to aggregate them instead, which kept the data model aligned with the UI and reduced duplication. I verified behavior by running the CLI demo and pytest after each change.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested things like completing a task, adding tasks, sorting the schedule, creating recurring tasks, catching conflicts and filtering by pet, status, or date. These mattered because they cover the main things users are actually going to do and they check both the normal cases and some edge cases too.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm pretty confident it works for the main stuff since the UI and the tests give the same results. If I had more time I'd want to test things like tasks that overlap in duration, really long task lists and more complicated repeating schedules.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most happy with how everything came together from the UML all the way to the actual UI, especially the recurring task feature and seeing the conflict warnings actually show up in the schedule.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would add duration-aware conflicts, richer priorities and clearer explanations in the UI for why tasks were ordered or flagged.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Using separate chat sessions for design, implementation and testing helped me keep each phase focused and avoid mixing requirements. As the lead architect, I learned to treat AI output as a draft, validate it against my goals and make the final design calls based on clarity and maintainability.

My key takeaway is that AI accelerates exploration, but good system design still depends on clear ownership of requirements, consistent naming and frequent verification.
