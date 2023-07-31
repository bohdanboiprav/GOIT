from datetime import datetime, timedelta, date


def get_birthdays_per_week(users):
    today_day = datetime.now()
    today_day = today_day.date()
    seven_days_interval = today_day + timedelta(days=7)
    birthday_dict = {}
    for i in users:
        k = i["birthday"].replace(year=datetime.now().year)
        if k.strftime("%A") == "Saturday":
            k = k + timedelta(days=2)
        if k.strftime("%A") == "Sunday":
            k = k + timedelta(days=1)
        if k >= today_day and k <= seven_days_interval:
            if k in birthday_dict.keys():
                birthday_dict[k] = birthday_dict[k] + ", " + i["name"]
            else:
                birthday_dict[k] = i["name"]
                k = k
    sorted_birthday_dict = {k: v for k, v in sorted(birthday_dict.items())}
    print(sorted_birthday_dict)
    for i, k in sorted_birthday_dict.items():
        print(i.strftime("%A") + ": " + k)


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
