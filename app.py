from fastapi import FastAPI, Request, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordBearer

tags_metadata = [
    {
        "name": "Business",
        "description": "",
    },
    {
        "name": "Users",
        "description": "",
    },
    {
        "name": "Roles",
        "description": "",
    },
    {
        "name": "Bookings",
        "description": "",
    },
    {
        "name": "Customers",
        "description": "",
    },
    {
        "name": "Transactions",
        "description": "",
    },
    {
        "name": "Invoices",
        "description": "",
    },
    {
        "name": "Payments",
        "description": "",
    },
    {
        "name": "Prices",
        "description": "",
    },
    {
        "name": "Discounts",
        "description": "",
    },
    {
        "name": "Banks",
        "description": "",
    },
    {
        "name": "Services",
        "description": "",
    },
    {
        "name": "Persons",
        "description": "",
    },
]

app = FastAPI(
    title="API Endpoints",
    description="Puedes volver <a href='/'>haciendo clic aquí</a>. <br>Puedes cambiar la operativa <a href='/docs'>haciendo clic aquí</a>",
    version="1.0.0",
    openapi_tags=tags_metadata
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse, 
summary="Dashboard",
include_in_schema=False)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/account", response_class=HTMLResponse,
summary="Login",
include_in_schema=False)
def account(request: Request):
    return templates.TemplateResponse("sign-in.html", {"request": request})


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    username: str
    has_permission: bool = False

def fake_decode_token(token: str):
    return User(username=token)

def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

class Business:

    class Business(BaseModel):
        name: str
        description: Optional[str] = None
        price: float
        tax: Optional[float] = None

    object = {}

    @app.post("/business", tags=["Business"])
    async def create_business(item: Business, user: User = Depends(get_current_user)):
        if not user.has_permission:
            raise HTTPException(status_code=400, detail="No tienes permiso para crear items.")
        return {"item": item}


    @app.get("/items/{item_id}", tags=["Bookings"])
    async def read_item(item_id: int):
        item = Business.object.get(item_id, None)
        if item is None:
            return {"message": "Item not found."}
        return item

    @app.put("/items/{item_id}", tags=["Bookings"])
    async def update_item(item_id: int, item: Business):
        Business.object[item_id] = item
        return {"message": "Item updated successfully."}

    @app.delete("/items/{item_id}", tags=["Bookings"])
    async def delete_item(item_id: int):
        if item_id in Business.object:
            del Business.object[item_id]
            return {"message": "Item deleted successfully."}
        else:
            return {"message": "Item not found."}
