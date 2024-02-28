from fastapi import Request, HTTPException
from starlette.responses import JSONResponse

from . import database

async def register_user(request: Request):
    data = await request.json()

    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    username = data.get("username")
    login = data.get("login")
    password = data.get("password")

    registration_successful = False
    message = "Неизвестная ошибка"

    doc = database.find_user({"login": login})
    if not doc:
        database.add_user(username, login, password)
        registration_successful = True
    else:
        message = "Пользователь с таким логином уже существует"

    if registration_successful:
        return {"success": True, "message": "Пользователь успешно зарегистрирован"}
    else:
        return {"success": False, "message": message}