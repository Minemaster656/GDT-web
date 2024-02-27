import os

if not os.path.exists("private/Core.py"):
    os.mkdir("private")
    with open("private/Core.py", "w") as file:
        file.write('import os\n')
        file.write('#os.system("python -m pip install -r requirements.txt")\n')
        file.write('DB_ADDRESS="mongodb://localhost:27017"\n')
        file.write('DB_NAME="GDTWeb_data"\n')
        print("File private/Core.py created successfully.")
else:
    print("File private/Core.py already exists.")

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
