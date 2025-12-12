from fastapi import Header, HTTPException
from typing import Optional
from app.utils.security import SecurityUtil
from jose import JWTError


class AuthMiddleware:
    @staticmethod
    async def verify_token(authorization: Optional[str] = Header(None)) -> dict:
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        try:
            scheme, token = authorization.split()
            if scheme.lower() != "bearer":
                raise HTTPException(status_code=401, detail="Invalid authentication scheme")

            payload = SecurityUtil.decode_token(token)
            return payload
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid authorization header format")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid or expired token")