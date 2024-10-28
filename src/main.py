# import os
# import sys
#
# sys.path.insert(1, ".routers")
# sys.path.insert(2, ".schemas")
import uvicorn
from fastapi import FastAPI
from src.routers.auth import router as auth_router


app = FastAPI(title="RuStoGramm")
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8133, reload=True)
