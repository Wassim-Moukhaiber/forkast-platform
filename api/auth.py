"""
Forkast API Authentication
API Key validation for POS and admin endpoints
"""
import hashlib
from datetime import datetime
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from api.database import get_db
from api.config import settings
from api.models.db_models import APIKeyDB

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def hash_api_key(key: str) -> str:
    """SHA-256 hash of the API key for storage."""
    return hashlib.sha256(key.encode()).hexdigest()


def verify_api_key(
    api_key: str = Security(api_key_header),
    db: Session = Depends(get_db),
) -> APIKeyDB:
    """Validate API key from X-API-Key header."""
    if not api_key:
        raise HTTPException(status_code=401, detail="Missing X-API-Key header")

    # Check admin key first
    if api_key == settings.admin_api_key:
        return APIKeyDB(
            id=0,
            key_hash="admin",
            key_prefix="admin",
            name="Admin",
            permissions=["admin", "pos:read", "pos:write", "payments:read", "payments:write"],
            is_active=True,
        )

    # Look up in database
    key_hash = hash_api_key(api_key)
    db_key = db.query(APIKeyDB).filter(
        APIKeyDB.key_hash == key_hash,
        APIKeyDB.is_active == True,
    ).first()

    if not db_key:
        raise HTTPException(status_code=401, detail="Invalid or inactive API key")

    # Update usage tracking
    db_key.last_used_at = datetime.now()
    db_key.request_count += 1
    db.commit()

    return db_key


def require_permission(permission: str):
    """Factory: returns a dependency that checks for a specific permission."""
    def checker(key: APIKeyDB = Depends(verify_api_key)):
        if "admin" in key.permissions:
            return key
        if permission not in key.permissions:
            raise HTTPException(
                status_code=403,
                detail=f"API key lacks required permission: {permission}",
            )
        return key
    return checker
