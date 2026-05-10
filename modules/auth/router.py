import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from core.config import settings
from core.deps import get_current_user
from core.security import ExpiredTokenError, InvalidTokenError, decode_token
from db.base import get_db
from modules.users.models import User
from modules.verification import service as verification_service
from modules.verification.schemas import (
    PasswordResetConfirm,
    PasswordResetConfirmResponse,
    PasswordResetRequest,
    PasswordResetRequestResponse,
)

from . import service
from .schemas import GoogleAuthRequest, RegisterResponse, RefreshRequest, Token, UserLogin, UserRead, UserRegister

router = APIRouter(prefix="/auth", tags=["auth"])
logger = logging.getLogger(__name__)

_UNAUTHORIZED = {"WWW-Authenticate": "Bearer"}


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, db: Session = Depends(get_db)) -> RegisterResponse:
    if service.get_by_email(db, payload.email):
        raise HTTPException(status_code=409, detail="Email already registered")
    try:
        result = service.register(db, payload)
    except service.VerificationEmailDeliveryError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No pudimos enviarte el código de verificación. Tu cuenta fue creada — intenta de nuevo en unos minutos con 'Reenviar código'.",
        )
    return RegisterResponse(
        detail="User registered. Verify your email before login",
        verification_expires_at=result.verification_expires_at,
        verification_code=result.verification_code if settings.DEBUG else None,
    )


@router.post("/login", response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)) -> Token:
    user = service.authenticate(db, payload.email, payload.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers=_UNAUTHORIZED,
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account not verified. Verify your email first",
        )
    return service.issue_tokens(user.id)


@router.post("/token", response_model=Token, include_in_schema=False)
def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    user = service.authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers=_UNAUTHORIZED,
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account not verified. Verify your email first",
        )
    return service.issue_tokens(user.id)


@router.post("/refresh", response_model=Token)
def refresh(body: RefreshRequest, db: Session = Depends(get_db)) -> Token:
    try:
        payload = decode_token(body.refresh_token, expected_type="refresh")
    except ExpiredTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers=_UNAUTHORIZED,
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers=_UNAUTHORIZED,
        )
    subject = payload.get("sub")
    user = db.get(User, int(subject)) if subject else None
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers=_UNAUTHORIZED,
        )
    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account not verified. Verify your email first",
        )
    return service.issue_tokens(user.id)


@router.get("/me", response_model=UserRead)
def me(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.post("/forgot-password", response_model=PasswordResetRequestResponse)
def forgot_password(
    payload: PasswordResetRequest,
    db: Session = Depends(get_db),
) -> PasswordResetRequestResponse:
    try:
        reset_code = verification_service.request_password_reset(db, payload.email)
    except verification_service.UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except verification_service.VerificationEmailDeliveryError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Reset code generated but email could not be sent",
        )
    return PasswordResetRequestResponse(
        detail="Reset code sent. Check your email",
        expires_at=reset_code.expired_at,
        reset_code=reset_code.code if settings.DEBUG else None,
    )


@router.post("/reset-password", response_model=PasswordResetConfirmResponse)
def reset_password(
    payload: PasswordResetConfirm,
    db: Session = Depends(get_db),
) -> PasswordResetConfirmResponse:
    try:
        verification_service.confirm_password_reset(
            db, payload.email, payload.code, payload.new_password
        )
    except verification_service.UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except verification_service.PasswordResetCodeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active reset code. Request a new one",
        )
    except verification_service.PasswordResetCodeExpiredError:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Reset code expired. Request a new one",
        )
    except verification_service.InvalidPasswordResetCodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset code",
        )
    return PasswordResetConfirmResponse(detail="Password reset successfully")


@router.post("/google", response_model=Token)
def google_auth(payload: GoogleAuthRequest, db: Session = Depends(get_db)) -> Token:
    try:
        return service.google_authenticate(db, payload.id_token, payload.access_token)
    except service.GoogleTokenError as exc:
        logger.warning("Google auth failed: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo autenticar con Google",
        )
