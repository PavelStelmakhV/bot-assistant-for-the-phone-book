from handlers import handlers
from parser import string_parsing


def main():
    while True:
        input_user = input()
        command, modifier = string_parsing(input_user)
        function_handler = handlers.get(command)
        try:
            print(function_handler(modifier))
        except SystemExit as e:
            print(e)
            break


if __name__ == '__main__':
    main()

