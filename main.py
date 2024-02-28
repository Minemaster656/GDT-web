from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import config
import userdata

if __name__ == "__main__":
    import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# FIXME: потенциально небезопасно!!!!!
@app.get("/items/{item_id}")
async def read_item(request: Request, item_id: int):
    # pylint: disable=protected-access
    item = userdata.database.__db.find_one({"_id": item_id})
    # pylint: enable=protected-access
    return templates.TemplateResponse("item.html", {"request": request, "item": item})

@app.get("/register")
async def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/API/register")
async def register_user(request: Request):
    return await userdata.registration.register_user(request)

if __name__ == "__main__":
    uvicorn.run(app, host=config.HOST, port=config.PORT)
