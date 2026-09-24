from pathlib import Path
from typing import Any

from chromadb import PersistentClient

from v_crop_rag.storage.base import BaseVectorIndex, VectoreSearchResult


class ChromaVectorIndex(BaseVectorIndex):
    """Implement a BaseVector using Chroma"""

    def __init__(self, path: str | Path, collection_name: str) -> None:
        if not isinstance(collection_name, str):
            raise TypeError("collection_name must be a string")

        if not collection_name.strip():
            raise ValueError("collection_name is required")

        if not isinstance(path, (str, Path)):
            raise TypeError("Path must be a string or a path")

        if isinstance(path, str) and not path.strip():
            raise ValueError("Path is required")

        self._client = PersistentClient(path=path)
        self._collection = self._client.get_or_create_collection(name=collection_name)

    def add(self, id: str, vector: list[float], metadata: dict[str, Any]) -> None:
        if not isinstance(id, str):
            raise TypeError("id must be a string")

        if not id.strip():
            raise ValueError("id is required")

        if not isinstance(vector, list):
            raise TypeError("vector must be a list")

        if not vector:
            raise ValueError("vector is required")

        if not all(type(element) in (int, float) for element in vector):
            raise TypeError("vector must contain only int or float")

        if not isinstance(metadata, dict):
            raise TypeError("metadata must be a dictionary")

        self._collection.add(ids=[id], embeddings=[vector], metadatas=[metadata])

    def query(self, vector: list[float], k: int = 5) -> list[VectoreSearchResult]:

        if not isinstance(vector, list):
            raise TypeError("le vecteur doit être sous forme de liste de flottant")

        if vector == []:
            raise ValueError("le vecteur est obligatoire")

        if not all(type(item) in (int, float) for item in vector):
            raise TypeError("les coordonnées du vecteurs doivent être des entiers ou des flottants")

        if type(k) is not int:
            raise TypeError("Le nombre de résultats doit être un entier")

        if k <= 0:
            raise ValueError("le nombre de résultats doit être positif")

        results = self._collection.query(query_embeddings=[vector], n_results=k)

        # Recover the first element of each because only one request is sent here
        ids = results["ids"][0]
        distances = results["distances"][0]
        metadatas = results["metadatas"][0]

        list_objects = []
        for result_id, result_distance, result_metadata in zip(ids, distances, metadatas):
            vector_result = VectoreSearchResult(id=result_id, distance=result_distance, metadata=result_metadata)
            list_objects.append(vector_result)

        return list_objects
