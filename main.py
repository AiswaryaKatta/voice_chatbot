# main.py
import time
from datetime import datetime, timedelta
import openai

from config import OPENAI_API_KEY
from voice_utils import speak, listen
from schedule_manager import add_event, start_scheduler

# Set your OpenAI API key.
openai.api_key = OPENAI_API_KEY

def generate_response(prompt):
    """Use the OpenAI API to generate an answer for general queries."""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def process_command(command):
    """
    Process the user's command:
    - If it includes a reminder request, extract details and schedule an event.
    - Otherwise, use the OpenAI API to answer the question.
    """
    if "remind me" in command.lower():
        try:
            # Expecting a command like "Remind me to attend the meeting at 15:00"
            parts = command.lower().split("remind me to")
            details = parts[1].strip() if len(parts) > 1 else ""
            if "at" in details:
                event_parts = details.split("at")
                description = event_parts[0].strip()
                time_part = event_parts[1].strip()
                # Parse the time assuming a 24-hour format "HH:MM"
                event_time = datetime.strptime(time_part, "%H:%M")
                # Adjust event_time to today's date; if the time has passed, set it for tomorrow.
                now = datetime.now()
                event_time = event_time.replace(year=now.year, month=now.month, day=now.day)
                if event_time < now:
                    event_time += timedelta(days=1)
                add_event(event_time, description)
            else:
                speak("Please specify the time for the reminder using 'at HH:MM'.")
        except Exception as e:
            speak("Sorry, I couldn't parse the event details. Please try again.")
    else:
        # For general queries, generate a response using the OpenAI API.
        response = generate_response(command)
        speak(response)

def main():
    # Start the background scheduler for event reminders.
    start_scheduler()
    speak("Hello, I am your personal voice assistant.")
    print("Greeting spoken. Now entering main loop...")
    
    while True:
        command = listen()
        if command:
            process_command(command)
        time.sleep(1)

if __name__ == "__main__":
    main()
