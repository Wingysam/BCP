import csv
from datetime import datetime, timedelta
from collections import defaultdict, Counter

YEAR = 2024  # Year this semester was part of
START_DATE = datetime(2024, 11, 5)  # First day of the studied period
END_DATE = datetime(2024, 12, 3)  # Last day of the studied period
WINDOW = 7  # Number of days to look ahead for due assignments


def read_assignments(file_path):
    with open(file_path, mode="r") as file:
        reader = csv.DictReader(file)
        return list(reader)


assignments = read_assignments(
    "/Users/wingy/Documents/Code/Personal/BCP/data/assignments.csv"
)


def parse_canvas_date(date):
    if date == "":
        return None

    # Formatted like: Nov 11 by 11:59pm
    # Or: Nov 4 at 10:52pm
    # Or: Sep 30 at 5pm
    date_formats = [
        "%b %d by %I:%M%p",
        "%b %d by %I%p",
        "%b %d at %I:%M%p",
        "%b %d at %I%p",
    ]
    for date_format in date_formats:
        try:
            return datetime.strptime(f"{YEAR} {date}", f"%Y {date_format}")
        except ValueError:
            continue
    raise ValueError(f"Date format for '{date}' is not recognized")


# Convert string dates to datetime objects in all of the assignment dictionaries
for assignment in assignments:
    assignment["due_date"] = parse_canvas_date(assignment["due_date"])
    assignment["submit_date"] = parse_canvas_date(assignment["submit_date"])

# Filter out assignments that are outside of the studied period, did not have a due date, or were never submitted
assignments = [
    assignment
    for assignment in assignments
    if assignment["due_date"] is not None
    and START_DATE <= assignment["due_date"] <= (END_DATE + timedelta(days=WINDOW))
]

# Sort assignments by due date, earliest first
assignments = sorted(
    assignments, key=lambda assignment: assignment["due_date"], reverse=True
)

# Initialize a dictionary to count assignments for each day
day_counts = defaultdict(Counter)

current_date = START_DATE
while current_date <= END_DATE:
    for assignment in assignments:
        due_date = assignment["due_date"]
        submit_date = assignment["submit_date"]
        is_submitted_yet = submit_date is not None and submit_date <= current_date
        if is_submitted_yet:
            continue
        if due_date and (0 <= (due_date - current_date).days <= WINDOW):
            day_counts[current_date]["due_within_window"] += 1
        if due_date and submit_date and due_date < current_date:
            day_counts[current_date]["past_due_submitted"] += 1
    current_date += timedelta(days=1)

# Print the results
print(f"Date,Due within {WINDOW} days")
for day, counts in day_counts.items():
    print(
        f'{day.strftime("%Y-%m-%d")},{counts["due_within_window"]+ counts['past_due_submitted']}'
    )
