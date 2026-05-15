# Псевдокод:
# Імпортувати UserDict з модуля collections.
# Створити базовий клас Field для зберігання значення поля.
# Створити клас Name для імені контакту.
# Створити клас Phone для телефону з перевіркою на 10 цифр.
# Створити клас Record для одного контакту: ім'я + список телефонів.
# Створити клас AddressBook для зберігання всіх контактів.
# Створити декоратор input_error для обробки помилок введення.
# Розділити введення користувача на команду та аргументи.
# Додати CLI-команди: hello, add, change, phone, all.
# Запустити цикл роботи бота.
# Обробляти команди користувача.
# Якщо команда невідома — виводити повідомлення про помилку.
# Завершувати роботу командою exit.

from collections import UserDict


class Field:
    # Базовий клас для полів запису
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    # Клас для зберігання імені контакту
    pass


class Phone(Field):
    # Клас для зберігання телефону з валідацією
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)


class Record:
    # Клас для зберігання одного контакту
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        # Додаємо телефон до контакту
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        # Видаляємо телефон з контакту
        phone_to_remove = self.find_phone(phone)

        if phone_to_remove:
            self.phones.remove(phone_to_remove)

    def edit_phone(self, old_phone, new_phone):
        # Редагуємо існуючий телефон
        phone_to_edit = self.find_phone(old_phone)

        if phone_to_edit is None:
            raise ValueError("Phone not found.")

        phone_to_edit.value = Phone(new_phone).value

    def find_phone(self, phone):
        # Шукаємо телефон у контакті
        for item in self.phones:
            if item.value == phone:
                return item

        return None

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    # Клас для зберігання адресної книги
    def add_record(self, record):
        # Додаємо запис до адресної книги
        self.data[record.name.value] = record

    def find(self, name):
        # Шукаємо запис за іменем
        return self.data.get(name)

    def delete(self, name):
        # Видаляємо запис за іменем
        if name in self.data:
            del self.data[name]


def input_error(func):
    # Декоратор для обробки помилок введення
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as error:
            return str(error)
        except KeyError:
            return "Enter user name."
        except IndexError:
            return "Give me name and phone please."
        except AttributeError:
            return "Contact not found."

    return inner


def parse_input(user_input):
    # Розділяємо введений текст на команду та аргументи
    parts = user_input.split()

    if not parts:
        return "", []

    command = parts[0].lower()
    args = parts[1:]

    return command, args


@input_error
def add_contact(args, book):
    # Додаємо новий контакт або новий телефон до існуючого контакту
    if len(args) < 2:
        raise IndexError

    name, phone = args

    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    else:
        record.add_phone(phone)

    return "Contact added."


@input_error
def change_contact(args, book):
    # Змінюємо телефон існуючого контакту
    if len(args) < 3:
        return "Give me name, old phone and new phone please."

    name, old_phone, new_phone = args

    record = book.find(name)

    if record is None:
        raise AttributeError

    record.edit_phone(old_phone, new_phone)

    return "Contact updated."


@input_error
def show_phone(args, book):
    # Показуємо телефони контакту за іменем
    if len(args) < 1:
        raise IndexError

    name = args[0]
    record = book.find(name)

    if record is None:
        raise AttributeError

    return "; ".join(phone.value for phone in record.phones)


@input_error
def show_all(book):
    # Показуємо всі контакти
    if not book.data:
        return "No contacts."

    result = ""

    for record in book.data.values():
        result += str(record) + "\n"

    return result.strip()


def main():
    # Створюємо нову адресну книгу
    book = AddressBook()

    print("Welcome to the Jarvis assistant!")

    while True:
        # Отримуємо команду від користувача
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        # Привітання
        if command == "hello":
            print("How can I help you sir?")

        # Додати контакт або телефон
        elif command == "add":
            print(add_contact(args, book))

        # Змінити телефон контакту
        elif command == "change":
            print(change_contact(args, book))

        # Показати телефони контакту
        elif command == "phone":
            print(show_phone(args, book))

        # Показати всі контакти
        elif command == "all":
            print(show_all(book))

        # Завершення роботи бота
        elif command in ["exit"]:
            print("Good bye sir!")
            break

        # Якщо команда невідома
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()