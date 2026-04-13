import pytest

from main import format_surname, format_phone, merge_contacts, process_contacts


@pytest.mark.parametrize(
    "contact, expected",
    [
        (
            ["Иванов", "Иван", "Иванович", "Компания", "Инженер", "", "ivanov@mail.ru"],
            ["Иванов", "Иван", "Иванович", "Компания", "Инженер", "", "ivanov@mail.ru"],
        ),
        (
            ["Иванов Иван", "Иванович", "", "Компания", "Инженер", "", "ivanov@mail.ru"],
            ["Иванов", "Иван", "Иванович", "Компания", "Инженер", "", "ivanov@mail.ru"],
        ),
        (
            ["Иванов Иван Иванович", "", "", "Компания", "Инженер", "", "ivanov@mail.ru"],
            ["Иванов", "Иван", "Иванович", "Компания", "Инженер", "", "ivanov@mail.ru"],
        ),
        (
            ["Иванов", "Иван", "", "Компания", "Инженер", "", "ivanov@mail.ru"],
            ["Иванов", "Иван", "", "Компания", "Инженер", "", "ivanov@mail.ru"],
        ),
    ],
)
def test_format_surname(contact, expected):
    assert format_surname(contact) == expected


@pytest.mark.parametrize(
    "phone, expected",
    [
        ("8(999)1112233", "+7(999)111-22-33"),
        ("8 999 111 22 33", "+7(999)111-22-33"),
        ("+7(999)111-22-33", "+7(999)111-22-33"),
        ("+7 999 111 22 33", "+7(999)111-22-33"),
        ("8(999)111-22-33 доб.1234", "+7(999)111-22-33 доб.1234"),
        ("+7(999)1112233 доб.5678", "+7(999)111-22-33 доб.5678"),
    ],
)
def test_format_phone(phone, expected):
    assert format_phone(phone) == expected


def test_merge_contacts():
    contacts = [
        ["Иванов", "Иван", "Иванович", "Компания", "Инженер", "", ""],
        ["Иванов", "Иван", "Иванович", "", "", "+7(999)111-22-33", "ivanov@mail.ru"],
        ["Петров", "Петр", "Петрович", "Другая компания", "Менеджер", "+7(999)222-33-44", "petrov@mail.ru"],
    ]

    result = merge_contacts(contacts)

    assert len(result) == 2

    merged_ivanov = next(contact for contact in result if contact[0] == "Иванов" and contact[1] == "Иван")
    assert merged_ivanov == [
        "Иванов",
        "Иван",
        "Иванович",
        "Компания",
        "Инженер",
        "+7(999)111-22-33",
        "ivanov@mail.ru",
    ]


def test_process_contacts():
    contacts_list = [
        ["lastname", "firstname", "surname", "organization", "position", "phone", "email"],
        ["Иванов Иван", "Иванович", "", "Компания", "Инженер", "8(999)1112233", "ivanov@mail.ru"],
        ["Иванов", "Иван", "Иванович", "", "", "+7 999 111 22 33", ""],
        ["Петров", "Петр", "Петрович", "Другая компания", "Менеджер", "8(999)222-33-44", "petrov@mail.ru"],
    ]

    result = process_contacts(contacts_list)

    assert result[0] == ["lastname", "firstname", "surname", "organization", "position", "phone", "email"]
    assert len(result) == 3

    ivanov = next(contact for contact in result[1:] if contact[0] == "Иванов" and contact[1] == "Иван")
    assert ivanov == [
        "Иванов",
        "Иван",
        "Иванович",
        "Компания",
        "Инженер",
        "+7(999)111-22-33",
        "ivanov@mail.ru",
    ]

    petrov = next(contact for contact in result[1:] if contact[0] == "Петров" and contact[1] == "Петр")
    assert petrov == [
        "Петров",
        "Петр",
        "Петрович",
        "Другая компания",
        "Менеджер",
        "+7(999)222-33-44",
        "petrov@mail.ru",
    ]