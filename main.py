import asyncio
import time

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette import status
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_418_IM_A_TEAPOT, HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS

import DB
import Data
import TEMPLATES
import Utils

import API_data

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

@app.post("/API/AJAX/regchar")
async def regchar(request: Request):
    # Ваша логика обработки данных
    data = await request.json()



    if not data:
        return JSONResponse(content={"message": "Invalid data"}, status_code=204)
    else:
        tempdoc = DB.db_rtb.characters.find_one({"id": data["id"]})
        if tempdoc:
            return JSONResponse(content={"message": "Такой персонаж уже есть!"}, status_code=409)
        tempdoc = DB.db_rtb.moderating_characters.find_one({"id": data["id"]})
        if tempdoc:
            return JSONResponse(content={"message": "Такой персонаж уже есть!"}, status_code=409)
        userdoc = DB.getRTBUser(data["owner"])
        if data["token"]!=userdoc["access_token"] or userdoc["access_token_expires"]<time.time():
            return JSONResponse(content={"message": "Invalid token"}, status_code=498)
        else:
            mask ={"name": None, "bodystats": None, "age": None,
            "abilities": None, "weaknesses": None, "character": None,
            "inventory": None, "bio": None, "appearances": None,
            "art": "https://media.discordapp.net/attachments/1018886769619505212/1176561157939662978/ad643992b38e34e2.png",
            "shortened": None, "id": None, "owner": 0,
            "prefix": None, "totalMessages": 0}
            doc = DB.maskDoc(mask, data)
            DB.db_rtb.moderating_characters.insert_one(doc)
            DB.db_rtb.users.update_one({"userid": userdoc["userid"]}, {"$set": {"access_token_expires":0}})
            # DB.db_rtb.requests.insert_one({"type":"regchar", "userid":data["owner"], "id":data['id']})


            return JSONResponse(content={"message": "Отправлено на обработку..."}, status_code=201)
    return JSONResponse(content={"message": "Unknown error"}, status_code=418)
    # if data:
    #     return JSONResponse(content={"message": "Data received successfully"}, status_code=201)
    # else:
    #     return JSONResponse(content={"message": "Error processing data"}, status_code=400)
@app.get("/API/getstatus")
async def return_status_code():
    return JSONResponse(content={"message": "Ok"}, status_code=status.HTTP_200_OK)
@app.get("/API/remote_commands_pc_api/setcommand")
async def get_headers(command: str, expire_seconds: int,
                      token: str = Header(None), code: int = Header(None)):
    doc = DB.db_rtb.api_keys.find_one({"token": token})
    if doc:
        if doc['mass_command_api_code']==code:
            API_data.remote_commands_pc_api[command] = {"expire_time": time.time() + expire_seconds, "command": command}
            return JSONResponse(content={"message": "Created"}, status_code=status.HTTP_201_CREATED)
        else:
            return JSONResponse(content={"message": "Forbidden"}, status_code=status.HTTP_403_FORBIDDEN)
    else:
        return JSONResponse(content={"message": "Unauthorized"}, status_code=status.HTTP_401_UNAUTHORIZED)


@app.get("/API/remote_commands_pc_api/getcommand")
async def return_status_code(code:int):
    if code in API_data.remote_commands_pc_api.keys():
        return JSONResponse(content={"message": API_data.remote_commands_pc_api[code]["command"]}, status_code=status.HTTP_200_OK)
    else:
        return JSONResponse(content={"message": "None"}, status_code=status.HTTP_404_NOT_FOUND)







async def loop():
    while True:
        # for i in API_data.remote_commands_pc_api:
        #     if i["expire_time"]<time.time():
        #         API_data.remote_commands_pc_api.pop(i)
        for k in API_data.remote_commands_pc_api.keys():
            if API_data.remote_commands_pc_api[k]["expire_time"]<time.time():
                API_data.remote_commands_pc_api.pop(k)





        await asyncio.sleep(1)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(loop())
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=Data.PORT)
