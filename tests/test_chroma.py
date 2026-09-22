from pathlib import Path
from typing import Any
from unittest.mock import Mock, patch

from chromadb import PersistentClient
import pytest


from v_crop_rag.storage.chroma import ChromaVectorIndex


"""id incorrect
├── pas une str
└── chaîne vide

vector incorrect
├── pas une list
├── liste vide
└── contient autre chose que int/float

metadata incorrect
└── pas un dict


add(
    id="object_001",
    vector=[0.1, 0.2],
    metadata={"label": "vélo"}
)

                ↓

_collection.add(
    ids=["object_001"],
    embeddings=[[0.1, 0.2]],
    metadatas=[{"label": "vélo"}],
)
"""

def test_init_create_persistent_collection():
    
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        
        ChromaVectorIndex(path="data/chroma", collection_name="test_images")
    
        mock_persistent_client.assert_called_once_with(path="data/chroma")
        
        mock_client = mock_persistent_client.return_value
        
        mock_client.get_or_create_collection.assert_called_once_with(name="test_images")


def test_add_send_data_to_chroma():
    
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(path="data/chroma", collection_name="test_images")
        
        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.get_or_create_collection.return_value
        
        index.add(id="object01_test", vector=[0.1, -0.2, 0.7], metadata={"label": "test"})
        
        mock_collection.add.assert_called_once_with(ids=["object01_test"], embeddings=[[0.1, -0.2, 0.7]], metadatas=[{"label": "test"}])


@pytest.mark.parametrize("invalid_id",
                         [
                             123,
                             None,
                             [],
                             {},
                         ],
)
def test_add_reject_invalid_id_type(invalid_id):
    
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(
            path="data/chroma",
            collection_name="test_images"
        )
        
        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.get_or_create_collection.return_value
        
        with pytest.raises(TypeError):
            index.add(id=invalid_id, vector=[0.1, -0.2, 0.7], metadata={"label": "test"})



@pytest.mark.parametrize("invalid_value_id",
                         [
                             "",
                             "   ",
                         ],
)
def test_add_reject_invalid_id_value(invalid_value_id):
    
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(
            path="data/chroma",
            collection_name="test_images"
        )
        
        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.get_or_create_collection.return_value
        
        with pytest.raises(ValueError):
            index.add(id=invalid_value_id, vector=[0.1, -0.2, 0.7], metadata={"label": "test"})