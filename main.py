from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_418_IM_A_TEAPOT, HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

import DB
import Data
import TEMPLATES
import Utils

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.middleware("http")
async def validate_request(request: Request, call_next):
    if request.url.path.startswith("/AJAX"):
        origin = request.headers.get("origin")
        user_agent = request.headers.get("user-agent")

        if origin not in Data.DOMAINS:  # or "Mozilla" not in user_agent
            print(origin)
            raise HTTPException(status_code=418)
            # return {"success": False, "message": f"Ошибка при регистрации: вы чайник!"}

    response = await call_next(request)
    return response


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request, "header": TEMPLATES.HEADER, "head": TEMPLATES.HEAD_CONTENT})


@app.get("/items/{item_id}")
async def read_item(request: Request, item_id: int):
    item = DB.db.find_one({"_id": item_id})
    return templates.TemplateResponse("item.html", {"request": request, "item": item})
@app.get("/user/{username}")
async def read_user(request: Request, username: str):
    doc = DB.db_rtb.users.find_one({"username": username})
    if doc:
        doc = DB.schema(doc, DB.Schemes.RTB_user)
        def makeActivityHistory(history):
            return str(history)
        print("#"+(str(hex(doc["color"]))[2:]))
        return templates.TemplateResponse("user.html", {"request": request,
                                                        "header": TEMPLATES.HEADER, "head": TEMPLATES.HEAD_CONTENT,
                                                        "username":username,
                                                        "about":doc["about"],
                                                        # "avatar":doc["avatar"],
                                                        "userid":doc["userid"],
                                                        "age":doc["age"],
                                                        "timezone":doc["timezone"],
                                                        "color":"#"+(str(hex(doc["color"]))[2:]) if doc["color"] else "#5865F2", "color_glow":"#"+(str(hex(doc["color"]))[2:])+"a4" if doc["color"] else "#5865F2a4",
                                                        "karma":doc["karma"],
                                                        "luck":doc["luck"],
                                                        "permissions":doc["permissions"],
                                                        "money":doc["money"],
                                                        "money_bank":doc["money_bank"],
                                                        "xp":doc["xp"],
                                                        "banned":doc["banned"],
                                                        "autoresponder": 'Вкл.' if doc["autoresponder"] else 'Выкл.',
                                                        "autoresponder-inactive":doc["autoresponder-inactive"],
                                                        "autoresponder-offline":doc["autoresponder-offline"],
                                                        "autoresponder-disturb":doc["autoresponder-disturb"],
                                                        "premium_end":doc["premium_end"],

                                                        "activity_changes":makeActivityHistory(doc["activity_changes"]),})
    else:
        return templates.TemplateResponse("c404.html", {"request": request,
                                                        "header": TEMPLATES.HEADER, "head": TEMPLATES.HEAD_CONTENT})

@app.get("/register")
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/character/{id}")
async def read_character_by_id(request: Request, id: str):
    doc = DB.db_rtb.characters.find_one({"id": id})
    # print(doc)
    def strToHTMLstr(s):
        s = s.replace("\n", "<br>")
        s = s.replace("\\n", "<br>")
        s = s.replace("\\\\n", "<br>")
        s = Utils.str_to_HTML(s)
        return s

    if doc:
        print(doc)
        return templates.TemplateResponse("character.html", {"request": request,
                                                             "header": TEMPLATES.HEADER,
                                                             "head": TEMPLATES.HEAD_CONTENT,
                                                             "character": doc,
                                                             "art": doc["art"],
                                                             "name": doc["name"],
                                                             "shortened": strToHTMLstr(doc["shortened"]),
                                                             "bio": strToHTMLstr(doc["bio"]),
                                                             "bodystats": strToHTMLstr(doc["bodystats"]),
                                                             "age": doc["age"],
                                                             "abilities": strToHTMLstr(doc["abilities"]),
                                                             "weaknesses": strToHTMLstr(doc["weaknesses"]),
                                                             "appearances": strToHTMLstr(doc["appearances"]),
                                                             "inventory": strToHTMLstr(doc["inventory"]),
                                                             "owner": doc["owner"]
                                                             })
    else:
        # return templates.TemplateResponse("character_not_found.html", {"request": request,
        #                                                                "header": TEMPLATES.HEADER,
        #                                                                "head": TEMPLATES.HEAD_CONTENT,
        #                                                                "id": id
        #                                                                })
        return templates.TemplateResponse("c404.html", {"request": request,
                                                                       "header": TEMPLATES.HEADER,
                                                                       "head": TEMPLATES.HEAD_CONTENT,
                                                                       "id": id
                                                                       })


@app.get("/characters/register")
async def read_characters_register(request: Request):
    return templates.TemplateResponse("character_register.html", {"request": request,
                                                                       "header": TEMPLATES.HEADER,
                                                                       "head": TEMPLATES.HEAD_CONTENT,
                                                                  })

@app.post("/AJAX/API/register")
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
    hashed_password = Utils.hash_SHA3_str(password)
    hashed_password1 = Utils.hash_SHA3_str(password1)

    registration_successful = False
    message = ""
    if hashed_password == hashed_password1:

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
