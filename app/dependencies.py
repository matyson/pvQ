from .env import Settings
from fastapi import HTTPException, Depends
from fastapi.security import APIKeyCookie
from typing import Annotated

config = Settings()

token_scheme = APIKeyCookie(name="access_token")


async def verify_token(token: Annotated[str, Depends(token_scheme)]):
    if token != config.secret:
        raise HTTPException(status_code=403, detail="Unauthorized")