# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from reminder_db import get_due_reminders, mark_triggered
import pyttsx3
import time

engine = pyttsx3.init()
scheduler = BackgroundScheduler()

def check_reminders():
    due = get_due_reminders()
    for rid, note, remind_at in due:
        msg = f"Reminder: {note} scheduled at {remind_at}"
        print(msg)
        engine.say(msg)
        engine.runAndWait()
        mark_triggered(rid)

def start():
    scheduler.add_job(check_reminders, "interval", seconds=30, id="reminder_job")
    scheduler.start()
    print("Reminder scheduler started.")
