# from fastapi import APIRouter, Depends, HTTPException
# from fastapi.security import OAuth2PasswordRequestForm
# from main import authenticate_user
# from ..schemas import Token

# router = APIRouter(prefix="/auth", tags=["Auth"])

# @router.post("/login", response_model=Token)
# def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     return {"access_token": user.username, "token_type": "bearer"}