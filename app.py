import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from ics import Calendar, Event
from ics.attendee import Attendee

# Initialize the calendar
calendar = Calendar()

# Function to add events to the .ics file
def add_event_to_ics(event_name, start_time_str, duration_hours, location, url, notes, all_day, status, recurrence, invitees, attachment, travel_time):
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    if all_day.lower() == 'yes':
        end_time = start_time + timedelta(days=1)
    else:
        end_time = start_time + timedelta(hours=duration_hours)

    event = Event()
    event.name = event_name
    event.begin = start_time
    event.end = end_time
    event.location = location
    event.url = url
    event.description = notes
    event.status = status
    event.transparent = (status.lower() == 'free')

    if recurrence.lower() == 'yes':
        event.make_all_day()
    
    # Add attendees
    if invitees:
        for invitee in invitees.split(','):
            event.attendees.add(Attendee(email=invitee.strip()))
    
    # Add attachment as a URL or file path
    if attachment:
        event.url = attachment  # Assuming attachment is a URL or file path

    calendar.events.add(event)

def get_next_day_date(day_name):
    today = datetime.today()
    days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_name = day_name.lower()
    if day_name not in days_of_week:
        raise ValueError("Invalid day of the week.")
    today_weekday = today.weekday()  # Monday is 0 and Sunday is 6
    target_weekday = days_of_week.index(day_name)
    days_ahead = (target_weekday - today_weekday + 7) % 7
    if days_ahead == 0:
        days_ahead = 7
    next_day_date = today + timedelta(days=days_ahead)
    return next_day_date.strftime('%Y-%m-%d')

def save_event():
    day = day_var.get()
    time = time_var.get()
    name = name_var.get()
    duration = duration_var.get()
    location = location_var.get()
    url = url_var.get()
    notes = notes_var.get()
    all_day = all_day_var.get()
    status = status_var.get().upper()  # Convert to uppercase for consistency
    recurrence = recurrence_var.get()
    invitees = invitees_var.get()
    attachment = attachment_var.get()
    travel_time = travel_time_var.get()

    # Validate status
    if status and status not in ['TENTATIVE', 'CONFIRMED', 'CANCELLED']:
        messagebox.showwarning("Input Error", "Status must be one of: TENTATIVE, CONFIRMED, CANCELLED")
        return

    if not day or not time or not name:
        messagebox.showwarning("Input Error", "Day, Time, and Event Name are required!")
        return

    try:
        duration = int(duration)
    except ValueError:
        messagebox.showwarning("Input Error", "Duration must be a number!")
        return

    start_date = get_next_day_date(day)
    add_event_to_ics(name, f"{start_date} {time}:00", duration, location, url, notes, all_day, status, recurrence, invitees, attachment, travel_time)
    messagebox.showinfo("Event Added", f"Event '{name}' added on {day} at {time} for {duration} hour(s).")

def save_to_file():
    with open('weekly_schedule.ics', 'w') as f:
        f.writelines(calendar)
    messagebox.showinfo("File Saved", "Weekly schedule has been created and saved as 'weekly_schedule.ics'.")

# Create the main window
root = tk.Tk()
root.title("Weekly Schedule Creator")

# Create and place the input fields
tk.Label(root, text="Day of the Week:").grid(row=0, column=0, padx=10, pady=5)
day_var = tk.StringVar()
tk.Entry(root, textvariable=day_var).grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Time (HH:MM):").grid(row=1, column=0, padx=10, pady=5)
time_var = tk.StringVar()
tk.Entry(root, textvariable=time_var).grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Event Name:").grid(row=2, column=0, padx=10, pady=5)
name_var = tk.StringVar()
tk.Entry(root, textvariable=name_var).grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Duration (hours):").grid(row=3, column=0, padx=10, pady=5)
duration_var = tk.StringVar()
tk.Entry(root, textvariable=duration_var).grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Location:").grid(row=4, column=0, padx=10, pady=5)
location_var = tk.StringVar()
tk.Entry(root, textvariable=location_var).grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="URL:").grid(row=5, column=0, padx=10, pady=5)
url_var = tk.StringVar()
tk.Entry(root, textvariable=url_var).grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Notes:").grid(row=6, column=0, padx=10, pady=5)
notes_var = tk.StringVar()
tk.Entry(root, textvariable=notes_var).grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="All Day (yes/no):").grid(row=7, column=0, padx=10, pady=5)
all_day_var = tk.StringVar()
tk.Entry(root, textvariable=all_day_var).grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Status (free/busy):").grid(row=9, column=0, padx=10, pady=5)
status_var = tk.StringVar()
tk.Entry(root, textvariable=status_var).grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="Recurrence (yes/no):").grid(row=10, column=0, padx=10, pady=5)
recurrence_var = tk.StringVar()
tk.Entry(root, textvariable=recurrence_var).grid(row=10, column=1, padx=10, pady=5)

tk.Label(root, text="Invitees (comma-separated emails):").grid(row=11, column=0, padx=10, pady=5)
invitees_var = tk.StringVar()
tk.Entry(root, textvariable=invitees_var).grid(row=11, column=1, padx=10, pady=5)

tk.Label(root, text="Attachment (file path):").grid(row=12, column=0, padx=10, pady=5)
attachment_var = tk.StringVar()
tk.Entry(root, textvariable=attachment_var).grid(row=12, column=1, padx=10, pady=5)

tk.Label(root, text="Travel Time (minutes):").grid(row=13, column=0, padx=10, pady=5)
travel_time_var = tk.StringVar()
tk.Entry(root, textvariable=travel_time_var).grid(row=13, column=1, padx=10, pady=5)

# Create and place the buttons
tk.Button(root, text="Add Event", command=save_event).grid(row=14, column=0, padx=10, pady=10)
tk.Button(root, text="Save to File", command=save_to_file).grid(row=14, column=1, padx=10, pady=10)

# Run the application
root.mainloop()
