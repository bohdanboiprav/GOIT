ADDRESSBOOK = {}


def input_error(inner):
    def wrap(*args):
        try:
            return inner(*args)
        except (KeyError, ValueError, IndexError) as e:
            if isinstance(e, KeyError):
                return "KeyError: Name not found in address book"
            elif isinstance(e, ValueError):
                return "ValueError: Give me name and phone please"
            elif isinstance(e, IndexError):
                return "IndexError: Give me name and phone please"
    return wrap


@input_error
def add_handler(data):
    name = data[0].title()
    phone = data[1]
    ADDRESSBOOK[name] = phone
    return f"Contact {name} with phone {phone} was saved"


@input_error
def change_handler(data):
    if data[0].title() in ADDRESSBOOK:
        name = data[0].title()
        phone = data[1]
        ADDRESSBOOK[name] = phone
        return f"Contact {name} phone was changed to {phone}"
    else:
        return f"{data[0]} is not in database. Use 'add' command"


def show_all_handler():
    return ADDRESSBOOK


@input_error
def phone_handler(data):
    name = data[0].title()
    if name in ADDRESSBOOK:
        return ADDRESSBOOK[name]


def exit_handler(*args):
    return "Good bye!"


def hello_handler(*args):
    return "Hello"


@input_error
def command_parser(raw_str: str):
    elements = raw_str.split()
    for key, value in COMMANDS.items():
        if elements[0].lower() in value:
            return key(elements[1:])
        elif raw_str in value:
            return key()
    return "Unknown command"


COMMANDS = {
    add_handler: ["add", "додай", "+"],
    exit_handler: ["good bye", "close", "exit"],
    hello_handler: ["hello"],
    change_handler: ["change"],
    show_all_handler: ["show all"],
    phone_handler: ["phone", "find"]

}


def main():
    while True:
        user_input = input(">>> ")
        result = command_parser(user_input)
        print(result)
        if result == "Good bye!":
            break


if __name__ == "__main__":
    main()
