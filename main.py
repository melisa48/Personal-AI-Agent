import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional
import json
import os
from enum import Enum


class TaskPriority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class TaskStatus(Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"


@dataclass
class Reminder:
    task_id: str
    reminder_time: datetime.datetime
    notification_sent: bool = False
    message: str = ""


@dataclass
class Task:
    id: str
    title: str
    description: str
    due_date: datetime.datetime
    priority: TaskPriority
    status: TaskStatus
    reminders: List[Reminder] = None


@dataclass
class EmailTemplate:
    subject: str
    content: str
    placeholders: List[str]


@dataclass
class TravelDay:
    date: datetime.datetime
    morning: str
    afternoon: str
    evening: str
    notes: Optional[str] = None


@dataclass
class TravelItinerary:
    destination: str
    start_date: datetime.datetime
    end_date: datetime.datetime
    days: List[TravelDay]
    hotel_info: Dict
    flight_info: Dict


class PersonalAIAgent:
    def __init__(self, user_name: str):
        self.user_name = user_name
        self.tasks: List[Task] = []
        self.reminders: List[Reminder] = []
        self.travel_itineraries: List[TravelItinerary] = []

    def add_reminder(self, task_id: str, reminder_time: str, message: str = "") -> Reminder:
        """Add a new reminder for a task"""
        reminder_datetime = datetime.datetime.strptime(reminder_time, "%Y-%m-%d %H:%M")
        reminder = Reminder(
            task_id=task_id,
            reminder_time=reminder_datetime,
            message=message
        )
        self.reminders.append(reminder)
        return reminder

    def create_task_with_reminders(self, title: str, description: str,
                                   due_date: str, priority: str,
                                   reminder_times: List[str] = None) -> Task:
        """Create a task with optional reminders"""
        task_id = f"task_{len(self.tasks) + 1}"
        due_date_obj = datetime.datetime.strptime(due_date, "%Y-%m-%d %H:%M")

        reminders = []
        if reminder_times:
            for reminder_time in reminder_times:
                reminder = self.add_reminder(
                    task_id=task_id,
                    reminder_time=reminder_time,
                    message=f"Reminder: {title} is due {due_date}"
                )
                reminders.append(reminder)

        task = Task(
            id=task_id,
            title=title,
            description=description,
            due_date=due_date_obj,
            priority=TaskPriority[priority.upper()],
            status=TaskStatus.TODO,
            reminders=reminders
        )

        self.tasks.append(task)
        return task

    def get_email_templates(self) -> Dict[str, EmailTemplate]:
        """Predefined email templates"""
        return {
            "meeting_followup": EmailTemplate(
                subject="Follow-up on Our {meeting_type} Meeting",
                content="""
Hi {recipient_name},

Thank you for the productive meeting {meeting_time}. It was great to discuss {topics_discussed}. I appreciate your insights and suggestions.

As we agreed, I will {action_items}, and I look forward to {next_steps}.

Please let me know if you have any questions or need further information.

Best regards,
{sender_name}
                """,
                placeholders=["meeting_type", "recipient_name", "meeting_time",
                              "topics_discussed", "action_items", "next_steps", "sender_name"]
            ),
            "project_update": EmailTemplate(
                subject="Project Update: {project_name}",
                content="""
Dear {recipient_name},

I hope this email finds you well. I wanted to provide an update on {project_name}.

Current Status:
{project_status}

Key Achievements:
{achievements}

Next Steps:
{next_steps}

Timeline:
{timeline}

Please let me know if you need any clarification or have questions.

Best regards,
{sender_name}
                """,
                placeholders=["project_name", "recipient_name", "project_status",
                              "achievements", "next_steps", "timeline", "sender_name"]
            )
        }

    def create_travel_itinerary(self, destination: str, start_date: str,
                                end_date: str, activities: Dict[str, Dict[str, str]],
                                hotel_info: Dict, flight_info: Dict) -> TravelItinerary:
        """Create a detailed travel itinerary"""
        start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        days = []
        current_date = start_date_obj
        while current_date <= end_date_obj:
            date_str = current_date.strftime("%Y-%m-%d")
            day_activities = activities.get(date_str, {
                "morning": "Free time",
                "afternoon": "Free time",
                "evening": "Free time"
            })

            days.append(TravelDay(
                date=current_date,
                morning=day_activities["morning"],
                afternoon=day_activities["afternoon"],
                evening=day_activities["evening"],
                notes=day_activities.get("notes")
            ))
            current_date += datetime.timedelta(days=1)

        itinerary = TravelItinerary(
            destination=destination,
            start_date=start_date_obj,
            end_date=end_date_obj,
            days=days,
            hotel_info=hotel_info,
            flight_info=flight_info
        )

        self.travel_itineraries.append(itinerary)
        return itinerary

    def format_travel_itinerary(self, itinerary: TravelItinerary) -> str:
        """Format a travel itinerary for display"""
        output = [f"Travel Itinerary: {itinerary.destination}"]
        output.append(f"Date: {itinerary.start_date.strftime('%b %d')} - {itinerary.end_date.strftime('%b %d')}\n")

        output.append("Flight Information:")
        output.append(f"Departure: {itinerary.flight_info['departure_time']}")
        output.append(f"Arrival: {itinerary.flight_info['arrival_time']}")
        output.append(f"Flight Number: {itinerary.flight_info['flight_number']}\n")

        output.append("Hotel Information:")
        output.append(f"Name: {itinerary.hotel_info['name']}")
        output.append(f"Address: {itinerary.hotel_info['address']}")
        output.append(f"Confirmation: {itinerary.hotel_info['confirmation']}\n")

        output.append("Daily Schedule:")
        for day in itinerary.days:
            output.append(f"\nDay {(day.date - itinerary.start_date).days + 1}: {day.date.strftime('%A, %B %d')}")
            output.append(f"Morning: {day.morning}")
            output.append(f"Afternoon: {day.afternoon}")
            output.append(f"Evening: {day.evening}")
            if day.notes:
                output.append(f"Notes: {day.notes}")

        return "\n".join(output)

    def get_upcoming_reminders(self) -> List[Dict]:
        """Get all upcoming reminders with task details"""
        now = datetime.datetime.now()
        upcoming = []
        for reminder in self.reminders:
            if not reminder.notification_sent and reminder.reminder_time > now:
                task = next((t for t in self.tasks if t.id == reminder.task_id), None)
                if task:
                    upcoming.append({
                        'time': reminder.reminder_time,
                        'task_title': task.title,
                        'message': reminder.message
                    })
        return sorted(upcoming, key=lambda x: x['time'])

    def print_daily_schedule(self):
        """Print today's schedule including tasks and reminders"""
        today = datetime.datetime.now()
        print(f"\nToday's Schedule ({today.strftime('%Y-%m-%d')}):")

        # Get today's tasks
        today_tasks = [task for task in self.tasks
                       if task.due_date.date() == today.date()]

        if today_tasks:
            for task in today_tasks:
                print(f"- {task.due_date.strftime('%H:%M')} - {task.title} ({task.priority.value})")
        else:
            print("No tasks scheduled for today")

        # Get upcoming reminders
        print("\nUpcoming Reminders:")
        upcoming = self.get_upcoming_reminders()
        if upcoming:
            for reminder in upcoming:
                print(f"- {reminder['time'].strftime('%Y-%m-%d %H:%M')} - {reminder['task_title']}")
        else:
            print("No upcoming reminders")


def main():
    agent = PersonalAIAgent("John Doe")

    # Create tasks with reminders
    agent.create_task_with_reminders(
        title="Quarterly Review Presentation",
        description="Prepare and deliver Q1 review presentation",
        due_date="2025-02-15 14:00",
        priority="HIGH",
        reminder_times=[
            "2025-02-14 10:00",
            "2025-02-15 09:00"
        ]
    )

    # Create a travel itinerary
    new_york_activities = {
        "2025-03-15": {
            "morning": "Arrive in New York and check into hotel",
            "afternoon": "Explore Times Square and surrounding area",
            "evening": "Broadway show: The Lion King",
            "notes": "Hotel check-in after 3 PM"
        },
        "2025-03-16": {
            "morning": "Visit Statue of Liberty and Ellis Island",
            "afternoon": "Walk across Brooklyn Bridge, explore Brooklyn Heights",
            "evening": "Dinner in DUMBO",
            "notes": "Book ferry tickets in advance"
        }
    }

    hotel_info = {
        "name": "Grand Hyatt New York",
        "address": "109 E 42nd St, New York, NY 10017",
        "confirmation": "HY123456",
        "check_in": "2025-03-15",
        "check_out": "2025-03-19"
    }

    flight_info = {
        "airline": "Delta Airlines",
        "flight_number": "DL123",
        "departure_time": "2025-03-15 08:00",
        "arrival_time": "2025-03-15 11:00",
        "confirmation": "DL789012"
    }

    itinerary = agent.create_travel_itinerary(
        destination="New York",
        start_date="2025-03-15",
        end_date="2025-03-19",
        activities=new_york_activities,
        hotel_info=hotel_info,
        flight_info=flight_info
    )

    # Print formatted itinerary
    print(agent.format_travel_itinerary(itinerary))

    # Create and print email
    templates = agent.get_email_templates()
    meeting_template = templates["meeting_followup"]

    meeting_email = meeting_template.content.format(
        meeting_type="Project Planning",
        recipient_name="Sarah Smith",
        meeting_time="today",
        topics_discussed="the Q1 marketing strategy and budget allocation",
        action_items="prepare the revised budget proposal by next Friday",
        next_steps="our follow-up meeting next week",
        sender_name="John Doe"
    )

    print("\nEmail Draft:")
    print(meeting_template.subject.format(meeting_type="Project Planning"))
    print(meeting_email)

    # Print schedule and reminders
    agent.print_daily_schedule()


if __name__ == "__main__":
    main()