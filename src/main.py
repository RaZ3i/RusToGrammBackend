import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.config import LOGGING_CONFIG

from src.routers.auth import router as auth_router
from src.routers.profile_oper import router as profile_oper_router
from src.routers.user_information import router as user_information_router
from src.routers.chat import router as chat_router

app = FastAPI(title="RuStoGramm")
app.include_router(auth_router)
app.include_router(profile_oper_router)
app.include_router(user_information_router)
app.include_router(chat_router)

if __name__ == "__main__":
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = (
            "%(asctime)s " + LOGGING_CONFIG["formatters"]["access"]["fmt"]
    )
    uvicorn.run("main:app", host="0.0.0.0", port=8134, reload=True)


origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*'],
# )
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "PATCH", "PUT", "OPTIONS"],
    allow_headers=[
        "Content-Type",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

