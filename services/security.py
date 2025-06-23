from fastapi import HTTPException, Depends, Request

def get_currentuser(request: Request):
    user=request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated. Please login")
    return user

def require_role(*roles: str):
    def role_check(user: dict=Depends(get_currentuser)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Not Authorized to this role")
    return role_check