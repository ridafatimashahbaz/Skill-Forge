from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .security import decode_token

bearer_scheme = HTTPBearer()


def get_current_claims(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    try:
        return decode_token(creds.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


def require_role(*roles: str):
    def checker(claims: dict = Depends(get_current_claims)) -> dict:
        if claims.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return claims
    return checker
