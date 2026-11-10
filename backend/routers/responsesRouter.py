

from fastapi import APIRouter
from backend.models.Response import Response, Role

class ResponsesRouter(APIRouter):

    def __init__(self) -> None:
        super().__init__(prefix="/responses", tags=["responses"])
        self._register_endpoints()

    def _register_endpoints(self) -> None:
        """ Fonction permettant d'enregistrer toutes les routes au sein du router.
        """
        self.get("/", response_model=dict)(self.root)
        self.get("/all", response_model=dict)(self.get_all_responses)
        self.get("/{response_id}", response_model=dict)(self.get_response_by_id)

    async def root(self) -> dict:
        return {"message": "Responses route"}

    async def get_all_responses(self) -> dict:

        responses_list : list[Response] = [
            Response(id=1, role=Role.USER, content="This is the first response", img_url="https://example.com/image1.jpg"),
            Response(id=2, role=Role.IA, content="This is the second response", img_url="https://example.com/image2.jpg")
        ]

        return {
            "message": "Getting all responses",
            "content": responses_list
        }

    async def get_response_by_id(self, response_id: int) -> dict:
        """
        Fonction permettant de trouver une réponse en fonction de son Id. Si la réponse est trouvée un dictionnaire contenant la réponse sera renvoyé 
        ou vide sinon

        Parameters
        ----------
        response_id : int
            Id de la réponse a rechercher

        Returns
        -------
        type
            Description
        """
        response : Response = Response(id=response_id, role=Role.IA, content="This is the response", img_url="https://example.com/image.jpg")
        return {
            "message": f"Getting response with ID {response_id}",
            "content": [response]
        }