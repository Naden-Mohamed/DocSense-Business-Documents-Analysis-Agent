from fastapi import APIRouter

base = APIRouter(tags=["api"], prefix="/api")

@base.get('/')
def get_status():
    return {"APP_NAME": "app_settings.app_name"}

@base.get('/health')
def health_check():
    return {"status": "FastAPI is running"} 