# import os
# import sys
#
# sys.path.insert(1, ".routers")
# sys.path.insert(2, ".schemas")

from fastapi import FastAPI
from .routers.auth import router as auth_router


app = FastAPI(title="RuStoGramm")
app.include_router(auth_router)
