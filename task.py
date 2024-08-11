def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (IndexError, ValueError) as e:
            return str(e)
    return wrapper

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    if old_phone in record.phones:
        record.phones[record.phones.index(old_phone)] = new_phone
        return "Phone number updated."
    else:
        raise ValueError("Old phone number not found.")

@input_error
def phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    return ", ".join(record.phones)

@input_error
def all_contacts(args, book: AddressBook):
    return [f"{record.name}: {', '.join(record.phones)}" for record in book.records]

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    record.add_birthday(birthday)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise ValueError("Contact not found.")
    if record.birthday is None:
        return "Birthday not set."
    return str(record.birthday)

@input_error
def birthdays(args, book: AddressBook):
    return book.get_upcoming_birthdays()


def parse_input(user_input):
    return user_input.strip().split()

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(phone(args, book))

        elif command == "all":
            print(all_contacts(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")
