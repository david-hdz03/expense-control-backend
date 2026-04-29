from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from core.config import settings
from db.base import get_db
from modules.auth import service as auth_service
from modules.auth.schemas import Token

from . import service
from .schemas import (
    VerificationConfirm,
    VerificationRequest,
    VerificationRequestResponse,
)

router = APIRouter(prefix="/verification", tags=["verification"])


@router.post("/request", response_model=VerificationRequestResponse)
def request_verification_code(
    payload: VerificationRequest,
    db: Session = Depends(get_db),
) -> VerificationRequestResponse:
    try:
        verification_code = service.request_email_verification(db, payload.email)
    except service.UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except service.AlreadyVerifiedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Account already verified",
        )
    except service.VerificationEmailDeliveryError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Verification code generated but email could not be sent",
        )

    return VerificationRequestResponse(
        detail="Verification code generated",
        expires_at=verification_code.expired_at,
        verification_code=verification_code.code if settings.DEBUG else None,
    )


@router.post("/confirm", response_model=Token)
def confirm_verification_code(
    payload: VerificationConfirm,
    db: Session = Depends(get_db),
) -> Token:
    try:
        user = service.confirm_email_verification(db, payload.email, payload.code)
    except service.UserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    except service.VerificationCodeNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active verification code. Request a new one",
        )
    except service.VerificationCodeExpiredError:
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="Verification code expired. Request a new one",
        )
    except service.InvalidVerificationCodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid verification code",
        )

    return auth_service.issue_tokens(user.id)
