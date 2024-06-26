import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime, timedelta
from ics import Calendar, Event
from ics.attendee import Attendee

# Initialize the calendar
calendar = Calendar()

# Function to add events to the .ics file
def add_event_to_ics(event_name, start_time_str, duration_hours, all_day, notes):
    start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
    if all_day:
        event = Event(name=event_name, begin=start_time.date())
    else:
        end_time = start_time + timedelta(hours=duration_hours)
        event = Event(name=event_name, begin=start_time, end=end_time)
    event.description = notes
    calendar.events.add(event)

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

def save_event():
    event_name = name_var.get()
    duration_hours = int(duration_var.get())
    notes = notes_var.get()

    # Check which days are selected
    selected_days = []
    for i, day_var in enumerate(day_vars):
        if day_var.get():
            selected_days.append(days_of_week[i])

    # Check if all-day event is selected
    all_day = all_day_var.get()

    for day in selected_days:
        start_date = get_next_day_date(day)
        start_time_str = f"{start_date} 00:00:00" if all_day else f"{start_date} {time_var.get()}:00"
        add_event_to_ics(event_name, start_time_str, duration_hours, all_day, notes)

    messagebox.showinfo("Event Added", f"Event '{event_name}' added on {', '.join(selected_days)}.")

def save_to_file():
    filename = tk.filedialog.asksaveasfilename(defaultextension=".ics", filetypes=[("iCalendar files", "*.ics")])
    if filename:
        with open(filename, 'w') as f:
            f.writelines(calendar)
        messagebox.showinfo("File Saved", f"Events saved to {filename}.")

# Create the main window
root = tk.Tk()
root.title("Weekly Schedule Creator")

# Days of the week labels and variables
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
day_vars = []

# Create and place the day selection checkboxes
for i, day in enumerate(days_of_week):
    day_var = tk.BooleanVar()
    day_vars.append(day_var)
    tk.Checkbutton(root, text=day, variable=day_var).grid(row=i, column=0, padx=10, pady=5)

# Create and place the input fields
tk.Label(root, text="Event Name:").grid(row=0, column=1, padx=10, pady=5)
name_var = tk.StringVar()
tk.Entry(root, textvariable=name_var).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Time (HH:MM):").grid(row=1, column=1, padx=10, pady=5)
time_var = tk.StringVar()
tk.Entry(root, textvariable=time_var).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Duration (hours):").grid(row=2, column=1, padx=10, pady=5)
duration_var = tk.StringVar()
tk.Entry(root, textvariable=duration_var).grid(row=2, column=2, padx=10, pady=5)

tk.Label(root, text="Notes:").grid(row=3, column=1, padx=10, pady=5)
notes_var = tk.StringVar()
tk.Entry(root, textvariable=notes_var).grid(row=3, column=2, padx=10, pady=5)

# Create and place the all-day checkboxes
tk.Label(root, text="All Day Event:").grid(row=4, column=1, padx=10, pady=5)
all_day_var = tk.BooleanVar()
tk.Checkbutton(root, text="Yes", variable=all_day_var, onvalue=True, offvalue=False).grid(row=4, column=2, padx=10, pady=5)
tk.Checkbutton(root, text="No", variable=all_day_var, onvalue=False, offvalue=True).grid(row=4, column=3, padx=10, pady=5)

# Create and place the buttons
tk.Button(root, text="Add Event", command=save_event).grid(row=5, column=1, padx=10, pady=10)
tk.Button(root, text="Save to File", command=save_to_file).grid(row=5, column=2, padx=10, pady=10)

# Run the application
root.mainloop()
