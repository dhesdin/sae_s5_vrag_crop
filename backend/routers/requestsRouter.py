from fastapi import APIRouter, HTTPException

from backend.models.Request import Request
from backend.models.SearchResult import SearchResult
from v_crop_rag.ollama_client.ollama_wrapper_iut import OllamaConnectionError
from v_crop_rag.service.search_service import search_images


class RequestsRouter(APIRouter):

    def __init__(self) -> None:
        super().__init__(prefix="/requests", tags=["requests"])
        self._register_endpoints()

    def _register_endpoints(self) -> None:
        """ Fonction permettant d'enregistrer toutes les routes au sein du router.
        """
        self.get("/", response_model=dict)(self.root)
        self.post("/", response_model=list[SearchResult])(self.send_request)

    async def root(self) -> dict:
        return {"message": "Requests route"}

    async def send_request(self, request: Request) -> list[SearchResult]:
        """
        Fonction permettant d'envoyer une requête de recherche d'images.

        Parameters
        ----------
        request : Request
            Le texte recherché et le nombre d'images voulues (k)

        Returns
        -------
        list[SearchResult]
            Les images trouvées, de la plus proche à la plus éloignée, avec leur rang (1 = meilleure)

        Raises
        ------
        HTTPException
            422 si la requête est vide ou k invalide, 503 si Ollama est injoignable,
            500 si l'index Chroma n'existe pas
        """
        try:
            results = await search_images(request.query, request.k)
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e)) from e
        except OllamaConnectionError as e:
            raise HTTPException(status_code=503, detail="Serveur Ollama injoignable") from e
        except FileNotFoundError as e:
            raise HTTPException(status_code=500, detail="Index de recherche absent") from e

        return [SearchResult(rank=rank, **result) for rank, result in enumerate(results, start=1)]
