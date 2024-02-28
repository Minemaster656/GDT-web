# Зачем... Не знаю, но оставлю.

import os

if not os.path.exists("templates"):
    os.mkdir("templates")
    print("TEMPLATES FOLDER CREATED")
else:
    print("TEMPLATES FOLDER ALREADY EXISTS")

if not os.path.exists("static"):
    os.mkdir("static")
    print("STATIC FOLDER CREATED")
else:
    print("STATIC FOLDER ALREADY EXISTS")
