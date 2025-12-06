from typing import Any
from uuid import UUID

import jwt
from fastapi import HTTPException, Cookie

from bootstrap.settings import get_settings


def get_user_id(
    access_token: str | None = Cookie(default=None)
) -> UUID:
    settings = get_settings()

    if access_token is None:
        raise HTTPException(status_code=401, detail="No access token")

    try:
        payload: dict[str, Any] = jwt.decode(
            access_token,
            settings.auth.secret_key,
            algorithms=[settings.auth.algorithm],
        )

    except jwt.InvalidTokenError:
        raise # todo дописать Exception

    user_id: str | None = payload.get("user_id", None)

    if user_id:
        return UUID(user_id)

    raise # todo дописать Exception