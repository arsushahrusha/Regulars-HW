from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding="utf-8") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
#pprint(contacts_list)

def format_surname(contact):
    formatted = ' '.join(contact[:3]).split()
    while len(formatted)<3:
       formatted.append('') 
    formatted.extend(contact[3:])
    return formatted

def format_phone_pattern(match):
    main = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
    if match.group(7):
        return f"{main} {match.group(7)}{match.group(8)}"
    return main

def format_phone(phone):
    phone_pattern = r"(\+7|8)?\s*[(]?(\d{3})[)]?\D?(\d{3})\D?(\d{2})\D?(\d{2})(\s*[(]?(доб.)\s*(\d{4})[)]?)?"
    phone = re.sub(phone_pattern, format_phone_pattern, phone)
    return phone

def merge_contacts(contacts_list):
    merged_contacts = {}

    for contact in contacts_list:
        key = (contact[0], contact[1])

        if key in merged_contacts:
            existing_contact = merged_contacts[key]
            for i in range(len(contact)):
                if contact[i] and not existing_contact[i]:
                    existing_contact[i] = contact[i]
        else:
            merged_contacts[key] = contact

    return list(merged_contacts.values())

def process_contacts(contacts_list):
    header = contacts_list[0]
    raw_contacts = contacts_list[1:]

    formatted_contacts = []
    for contact in raw_contacts:
        contact = format_surname(contact)
        contact[5] = format_phone(contact[5])
        formatted_contacts.append(contact)

    merged = merge_contacts(formatted_contacts)
    return [header] + merged

def read_csv(file_path):
    with open(file_path, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        return list(rows)

def write_csv(file_path, data):
    with open(file_path, "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=",")
        datawriter.writerows(data)

if __name__ == "__main__":
    contacts_list = read_csv("phonebook_raw.csv")
    result = process_contacts(contacts_list)
    write_csv("phonebook.csv", result)