import uvicorn
from fastapi import FastAPI, Path
from typing import Annotated

from users.routes import router as users_router

app = FastAPI()
app.include_router(users_router)

@app.get("/")
async def root():
    return {"message": "Hello World!!"}


@app.get("/hello")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/item/{item_id}")
async def say_hello(item_id: Annotated[int, Path(ge=0, lt=100000000)]):
    return {"item" : {
        "id": item_id,
    }}

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
