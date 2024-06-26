import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from ics import Calendar, Event

# Initialize the calendar
calendar = Calendar()

# Function to add events to the .ics file
def add_event_to_ics(event_name, start_time_str, duration_hours):
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    end_time = start_time + timedelta(hours=duration_hours)

    event = Event()
    event.name = event_name
    event.begin = start_time
    event.end = end_time

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

    if not day or not time or not name or not duration:
        messagebox.showwarning("Input Error", "All fields are required!")
        return

    try:
        duration = int(duration)
    except ValueError:
        messagebox.showwarning("Input Error", "Duration must be a number!")
        return

    start_date = get_next_day_date(day)
    add_event_to_ics(name, f"{start_date} {time}:00", duration)
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

# Create and place the buttons
tk.Button(root, text="Add Event", command=save_event).grid(row=4, column=0, padx=10, pady=10)
tk.Button(root, text="Save to File", command=save_to_file).grid(row=4, column=1, padx=10, pady=10)

# Run the application
root.mainloop()
