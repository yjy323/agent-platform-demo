from fastapi import FastAPI, Request
from src.routers import health

app = FastAPI(title="Test API", description="CI 파이프라인 테스트를 위한 API")

app.include_router(health.router)


@app.get("/")  # type: ignore
async def root(request: Request) -> dict:
    """루트 엔드포인트는 기본 인사말을 반환합니다."""
    return {"message": "Hello World! Welcome to Test API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
