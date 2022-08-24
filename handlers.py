from typing import Dict, Callable
from contacts import *


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError as error:
            result = str(error) + '\nTry again.'
        except ValueError as error:
            result = str(error) + '\nTry again.'
        except IndexError:
            result = "Incomplete command modifier. Give me name and phone please." + '\nTry again.'
        return result
    return inner


def handler_hello(*args) -> str:
    return 'How can I help you?'


@input_error
def handler_add(modifier: str) -> str:
    modifier_list = modifier.split(' ')
    if len(modifier_list) != 2:
        raise ValueError("Two parameters are required: name and phone number (separated by a space)")
    if modifier_list[0] in phone_book:
        phone_book[modifier_list[0]].add_phone(Phone(value=modifier_list[1]))
        return f'Phone added to record {modifier_list[0]}'
    else:
        phone_book.add_record(name=Name(value=modifier_list[0]), phone=Phone(value=modifier_list[1]))
        return 'Record added to phone book'


@input_error
def handler_birthday(modifier: str) -> str:
    modifier_list = modifier.split(' ')
    if len(modifier_list) != 2:
        raise ValueError("Two parameters are required: name and birthday (separated by a space)")
    if not (modifier_list[0] in phone_book):
        raise KeyError(f'Name {modifier_list[0]} not found in phone list')
    phone_book[modifier_list[0]].birthday = Birthday(value=modifier_list[1])
    return f'Record {modifier_list[0]} changed in phone book'


@input_error
def handler_day_of_birthday(modifier: str) -> str:
    modifier_list = modifier.split(' ')
    if not (modifier_list[0] in phone_book):
        raise KeyError(f'Name {modifier_list[0]} not found in phone list')
    return f"{modifier_list[0]}'s birthday in {phone_book[modifier_list[0]].days_to_birthday()} days"


@input_error
def handler_change(modifier: str) -> str:
    modifier_list = modifier.split(' ')
    if len(modifier_list) != 2:
        raise ValueError("Two parameters are required: name and phone number (separated by a space)")
    if not (modifier_list[0] in phone_book):
        raise KeyError(f'Name {modifier_list[0]} not found in phone list')
    phone_book[modifier_list[0]].change_phone(Phone(value=modifier_list[1]))
    return f'Record {modifier_list[0]} changed in phone book'


@input_error
def handler_delete(name: str) -> str:
    if not (name in phone_book):
        raise KeyError(f'Name {name} not found in phone list')
    del phone_book[name]
    return f'Record {name} deleted'


@input_error
def handler_phone(name: str) -> str:
    if not (name in phone_book):
        raise KeyError(f'Name {name} not found in phone list')
    return phone_book[name].show_phone()


@input_error
def handler_find(find_text: str) -> str:
    return phone_book.find_record(find_text)


@input_error
def handler_del_phone(name: str) -> str:
    if not (name in phone_book):
        raise KeyError(f'Name {name} not found in phone list')
    result = phone_book[name].delete_phone()
    return result


@input_error
def handler_show_all(*args) -> str:
    if len(phone_book) == 0:
        return 'Phone book is empty'

    try:
        max_line = int(args[0])
    except ValueError:
        max_line = len(phone_book)
    result = 'Phone book:\n'
    num_page = 0
    for page in phone_book.iterator(max_line=max_line):
        num_page += 1
        result += f'<< page {num_page} >>\n' if max_line < len(phone_book) else ''
        result += page
    return result


@input_error
def handler_exit(*args):
    phone_book.save_book()
    raise SystemExit('Good bye!')


@input_error
def handler_error(*args):
    return "Use one of the available commands: 'add', 'change', 'phone', 'show all', 'exit', 'good bye', 'close' or '.'"


@input_error
def handler_save(*args):
    phone_book.save_book()
    return 'Address book saved'


@input_error
def handler_load(*args):
    phone_book.load_book()
    return 'Address book loaded'


handlers: Dict[str, Callable] = {
    'hello': handler_hello,
    'add': handler_add,
    'birthday': handler_birthday,
    'day of birthday': handler_day_of_birthday,
    'change': handler_change,
    'phone': handler_phone,
    'del': handler_delete,
    'delete': handler_delete,
    'del_phone': handler_del_phone,
    'show all': handler_show_all,
    'close': handler_exit,
    'good bye': handler_exit,
    'exit': handler_exit,
    '.': handler_exit,
    'find': handler_find,
    'error command': handler_error,
    'save': handler_save,
    'load': handler_load
}