# schedule_manager.py
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from voice_utils import speak

# In-memory list to store scheduled events.
events = []

def add_event(event_time, description):
    """Add an event to the schedule."""
    events.append({'time': event_time, 'description': description})
    speak(f"Event added: {description} at {event_time.strftime('%I:%M %p')}.")

def check_reminders():
    """Check scheduled events and speak a reminder if an event is due."""
    now = datetime.now()
    for event in events[:]:
        # If the event is due now (or within the next minute).
        if now >= event['time'] and now <= event['time'] + timedelta(seconds=60):
            speak(f"Reminder: {event['description']} is scheduled now.")
            events.remove(event)

def start_scheduler():
    """Start a background scheduler to check for event reminders every 30 seconds."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_reminders, 'interval', seconds=30)
    scheduler.start()
