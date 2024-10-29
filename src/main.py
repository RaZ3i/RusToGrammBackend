# import os
# import sys
#
# sys.path.insert(1, ".routers")
# sys.path.insert(2, ".schemas")
import uvicorn
from fastapi import FastAPI
from src.routers.auth import router as auth_router
from src.routers.profile_oper import router as profile_oper_router

app = FastAPI(title="RuStoGramm")
app.include_router(auth_router)
app.include_router(profile_oper_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8134, reload=True)
