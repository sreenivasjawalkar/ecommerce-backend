from fastapi import FastAPI
from app.core.config import settings
from app.core.exceptions import ApplicationError
from app.api.v1.router import router as api_v1_router
from app.api.exception_handlers import application_error_handler

app = FastAPI( 
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug
)

app.include_router(api_v1_router)

@app.get("")
async def root():
    return {         
        "message": "Ecommerce AI Platform Backend",         
        "version": settings.app_version,         
        "environment": settings.environment,     
    }

app.add_exception_handler(
    ApplicationError,
    application_error_handler,
)