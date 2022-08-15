from typing import Dict, Callable
from contacts import phone_book


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
    phone_book.add_record(modifier_list[0])
    phone_book[modifier_list[0]].add_phone(modifier_list[1])
    return 'Record added to phone book'


@input_error
def handler_change(modifier: str) -> str:
    modifier_list = modifier.split(' ')
    if len(modifier_list) != 2:
        raise ValueError("Two parameters are required: name and phone number (separated by a space)")
    if not (modifier_list[0] in phone_book):
        raise KeyError(f'Name {modifier_list[0]} not found in phone list')
    phone_book[modifier_list[0]].change_phone(modifier_list[1])
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
    result = ' {:^10} {:^15} '.format('Name', 'Number phone') + '\n'
    result = result + '-' * 28 + '\n'
    phone_list = '\n'.join('|{:^10}|{:<15} '.format(name, ' ' + record.show_phone())
                           for name, record in phone_book.items())
    result = result + phone_list + '\n' + '-' * 28
    return result


@input_error
def handler_exit(*args):
    raise SystemExit('Good bye!')


@input_error
def handler_error(*args):
    return "Use one of the available commands: 'add', 'change', 'phone', 'show all', 'exit', 'good bye', 'close' or '.'"


handlers: Dict[str, Callable] = {
    'hello': handler_hello,
    'add': handler_add,
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
    'error command': handler_error
}