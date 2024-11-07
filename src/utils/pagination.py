from fastapi import Query
from pydantic import BaseModel


class Pagination(BaseModel):
    perPage: int
    page: int


def pagination_params(
    page: int = Query(ge=1, required=False, default=1, le=50),
    perpage: int = Query(ge=1, le=100, required=False, default=3),
):
    return Pagination(page=page, perPage=perpage)
