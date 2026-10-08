
from app.api.v0.endpoints import responses
from fastapi import APIRouter
api_router : APIRouter = APIRouter(prefix="/v0")
api_router.include_router(responses.responses_router)

@api_router.get(path="/health")
def read_health():
    return {"Status": "OK"}