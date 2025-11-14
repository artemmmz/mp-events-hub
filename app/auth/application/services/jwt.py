from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Optional
import jwt

from seedwork.application.service import BaseService


@dataclass
class JwtService(BaseService):
    _secret_key: str
    _access_token_lifetime: int
    _algorithm: str = "HS256"

    def issue_token(self, payload: dict[str, Any]) -> str:
        exp: datetime = datetime.now(tz=timezone.utc) + timedelta(seconds=self._access_token_lifetime)
        to_encode = payload.copy()
        to_encode["exp"] = exp
        return jwt.encode(to_encode, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> Optional[dict[str, Any]]:
        """
        Возвращает payload, если токен валиден, иначе None.
        """
        try:
            return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
        except jwt.InvalidTokenError:
            return None