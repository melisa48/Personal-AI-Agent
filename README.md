# Personal AI Agent

A Python-based personal assistant application that helps manage tasks, reminders, travel itineraries, and email templates.

## Features

- Task Management
  - Create and track tasks with priorities
  - Set multiple reminders for tasks
  - Track task status (To Do, In Progress, Completed)

- Travel Planning
  - Create detailed travel itineraries
  - Manage flight and hotel information
  - Plan daily activities and schedules
  - Add notes for specific days

- Email Management
  - Pre-defined email templates
  - Customizable placeholders
  - Templates for meeting follow-ups and project updates

- Schedule Management
  - View daily schedules
  - Track upcoming reminders
  - Organize tasks by priority

## Requirements

- Python 3.7+
- No external dependencies required (uses standard library only)

## Installation

1. Clone the repository or download the source code
2. Ensure you have Python 3.7 or higher installed
3. No additional package installation required

## Usage

### Running the Application

```bash
python main.py
```

### Creating Tasks

```python
agent = PersonalAIAgent("User Name")

# Create a task with reminders
agent.create_task_with_reminders(
    title="Task Title",
    description="Task Description",
    due_date="2025-02-15 14:00",
    priority="HIGH",
    reminder_times=[
        "2025-02-14 10:00",
        "2025-02-15 09:00"
    ]
)
```

### Creating Travel Itineraries

```python
# Define activities for each day
activities = {
    "2025-03-15": {
        "morning": "Activity description",
        "afternoon": "Activity description",
        "evening": "Activity description",
        "notes": "Additional notes"
    }
}

# Define hotel information
hotel_info = {
    "name": "Hotel Name",
    "address": "Hotel Address",
    "confirmation": "Confirmation Number",
    "check_in": "2025-03-15",
    "check_out": "2025-03-19"
}

# Define flight information
flight_info = {
    "airline": "Airline Name",
    "flight_number": "FL123",
    "departure_time": "2025-03-15 08:00",
    "arrival_time": "2025-03-15 11:00",
    "confirmation": "Confirmation Number"
}

# Create itinerary
itinerary = agent.create_travel_itinerary(
    destination="Destination",
    start_date="2025-03-15",
    end_date="2025-03-19",
    activities=activities,
    hotel_info=hotel_info,
    flight_info=flight_info
)
```

### Using Email Templates

```python
templates = agent.get_email_templates()
meeting_template = templates["meeting_followup"]

# Format email with custom values
meeting_email = meeting_template.content.format(
    meeting_type="Project Planning",
    recipient_name="Recipient Name",
    meeting_time="today",
    topics_discussed="discussion topics",
    action_items="action items",
    next_steps="next steps",
    sender_name="Sender Name"
)
```

## Data Structures

### Task Priority Levels
- HIGH
- MEDIUM
- LOW

### Task Status Options
- TODO
- IN_PROGRESS
- COMPLETED

## Output Format

The application provides formatted output for:
- Travel itineraries with daily schedules
- Current day's tasks and schedule
- Upcoming reminders
- Email drafts based on templates

## Code Structure

- `PersonalAIAgent`: Main class managing all functionality
- Data classes:
  - `Task`: Represents a task with reminders
  - `Reminder`: Represents a reminder for a task
  - `EmailTemplate`: Template for generating emails
  - `TravelDay`: Represents a single day in a travel itinerary
  - `TravelItinerary`: Complete travel plan with all details

## Contributing
- Contributions to improve the Personal AI Agent are welcome. Please fork the repository and submit a pull request with your changes.
