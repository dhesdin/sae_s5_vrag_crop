from http.client import HTTPException

from fastapi import APIRouter
from typing import Annotated
responses_router : APIRouter = APIRouter(prefix="/responses", tags=["Responses"])

@responses_router.get('/')
def read_responses():
    return {"Message": "This is a response endpoint"}

@responses_router.get(
        path="/{response_id}",
        responses={
            400: {"description": "Invalid response ID"},
            404: {"description": "Response not found"}
        }
    )
def read_response(response_id: Annotated[str, "The ID of the response to retrieve"]):
    """Retourne une réponse dont l'id est `response_id`

    Args:
        response_id (Annotated[str, &quot;The ID of the response to retrieve&quot;]): _description_

    Raises:
        HTTPException: _description_

    Returns:
        json: Contenu du message
    """
    if not response_id:
        raise HTTPException(status_code=400, detail="Invalid response ID")
    return {
        "ResponseID": response_id, 
        "Message": "This is a specific response endpoint"
    }