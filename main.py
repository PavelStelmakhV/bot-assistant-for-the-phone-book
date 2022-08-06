phone_book = {}


def string_parsing(string: str):
    if string.lower() in ['.', 'exit', 'good bye', 'close']:
        return 'exit', None
    elif string.lower() == 'hello':
        return 'hello', None
    elif string.lower() == 'show all':
        return 'show all', None

    input_list = string.split(' ')
    if input_list[0].lower() in ['add', 'change', 'phone']:
        return input_list[0].lower(), ' '.join(input_list[1::])

    return 'error command', None


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


@input_error
def hendler_add(modifier: str) -> str:
    modifier_list = modifier.split(' ')
    if len(modifier_list) < 2:
        raise ValueError("Incomplete command modifier. Give me name and phone please (separated by a space)")
    if len(modifier_list) > 2:
        raise ValueError("Two parameters are required: name and phone number (separated by a space)")
    if not modifier_list[1].isdigit():
        raise ValueError("Phone number must contain only digits")

    phone_book[modifier_list[0]] = modifier_list[1]
    return 'Record added to phonebook'


@input_error
def hendler_change (modifier: str) -> str:
    modifier_list = modifier.split(' ')
    if len(modifier_list) < 2:
        raise ValueError("Incomplete command modifier. Give me name and phone please (separated by a space)")
    if len(modifier_list) > 2:
        raise ValueError("Two parameters are required: name and phone number (separated by a space)")
    if not modifier_list[1].isdigit():
        raise ValueError("Phone number must contain only digits")
    if not (modifier_list[0] in phone_book):
        raise KeyError(f'Name {modifier_list[0]} not found in phone list')

    phone_book[modifier_list[0]] = modifier_list[1]
    return f'Record {modifier_list[0]} changed in phonebook'


@input_error
def hendler_phone (modifier: str) -> str:
    if not (modifier in phone_book):
        raise KeyError(f'Name {modifier} not found in phone list')
    return phone_book[modifier]


def main():
    while True:
        input_srting = input()
        command, modifier = string_parsing(input_srting)

        if command == 'hello':
            print('How can I help you?')
        elif command == 'exit':
            print('Good bye!')
            break
        elif command == 'add':
            print(hendler_add(modifier))
        elif command == 'change':
            print(hendler_change(modifier))
        elif command == 'phone':
            print(hendler_phone(modifier))
        elif command == 'show all':
            print('-' * 28)
            print('|{:^10}|{:^15}|'.format('Name', 'Number phone'))
            print('-' * 28)
            for name, phone_num in phone_book.items():
                print('|{:^10}|{:<15}|'.format(name, ' '+phone_num))
            print('-' * 28)
        elif command == 'error command':
            print("Use one of the available commands: 'add', 'change', 'phone', 'show all', 'exit', 'good bye', 'close' or '.'")


if __name__ == '__main__':
    main()

