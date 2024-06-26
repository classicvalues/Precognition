import argparse
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

# Command-line interface for adding events
def cli_interface():
    parser = argparse.ArgumentParser(description='Create and manage a weekly schedule.')
    parser.add_argument('--add', metavar=('DAY', 'TIME', 'NAME', 'DURATION'), type=str, nargs=4, 
                        help='Add an event to the schedule (e.g., --add monday 09:00 "Meeting with Team" 1)')
    args = parser.parse_args()

    if args.add:
        day, time, name, duration = args.add
        start_date = get_next_day_date(day)
        add_event_to_ics(name, f"{start_date} {time}:00", int(duration))
        print(f"Event '{name}' added on {day} at {time} for {duration} hour(s).")

    else:
        while True:
            add_more = input("Would you like to add an event? (y/n): ").lower()
            if add_more == 'n':
                break
            day = input("Enter the day of the week: ").strip().lower()
            time = input("Enter the time (HH:MM): ").strip()
            name = input("Enter the event name: ").strip()
            duration = input("Enter the duration in hours: ").strip()

            start_date = get_next_day_date(day)
            add_event_to_ics(name, f"{start_date} {time}:00", int(duration))
            print(f"Event '{name}' added on {day} at {time} for {duration} hour(s).")

    # Save the .ics file
    with open('weekly_schedule.ics', 'w') as f:
        f.writelines(calendar)
    print("Weekly schedule has been created and saved as 'weekly_schedule.ics'.")

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

if __name__ == '__main__':
    cli_interface()
