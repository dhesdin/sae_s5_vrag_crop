from pydantic import BaseModel


class SearchResult(BaseModel):
    """Une image trouvée par la recherche.

    Le front affiche, pour chaque image : le rang (1 = meilleure), le score
    similarity brut (ex. 0,73, jamais converti en pourcentage) et le texte matched.
    """

    rank: int
    image: str
    distance: float
    similarity: float
    matched: str
