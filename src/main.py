import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import hotels_router


app = FastAPI()
app.include_router(hotels_router)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
