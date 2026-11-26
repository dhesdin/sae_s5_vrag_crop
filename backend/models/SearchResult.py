from pydantic import BaseModel


class SearchResult(BaseModel):
    """Une image trouvée par la recherche.

    Le front affiche le rang, pas un pourcentage : avec un k élevé on récupère
    aussi des images sans rapport, et la distance n'a pas de sens en absolu.
    """

    rank: int
    image: str
    distance: float
    matched: str
