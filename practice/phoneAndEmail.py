#! /usr/bin/env python3
# phoneAndEmail.py - Search phone number and e-mail

import pyperclip, re

# Regular expression of phone number (for U.S.A.)
phone_regex = re.compile(r'''(
    (\d{3}|\(\d{3}\))?              # 市外局番
    (\s|-|\.)?                      # 区切り
    (\d{3})                         # 3桁の番号
    (\s|-|\.)?                      # 区切り
    (\d{4})                         # 4桁の番号
    (\s*(ext|x|ext.)\s*(\d{2,5}))?  # 内線番号
    )''', re.VERBOSE)

# Regular expression for e-mail
email_regex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+               # ユーザ名
    @                               # @
    [a-zA-Z0-9.-]+                  # ドメイン名
    (\.[a-zA-Z]{2,4})               # ドット何とか
    )''', re.VERBOSE)

# Search in the text of clip board
text = str(pyperclip.paste())
matches = []
for groups in phone_regex.findall(text):
    phone_num = '-'.join(groups[1], groups[3], groups[5])
    if groups[8] != '':
        phone_num += ' x' + groups[8]
    matches.append(phone_num)
for groups in email_regex.findall(text):
    matches.append(groups[0])




