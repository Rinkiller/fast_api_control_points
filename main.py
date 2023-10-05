# Необходимо создать API для управления списком пользователей 

# API должен содержать следующие конечные точки:
# — GET /users — возвращает список всех пользователей.
# — GET /users/{id} — возвращает пользователя с указанным идентификатором.
# — POST /users — добавляет нового пользователя.
# — PUT /users/{id} — обновляет пользователя с указанным идентификатором.
# — DELETE /users/{id} — удаляет пользователя с указанным идентификатором.

# Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку Pydantic.



from fastapi import FastAPI, HTTPException
import uvicorn
from typing import Optional, List
from pydantic import BaseModel
import databases
import sqlalchemy


app = FastAPI()

class User_Atr(BaseModel):
    name:str
    email: Optional[str] = None
    password:str

class User(User_Atr):
    id:int
    

users : List[User] = []

@app.get("/users", response_model=List[User])  #возвращает список всех пользователей
async def get_all_users():
    return users


@app.get("/users/{id}", response_model=User)  #возвращает пользователя с указанным идентификатором.
async def get_user_id(id:int):
    for user in users:
        if user.id == id:
            return user  
    return HTTPException(status_code=404, detail="User not found")

@app.post("/users/", response_model=User)  #добавляет нового пользователя.
async def create_new_user(uatr:User_Atr):
    user = User(id=len(users) + 1, **uatr.dict())
    users.append(user)
    return user  
    
@app.put("/users/{id}", response_model=User)  #возвращает пользователя с указанным идентификатором.
async def update_user_id(id:int, uatr:User_Atr):
    for user in users:
        if user.id == id:
            user.name = uatr.name
            user.email = uatr.email
            user.password = uatr.password
            return user  
    return HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{id}", response_model=dict)  #возвращает пользователя с указанным идентификатором.
async def delete_user_id(id:int):
    for user in users:
        if user.id == id:
            users.remove(user)
            return {'message': f'User (id={id}) is removed of list users'}  
    return HTTPException(status_code=404, detail="User not found")


if __name__=="__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)