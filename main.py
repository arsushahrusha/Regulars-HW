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

merged_contacts = {}

for i in range (1, len(contacts_list)):
    contacts_list[i] = format_surname(contacts_list[i])
    contacts_list[i][5] = format_phone(contacts_list[i][5])

    key = (contacts_list[i][0], contacts_list[i][1])
    if key in merged_contacts:
        exist = merged_contacts[key]
        for j in range(len(contacts_list[i])):
            if contacts_list[i][j] and not exist[j]:
                exist[j] = contacts_list[i][j]
    else:
        merged_contacts[key] = contacts_list[i]

result = [contacts_list[0]]
result.extend(merged_contacts.values())

with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerows(result)