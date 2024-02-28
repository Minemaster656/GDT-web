from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse

import DB
import Data
import Utils

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/items/{item_id}")
async def read_item(request: Request, item_id: int):
    item = DB.db.find_one({"_id": item_id})
    return templates.TemplateResponse("item.html", {"request": request, "item": item})
@app.get("/register")
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/API/register")
async def register_user(request: Request):
    data = await request.json()

    if not data:
        raise HTTPException(status_code=400, detail="No data provided")

    username = data.get("username")
    login = data.get("login")
    password = data.get("password")
    password1 = data.get("password1")

    # Проверка и обработка данных для регистрации пользователя
    # ...
    hashed_password = Utils.hash_password(password)
    hashed_password1 = Utils.hash_password(password1)

    registration_successful = False
    message=""
    if hashed_password==hashed_password1:
        doc = DB.db.users.find_one({"login": login})
        if not doc:
            DB.addUser(username, login, hashed_password)
            registration_successful = True
        else:
            message="Пользователь с таким логином уже существует"
    else:
        message="Пароли не совпадают"


    # Возвращение результата регистрации
    if registration_successful:
        return {"success": True, "message": "Пользователь успешно зарегистрирован"}
    else:
        return {"success": False, "message": f"Ошибка при регистрации: {message}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=Data.PORT)
