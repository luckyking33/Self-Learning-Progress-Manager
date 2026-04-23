"""Authentication routes for registration and login."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.models import User
from app.db.session import get_db_session
from app.schemas import ApiEnvelope, AuthTokenOut, UserRegisterIn


router = APIRouter()


def _build_avatar(username: str) -> str:
    compact = "".join(part[0] for part in username.split() if part).upper()
    if compact:
        return compact[:2]
    return username[:2].upper() or "ST"


@router.post("/register", response_model=ApiEnvelope[AuthTokenOut], status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserRegisterIn,
    session: AsyncSession = Depends(get_db_session),
) -> ApiEnvelope[AuthTokenOut]:
    existing_user_result = await session.execute(
        select(User).where(
            or_(User.username == payload.username, User.email == payload.email)
        )
    )
    existing_user = existing_user_result.scalar_one_or_none()
    if existing_user is not None:
        detail = "Username is already taken." if existing_user.username == payload.username else "Email is already registered."
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

    user = User(
        username=payload.username,
        email=payload.email,
        password_hash=get_password_hash(payload.password),
        avatar=_build_avatar(payload.username),
        headline=f"{payload.username} is learning with STAR",
        streak_days=0,
        is_active=True,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)

    token = create_access_token(str(user.id))
    return ApiEnvelope(
        code=0,
        message="registered",
        data=AuthTokenOut(access_token=token),
    )


@router.post("/login", response_model=ApiEnvelope[AuthTokenOut])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session),
) -> ApiEnvelope[AuthTokenOut]:
    result = await session.execute(
        select(User).where(
            or_(User.username == form_data.username, User.email == form_data.username)
        )
    )
    user = result.scalar_one_or_none()
    if user is None or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user.",
        )

    token = create_access_token(str(user.id))
    return ApiEnvelope(
        code=0,
        message="ok",
        data=AuthTokenOut(access_token=token),
    )
