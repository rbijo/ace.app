from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from jose import JWTError, jwt

from app.core.database import get_db, engine, Base
from app.core.security import create_access_token, verify_password, get_password_hash
from app.core.config import settings
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/token")


class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id_str: str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    stmt = select(User).where(User.id == user_id)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()
    if user is None:
        raise credentials_exception
    return user


@router.post("/signup", response_model=UserResponse)
async def signup(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    # Ensure DB tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    stmt = select(User).where(User.email == user_in.email)
    res = await db.execute(stmt)
    if res.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    # Ensure DB tables exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    stmt = select(User).where(User.email == form_data.username)
    res = await db.execute(stmt)
    user = res.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
