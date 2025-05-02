from typing import Dict

from fastapi import APIRouter, Request, status

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/", status_code=status.HTTP_200_OK)  # type: ignore
async def health_check(request: Request) -> Dict[str, str]:
    """API 상태 확인을 위한 헬스 체크 엔드포인트입니다."""
    return {"status": "healthy"}
