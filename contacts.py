from collections import UserDict
from datetime import datetime, timedelta
from pickle import load, dump


FILE_NAME = 'data.bin'


class Field:
    def __init__(self, value: str):
        self.__value = None

        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value


class Birthday(Field):
    def __init__(self, value: datetime):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) == 0:
            raise ValueError('Name length must be greater than 0')
        if '.' in value:
            Field.value.fset(self, datetime.strptime(value, '%d.%m.%Y'))
        elif '/' in value:
            Field.value.fset(self, datetime.strptime(value, '%d/%m/%Y'))
        else:
            raise ValueError('Date must be in the format "dd/mm/yyyy" or "dd.mm.yyyy"')


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) > 0:
            Field.value.fset(self, value)
        else:
            raise ValueError('Name length must be greater than 0')


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)

    @Field.value.setter
    def value(self, value):
        if len(value) == 0:
            raise ValueError('Phone length must be greater than 0')
        if len(value) == 9 and str(value).isdigit():
            value = '+380' + str(value)
            Field.value.fset(self, value)
        elif len(value[1::]) == 12 and str(value[1::]).isdigit() and value[0] == '+':
            Field.value.fset(self, value)
        else:
            raise ValueError('Phone must be in the format "+############" or "#########"')


class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None):
        self.name: Name = name
        self.phone_list: list[Phone] = [phone] if phone is not None else []
        self.birthday: Birthday = birthday

    def __str__(self):
        result = f"{self.name.value}:"
        if len(self.phone_list) > 0:
            result += f" {', '.join(phone.value for phone in self.phone_list)};"
        if self.birthday is not None:
            result += f" birthday: {self.birthday.value.strftime('%d.%m.%Y')}"
        result += '\n'
        return result

    def add_phone(self, phone: Phone):
        self.phone_list.append(phone)

    def change_phone(self, phone: Phone, index: int = 0):
        try:
            self.phone_list[index] = phone
            return 'Number changed successfully'
        except KeyError:
            return f'In field {index} there is no phone number to change'

    def delete_phone(self, index: int = 0):
        try:
            self.phone_list.pop(index)
            return 'Number deleted successfully'
        except KeyError:
            return f'In field {index} there is no phone number to delete'

    def show_phone(self):
        return ' '.join([phone.value for phone in self.phone_list])

    def days_to_birthday(self) -> int:
        if self.birthday is None:
            return None
        birthday = self.birthday.value
        try:
            birthday_this_year = birthday.replace(year=datetime.now().year)
            if birthday_this_year.date() < datetime.now().date():
                birthday_this_year = birthday_this_year.replace(year=datetime.now().year + 1)
            # processing on February 29 by increasing the date of the birthday by 1
        except ValueError:
            birthday += timedelta(days=1)
            birthday_this_year = birthday.replace(year=datetime.now().year)
            if birthday_this_year.date() < datetime.now().date():
                birthday_this_year = birthday_this_year.replace(year=datetime.now().year + 1)
        delta = birthday_this_year.date() - datetime.now().date()
        return delta.days


class AddressBook(UserDict):
    def __init__(self, max_line: int = 3):
        self.data = {}
        self.find_result = []
        self.max_line = max_line
        self.current_value = 0
        self.load_book()

    def iterator(self, max_line: int = 5):
        result = ''
        count = 0
        total_count = 0
        for record in self.data.values():  # type: Record
            count += 1
            total_count += 1
            result = result + str(record)
            if count >= max_line or total_count >= len(self.data):
                yield result
                result = ''
                count = 0

    def add_record(self, name: Name, phone: Phone = None):
        if not (name in self.data):
            self.data[name.value] = Record(name=name, phone=phone)

    def find_record(self, find_text: str):
        self.find_result = []
        for record in self.data.values():  # type: Record
            # find by name or phones
            if find_text in str(record.name.value) or bool(list(filter(lambda x: find_text in x.value, record.phone_list))):
                self.find_result.append(record.name.value)
        if len(self.find_result) > 0:
            return f'Records where "{find_text}" were found: ' + ', '.join(self.find_result)
        return f'"{find_text}" matches not found'

    def load_book(self):
        try:
            with open(FILE_NAME, 'rb') as fh:
                self.data = load(fh)
        except FileNotFoundError:
            pass

    def save_book(self):
        with open(FILE_NAME, 'wb') as fh:
            dump(self.data, fh)


phone_book = AddressBook()


