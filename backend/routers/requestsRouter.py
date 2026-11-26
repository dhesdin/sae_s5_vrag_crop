

from fastapi import APIRouter
from backend.models.Response import Response, Role

class RequestsRouter(APIRouter):

    def __init__(self) -> None:
        super().__init__(prefix="/requests", tags=["requests"])
        self._register_endpoints()

    def _register_endpoints(self) -> None:
        """ Fonction permettant d'enregistrer toutes les routes au sein du router.
        """
        self.get("/", response_model=dict)(self.root)
        self.get("/all", response_model=dict)(self.get_all_responses)
     

    async def root(self) -> dict:
        return {"message": "Requests route"}

    
    
    