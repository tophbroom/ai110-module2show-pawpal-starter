# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I started with four classes that mirror the core workflow. Owner stores the user's profile, time availability, and preferences plus their list of pets. Pet stores basic pet profile data used for planning. Task represents a single care item with duration, priority, and due date information. Planner owns the list of tasks and is responsible for adding/editing tasks and generating a daily plan for the owner.

Core user actions for PawPal+:
- Enter basic owner and pet info.
- Add or edit care tasks with duration and priority.
- Generate and view a daily plan that explains why tasks were scheduled.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

After reviewing the skeleton, I added a `task_id` to Task and updated Planner.edit_task to use that id instead of title. This avoids ambiguity when multiple tasks share the same name. I also added an optional `pet_name` on Task so each task can be tied to a specific pet, which makes the scheduling logic clearer.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

My scheduler only checks for exact time collisions (same scheduled time), not overlapping durations. This keeps the logic simple and easy to explain early in the project, and it is sufficient for a basic daily routine where tasks are short and usually non-overlapping by design.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
