from datetime import datetime

USER_TYPE = [
    (1, "HOD"),
    (2, "Faculty"),
    (3, "Student")
]

GENDER = [
    ("M", "Male"),
    ("F", "Female")
]

YEAR_CHOICES = [(None, "Select Year")] + [(year, str(year)) for year in range(datetime.now().year - 10, datetime.now().year + 6)]

STATUS_CHOICES = [
    ('active', 'Active'),
    ('closed', 'Closed'),
]
