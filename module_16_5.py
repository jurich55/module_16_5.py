from fastapi import FastAPI, Request, HTTPException, Body, Form
from fastapi import HTTPException, status
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int

@app.get("/")
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse("users.html",
            {"request": request, "users": users})

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int):
    try:
        user = next(user for user in users if user.id == user_id)
        return templates.TemplateResponse("users.html",
            {"request": request, "user": user})
    except IndexError:
        raise HTTPException(status_code=404, detail="user not found")

@app.delete('/user/{user_id}', response_model=User)
async def delete_user(user_id: int)-> User:
    if user_id != User(id=user_id):
        raise HTTPException(status_code=404, detail="User was not found")

    # Удаляем пользователя и возвращаем его
    deleted_user = users.pop(user_id - 1)
    return deleted_user

@app.post("/user", response_class=HTMLResponse)
async def user_post(request: Request, username: str = Form(),
                    age: int = Form()) -> HTMLResponse:

    user_id = users[-1].id + 1 if users else 1     # Генерация ID
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)               # Добавление пользователя
    return templates.TemplateResponse("users.html",
            {"request": request, "user": users})

@app.put('/user/{user_id}/{username}/{age}', response_model=User)
async def update_users(user_id:int, username:str, age:int) ->User:
                # Обновляем данные пользователя
    if user_id != User(id=user_id):  # существует ли пользователь?
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = User(id=user_id, username=username, age=age)
    users[user_id - 1] = updated_user   # учитываем индексацию с 0
    return updated_user




#   uvicorn module_16_5:app --reload
#   http://127.0.0.1:8000/user
#   http://127.0.0.1:8000/docs
