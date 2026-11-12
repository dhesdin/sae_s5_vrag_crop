from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class VectoreSearchResult:
    """result of vectorial research"""

    id: str
    distance: float
    metadata: dict[str, Any]


class BaseVectorIndex(ABC):
    """common interface for vectorials index"""

    @abstractmethod
    def add(self, id: str, vector: list[float], metadata: dict[str, Any]) -> None:
        """add a vector and his metadatas in index
        
        If an entry with the same id already exist, it's relaced (upsert)
        """
        raise NotImplementedError

    @abstractmethod
    def query(self, vector: list[float], k: int = 5) -> list[VectoreSearchResult]:
        """return k results closest to vector given"""
        raise NotImplementedError
    
    @abstractmethod
    def exists(self, id:str) -> bool:
        """return true if an entry with this id is already stored in the index"""
        raise NotImplementedError
    