import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
from ics import Calendar, Event
import os

# Function to add events to the .ics file and save each event to a separate file
def add_event_to_ics(event_name, start_time_str, duration_hours, notes, all_day):
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')

    if all_day.lower() == 'yes':
        end_time = start_time + timedelta(days=1)
        event = Event(name=event_name, begin=start_time.date(), end=end_time.date())
        event.make_all_day()
    else:
        end_time = start_time + timedelta(hours=duration_hours)
        event = Event(name=event_name, begin=start_time, end=end_time)

    event.description = notes

    # Create a new calendar and add the event to it
    calendar = Calendar()
    calendar.events.add(event)

    # Save event to a separate .ics file
    save_to_file(calendar, start_time)

def save_to_file(calendar, start_time):
    # Create directory if it doesn't exist
    directory = "ics_files"
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Format filename based on date and count for the day
    date_str = start_time.strftime('%Y%m%d')
    count = len([f for f in os.listdir(directory) if f.startswith(date_str)])
    filename = f"{date_str}_{count + 1}.ics"
    filepath = os.path.join(directory, filename)

    # Write calendar to .ics file
    with open(filepath, 'w') as f:
        f.writelines(calendar.serialize())

    messagebox.showinfo("File Saved", f"Event saved as '{filename}'.")

def save_event():
    day = day_var.get()
    time = time_var.get()
    name = name_var.get()
    duration = duration_var.get()
    notes = notes_var.get()
    all_day = all_day_var.get()

    if not day or not time or not name:
        messagebox.showwarning("Input Error", "Day, Time, and Event Name are required!")
        return

    try:
        duration = int(duration)
    except ValueError:
        messagebox.showwarning("Input Error", "Duration must be a number!")
        return

    start_date = get_next_day_date(day)
    add_event_to_ics(name, f"{start_date} {time}:00", duration, notes, all_day)

def get_next_day_date(day_name):
    today = datetime.today()
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_name = day_name.capitalize()
    if day_name not in days_of_week:
        raise ValueError("Invalid day of the week.")
    today_weekday = today.weekday()  # Monday is 0 and Sunday is 6
    target_weekday = days_of_week.index(day_name)
    days_ahead = (target_weekday - today_weekday + 7) % 7
    if days_ahead == 0:
        days_ahead = 7
    next_day_date = today + timedelta(days=days_ahead)
    return next_day_date.strftime('%Y-%m-%d')

# Create the main window
root = tk.Tk()
root.title("Weekly Event Scheduler")

# Create and place the input fields
tk.Label(root, text="Day of the Week:").grid(row=0, column=0, padx=10, pady=5)
day_var = tk.StringVar()
day_combobox = ttk.Combobox(root, textvariable=day_var, values=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
day_combobox.grid(row=0, column=1, padx=10, pady=5)
day_combobox.current(0)

tk.Label(root, text="Time (HH:MM):").grid(row=1, column=0, padx=10, pady=5)
time_var = tk.StringVar()
tk.Entry(root, textvariable=time_var).grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Event Name:").grid(row=2, column=0, padx=10, pady=5)
name_var = tk.StringVar()
tk.Entry(root, textvariable=name_var).grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Duration (hours):").grid(row=3, column=0, padx=10, pady=5)
duration_var = tk.StringVar()
tk.Entry(root, textvariable=duration_var).grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Notes:").grid(row=4, column=0, padx=10, pady=5)
notes_var = tk.StringVar()
tk.Entry(root, textvariable=notes_var).grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="All Day:").grid(row=5, column=0, padx=10, pady=5)
all_day_var = tk.StringVar()
all_day_check = ttk.Checkbutton(root, text="Yes", variable=all_day_var, onvalue="Yes", offvalue="No")
all_day_check.grid(row=5, column=1, padx=10, pady=5)

# Create and place the buttons
tk.Button(root, text="Add Event", command=save_event).grid(row=6, column=0, padx=10, pady=10)
tk.Button(root, text="Quit", command=root.quit).grid(row=6, column=1, padx=10, pady=10)

# Run the application
root.mainloop()
