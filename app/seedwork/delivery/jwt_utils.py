from typing import Any
from uuid import UUID

import jwt
from fastapi import HTTPException, Cookie, Header

from bootstrap.settings import get_settings


def get_user_id(
    access_token_cookie: str | None = Cookie(default=None),
    authorization: str | None = Header(default=None),
) -> UUID:
    settings = get_settings()

    token = None

    # Prefer cookie token
    if access_token_cookie:
        token = access_token_cookie

    # Fallback to Authorization header
    elif authorization and authorization.startswith("Bearer "):
        token = authorization.removeprefix("Bearer ")

    if token is None:
        raise HTTPException(status_code=401, detail="No access token")

    try:
        payload: dict[str, Any] = jwt.decode(
            token,
            settings.auth.secret_key,
            algorithms=[settings.auth.algorithm],
        )

    except jwt.InvalidTokenError:
        raise # todo дописать Exception

    user_id: str | None = payload.get("user_id", None)

    if user_id:
        return UUID(user_id)

    raise HTTPException(status_code=401, detail="Invalid token payload")