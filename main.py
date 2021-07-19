from typing import Optional

from fastapi import FastAPI, HTTPException

from pydantic import BaseModel # pylint: disable=no-name-in-module

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

app.mount("/static", StaticFiles(directory = "static"), name="static")

templates = Jinja2Templates(directory="templates")

listUsers = []

class Item(BaseModel): 
    item_id: int
    username: str
    email: str
    phone: Optional[str] = None # pylint: disable=unsubscriptable-object

class MyException(Exception):
    def __init__(self, message="Some Error"):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return f'{self.message}'

@app.get("/", response_class=HTMLResponse)
async def read_list(request: Request):
    if len(listUsers)!=0:
        return templates.TemplateResponse("index.html", {
                "request": request,
                "id": listUsers
            })
    raise HTTPException(status_code=404)


def get_one(item_id: int):
    for i in listUsers:
        if i.item_id == item_id:
            return i
    raise MyException("Item not found")

@app.get("/{item_id}", response_class=HTMLResponse)
def get_one_api(request: Request, item_id: int):
    try: 
        obj = get_one(item_id)
        return templates.TemplateResponse("item.html", {
            "request": request,
            "id": obj.item_id,
            "username": obj.username,
            "email": obj.email,
            "phone": obj.phone
        })
    except Exception as e:
        raise HTTPException(status_code=404, detail=e)


@app.post("/{item_id}/edit")
def post_data(item_id: int, objItem: Item):
    for i in range(len(listUsers)):
        if listUsers[i].item_id == item_id:
            listUsers[i] = objItem
            return listUsers[i]
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/{item_id}/delete")
def del_data(item_id: int):
    for i in range(len(listUsers)):
        if listUsers[i].item_id == item_id:
            return listUsers.pop(i)
    raise HTTPException(status_code=404, detail="Item not found")


@app.put("/{item_id}/create")
def put_data(item_id: int, username: str, email: str, phone: str = None):
    for i in range(len(listUsers)):
        if listUsers[i].item_id == item_id:
            raise HTTPException(status_code=404, detail=f"The user {item_id} already exists")
    objItem=Item(
        item_id=item_id,
        username=username,
        email=email,
        phone=phone
    )
    listUsers.append(objItem)
    return objItem

@app.exception_handler(StarletteHTTPException)
async def my_custom_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse('error.html', {
            'request': request,
            'status_code': exc.status_code,
            'detail': exc.detail
        })
    else:
        # Just use FastAPI's built-in handler for other errors
        return await http_exception_handler(request, exc)

