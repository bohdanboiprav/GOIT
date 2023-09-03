from collections import UserDict
from datetime import date
import re
import json


class PhoneNumberInvalid(Exception):
    pass


class DateError(Exception):
    pass


class Record:
    def __init__(self, name, phone, birthday_date):
        self.name = name
        self.phones = []
        self.__phone = None
        self.phone = phone
        self.__birthday_date = None
        self.birthday_date = birthday_date
        if phone:
            self.phones.append(phone)

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, new_phone):
        pattern = r'^(\+?38)?0\d{9}$'
        if re.match(pattern, new_phone.value):
            self.__phone = new_phone
        else:
            raise PhoneNumberInvalid(
                'Phone number is not correct')

    @property
    def birthday_date(self):
        return self.__birthday_date

    @birthday_date.setter
    def birthday_date(self, new_birthday_date):
        if type(new_birthday_date.value) == date:
            self.__birthday_date = new_birthday_date
        else:
            raise DateError(
                'Date of Birth is not correct')

    def days_to_birthday(self):
        today_day = date.today()
        next_birthday = self.birthday_date.value.replace(year=today_day.year)
        if next_birthday < today_day:
            next_birthday = next_birthday.replace(year=next_birthday.year + 1)
        number_of_days_left = next_birthday - today_day
        return f"{number_of_days_left.days} days left"

    def __repr__(self):
        return f"{self.name.value} {[ph.value for ph in self.phones]} {self.birthday_date.value if self.birthday_date else ''}"


class AddressBook(UserDict):
    N_LIMIT = 2

    def __init__(self):
        super().__init__()
        self.count = 0
        self.call_List = list(self.data.keys())
        with open('Week 12/homework/file_address_book.json') as reader:
            try:
                file_data = json.load(reader)
                for item in file_data:
                    self.data[item['name']
                              ] = f"{item['name']} {item['Phone number']} {item['Date of birth']}"
            except json.decoder.JSONDecodeError:
                file_data = []

    def add_record(self, record):
        with open('Week 12/homework/file_address_book.json') as reader:
            try:
                file_data = json.load(reader)
            except json.decoder.JSONDecodeError:
                file_data = []
        self.data[record.name.value] = record
        write_dict = {}
        write_dict["name"] = record.name.value
        write_dict["Phone number"] = [ph.value for ph in record.phones]
        write_dict["Date of birth"] = str(
            record.birthday_date.value) if record.birthday_date else ''
        file_data.append(write_dict)
        with open('Week 12/homework/file_address_book.json', 'w') as writer:
            json.dump(file_data, writer, indent=4)
            print("Done")

    def __iter__(self):
        return self.__next__()

    def __next__(self):
        index = 0
        contacts = list(self.data.values())
        while index < len(contacts):
            yield contacts[index:index + self.N_LIMIT]
            index += self.N_LIMIT

    def find_record(self, search_item):
        output = []
        search_item = search_item.lower()
        for record in self.data.values():
            record = str(record)
            if search_item in record.lower():
                output.append(record)
        return output


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    def __init__(self, phone=None):
        super().__init__(phone)


class Birthday(Field):
    def __init__(self, birthday_date=None):
        super().__init__(birthday_date)


if __name__ == '__main__':
    name = Name('Bill')
    phone = Phone('0634120821')
    birthdayday = Birthday(date(1985, 9, 15))
    rec = Record(name, phone, birthdayday)
    print(rec.days_to_birthday())
    ab = AddressBook()
    ab.add_record(rec)

    # add 2 contact
    name2 = Name('Bob')
    phone2 = Phone('0634520821')
    birthdayday2 = Birthday(date(1980, 11, 15))
    rec2 = Record(name2, phone2, birthdayday2)
    print(rec2.days_to_birthday())
    ab.add_record(rec2)

    # add 3 contact
    name3 = Name('Donny')
    phone3 = Phone('0634520822')
    birthdayday3 = Birthday(date(1980, 9, 2))
    rec3 = Record(name3, phone3, birthdayday3)
    print(rec3.days_to_birthday())
    ab.add_record(rec3)

    # add 4 contact
    name4 = Name('Sam')
    phone4 = Phone('0634520823')
    birthdayday4 = Birthday(date(1980, 8, 20))
    rec4 = Record(name4, phone4, birthdayday4)
    print(rec4.days_to_birthday())
    ab.add_record(rec4)
    # assert isinstance(ab['Bill'], Record)
    # assert isinstance(ab['Bill'].name, Name)
    # assert isinstance(ab['Bill'].phones, list)
    # assert isinstance(ab['Bill'].phones[0], Phone)
    # assert ab['Bill'].phones[0].value == '0634120821'

    print('All Ok)')

    page = 1
    for i in ab:
        print(f"Page {page}")
        print(i)
        page += 1

    print(ab.find_record("0634520822"))
