import uvicorn
from fastapi import FastAPI

from hotels import hotels_router

app = FastAPI()
app.include_router(hotels_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
