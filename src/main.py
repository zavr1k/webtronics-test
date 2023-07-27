import fastapi_users
from fastapi import FastAPI
from sqlalchemy.exc import NoResultFound

from auth.config import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead
from exception_handler import sqlalchemy_no_result_handler
from post.router import router as post_router

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
app.include_router(post_router)
app.add_exception_handler(NoResultFound, sqlalchemy_no_result_handler)
