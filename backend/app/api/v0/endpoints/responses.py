from fastapi import APIRouter

responses_router : APIRouter = APIRouter(prefix="/responses", tags=["Responses"])

@responses_router.get('/')
def read_responses():
    return {"Message": "This is a response endpoint"}

@responses_router.get('/{response_id}')
def read_response(response_id: str):
    return {"ResponseID": response_id, "Message": "This is a specific response endpoint"}