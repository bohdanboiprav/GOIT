from datetime import timedelta, date
import calendar


def get_birthdays_per_week(users):
    today_day = date.today()
    if today_day.weekday() == 0:
        today_day = today_day - timedelta(days=2)
    seven_days_interval = today_day + timedelta(days=7)
    birthday_dict = {i: [] for i in range(7)}
    for user in users:
        bd = user["birthday"].replace(year=today_day.year)
        if bd >= today_day and bd <= seven_days_interval:
            weekday = bd.weekday()
            if weekday in [5, 6]:
                weekday = 0
            birthday_dict[weekday].append(user['name'])
    for day, names in birthday_dict.items():
        if len(names) >= 1:
            names = ", ".join(names)
            print(calendar.day_name[day] + ": " + names)


users = [
    {"name": "John", "birthday": date(1985, 8, 15)},
    {"name": "Emily", "birthday": date(1992, 8, 14)},
    {"name": "Michael", "birthday": date(1978, 8, 3)},
    {"name": "Sarah", "birthday": date(1990, 8, 9)},
    {"name": "David", "birthday": date(1987, 9, 1)},
    {"name": "Jessica", "birthday": date(1983, 8, 2)},
    {"name": "Daniel", "birthday": date(1995, 8, 3)},
    {"name": "Jennifer", "birthday": date(1989, 8, 6)},
    {"name": "Christopher", "birthday": date(1980, 12, 24)},
    {"name": "Elizabeth", "birthday": date(1998, 8, 9)},
    {"name": "Matthew", "birthday": date(1984, 7, 8)},
    {"name": "Olivia", "birthday": date(1993, 10, 14)},
    {"name": "Andrew", "birthday": date(1976, 7, 13)},
    {"name": "Sophia", "birthday": date(1991, 9, 20)},
    {"name": "William", "birthday": date(1982, 4, 16)},
    {"name": "Ava", "birthday": date(1997, 11, 8)},
    {"name": "Ryan", "birthday": date(1986, 8, 11)},
    {"name": "Natalie", "birthday": date(1994, 8, 5)},
    {"name": "James", "birthday": date(1981, 8, 6)},
    {"name": "Grace", "birthday": date(1996, 6, 23)}
]

get_birthdays_per_week(users)
