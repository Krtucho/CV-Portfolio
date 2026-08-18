import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sqlalchemy.exc import SQLAlchemyError
from structlog import get_logger

from app.api.v1 import auth, health, items, users
from app.core.config import settings
from app.core.security import RateLimitExceeded, UnauthorizedError

logger = get_logger()

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.ENVIRONMENT,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            FastApiIntegration(),
            SqlalchemyIntegration(),
        ],
    )

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs" if settings.ENVIRONMENT != "production" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT != "production" else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID"],
)

app.include_router(health.router, prefix=f"{settings.API_V1_STR}/health", tags=["health"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(items.router, prefix=f"{settings.API_V1_STR}/items", tags=["items"])


@app.middleware("http")
async def add_request_id_header(request: Request, call_next):
    import uuid
    request_id = str(uuid.uuid4())
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


@app.exception_handler(UnauthorizedError)
async def unauthorized_handler(request: Request, exc: UnauthorizedError):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded. Try again later."})


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_handler(request: Request, exc: SQLAlchemyError):
    logger.error("database_error", error=str(exc))
    return JSONResponse(status_code=500, content={"detail": "Internal database error."})


@app.get("/")
async def root():
    return {"service": settings.PROJECT_NAME, "version": settings.VERSION, "status": "running"}
