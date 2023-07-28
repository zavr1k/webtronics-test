from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import NoResultFound


async def sqlalchemy_no_result_handler(request: Request, exception: NoResultFound):
    return JSONResponse(
        "Object not found",
        status_code=status.HTTP_404_NOT_FOUND,
    )
