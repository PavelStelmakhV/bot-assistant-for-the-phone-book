from collections import UserDict


class Field:
    pass


class Name(Field):
    def __init__(self, value):
        self.value = value


class Phone(Field):
    def __init__(self, value):
        self.value = value

    def set_number(self, value):
        self.value = value

    def get_number(self):
        return self.value


class Record:

    def __init__(self, name):
        self.name = name
        self.phone_list = []

    def add_phone(self, phone_number: str):
        self.phone_list.append(Phone(phone_number))

    def change_phone(self, phone_number: str, index=0):
        try:
            self.phone_list[index].set_number(phone_number)
            return 'Number changed successfully'
        except KeyError:
            return f'In field {index} there is no phone number to change'

    def delete_phone(self, index=0):
        try:
            self.phone_list.pop(index)
            return 'Number deleted successfully'
        except KeyError:
            return f'In field {index} there is no phone number to delete'

    def show_phone(self):
        return ' '.join([phone.get_number() for phone in self.phone_list])


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}
        self.find_result = []

    def add_record(self, name: str):
        if not (name in self.data):
            self.data[name] = Record(Name(name))

    def find_record(self, find_text):
        self.find_result = []
        for record in self.data.values():
            if str(record.name.value).find(find_text) > -1:
                self.find_result.append(record.name.value)
        if len(self.find_result) > 0:
            return f'Records where "{find_text}" were found: ' + ', '.join(self.find_result)
        return f'"{find_text}" matches not found'


phone_book = AddressBook()