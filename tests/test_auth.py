import pytest
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.dependencies import get_current_user
from datetime import timedelta
from fastapi import HTTPException
import jwt
from app.core.config import settings

def test_password_hashing():
    pwd = "my_super_password"
    hash1 = get_password_hash(pwd)
    hash2 = get_password_hash(pwd)
    
    # Verify different hashes for same password (salting)
    assert hash1 != hash2
    
    # Verify both hashes validate the same password
    assert verify_password(pwd, hash1) is True
    assert verify_password(pwd, hash2) is True
    
    # Verify wrong password fails
    assert verify_password("wrong", hash1) is False

@pytest.mark.asyncio
async def test_expired_jwt():
    # Create expired token
    token = create_access_token(data={"sub": "admin"}, expires_delta=timedelta(minutes=-1))
    
    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(token)
        
    assert excinfo.value.status_code == 401
    assert excinfo.value.detail == "Token expired"
