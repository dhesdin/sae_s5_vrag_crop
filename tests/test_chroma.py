from unittest.mock import patch

import pytest

from v_crop_rag.storage.chroma import ChromaVectorIndex


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


@pytest.mark.parametrize(
    "invalid_id",
    [
        123,
        None,
        [],
        {},
    ],
)
def test_add_reject_invalid_id_type(invalid_id):

    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(path="data/chroma", collection_name="test_images")

        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.get_or_create_collection.return_value

        with pytest.raises(TypeError):
            index.add(id=invalid_id, vector=[0.1, -0.2, 0.7], metadata={"label": "test"})

        mock_collection.add.assert_not_called()


@pytest.mark.parametrize(
    "invalid_value_id",
    [
        "",
        "   ",
    ],
)
def test_add_reject_invalid_id_value(invalid_value_id):

    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(path="data/chroma", collection_name="test_images")

        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.get_or_create_collection.return_value

        with pytest.raises(ValueError):
            index.add(id=invalid_value_id, vector=[0.1, -0.2, 0.7], metadata={"label": "test"})

        mock_collection.add.assert_not_called()


@pytest.mark.parametrize("invalid_vector", ["abc", (0.1, 0.2), 123, None])
def test_add_reject_invalid_vector_type(invalid_vector):
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(path="chroma/data", collection_name="test_images")

        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.get_or_create_collection.return_value

        with pytest.raises(TypeError):
            index.add(id="_object_01", vector=invalid_vector, metadata={"label": "test"})
        mock_collection.add.assert_not_called()


def test_add_reject_empty_vector():
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(path="chroma/data", collection_name="iamges_test")

        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.add.get_or_create_collection.return_value

        with pytest.raises(ValueError):
            index.add(id="test_object_01", vector=[], metadata={"label": "test"})
        mock_collection.add.assert_not_called()


@pytest.mark.parametrize(
    "invalid_vector",
    [
        [1.3, "test", 0.7],
        [None, 0.2],
        [True, 0.7],
    ],
)
def test_add_reject_invalid_vector_value(invalid_vector):
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persitent_client:
        index = ChromaVectorIndex(path="chroma/data", collection_name="images_test")

        mock_client = mock_persitent_client.return_value
        mock_collection = mock_client.add.return_value

        with pytest.raises(TypeError):
            index.add(id="test_object_01", vector=invalid_vector, metadata={"label": "test"})
        mock_collection.add.assert_not_called()


@pytest.mark.parametrize("invalid_metadata", [[], 123, None, "test"])
def test_add_reject_invalid_metadata_type(invalid_metadata):
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(path="chroma/data", collection_name="images_test")

        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.add.return_value

        with pytest.raises(TypeError):
            index.add(id="test_object_01", vector=[0.1, -0.2, 0.7], metadata=invalid_metadata)
        mock_collection.add.assert_not_called()


def test_query_returns_vector_search_results():
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(path="data/chroma", collection_name="test_images")

        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.get_or_create_collection.return_value

        mock_collection.query.return_value = {
            "ids": [["obj01", "obj02"]],
            "distances": [[0.12, 0.35]],
            "metadatas": [
                [
                    {"label": "velo"},
                    {"label": "moto"},
                ]
            ],
        }

        results = index.query(vector=[0.1, -0.2, 0.7], k=2)

        mock_collection.query.assert_called_once_with(query_embeddings=[[0.1, -0.2, 0.7]], n_results=2)

        assert len(results) == 2

        assert results[0].id == "obj01"
        assert results[0].distance == 0.12
        assert results[0].metadata == {"label": "velo"}

        assert results[1].id == "obj02"
        assert results[1].distance == 0.35
        assert results[1].metadata == {"label": "moto"}


@pytest.mark.parametrize("invalid_vector", ["abc", (0.1, 0.2), 123, None])
def test_query_reject_invalid_vector_type(invalid_vector):
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(path="chroma/data", collection_name="test_images")

        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.get_or_create_collection.return_value

        with pytest.raises(TypeError):
            index.query(vector=invalid_vector, k=2)
        mock_collection.query.assert_not_called()


def test_query_reject_empty_vector():
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(path="chroma/data", collection_name="iamges_test")

        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.add.get_or_create_collection.return_value

        with pytest.raises(ValueError):
            index.query(vector=[], k=2)
        mock_collection.query.assert_not_called()


@pytest.mark.parametrize(
    "invalid_vector",
    [
        [1.3, "test", 0.7],
        [None, 0.2],
        [True, 0.7],
    ],
)
def test_query_reject_invalid_vector_value(invalid_vector):
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persitent_client:
        index = ChromaVectorIndex(path="chroma/data", collection_name="images_test")

        mock_client = mock_persitent_client.return_value
        mock_collection = mock_client.add.return_value

        with pytest.raises(TypeError):
            index.query(vector=invalid_vector, k=2)
        mock_collection.query.assert_not_called()


@pytest.mark.parametrize("invalid_k", [1.2, False, (2, 3), "test", [1, 4], None])
def test_query_reject_invalid_k_type(invalid_k):
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(path="chroma/data", collection_name="iamges_test")

        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.add.get_or_create_collection.return_value

        with pytest.raises(TypeError):
            index.query(vector=[0.1, -0.2, 0.7], k=invalid_k)
        mock_collection.query.assert_not_called()


@pytest.mark.parametrize("invalid_k", [0, -1])
def test_query_reject_invalid_k_value(invalid_k):
    with patch("v_crop_rag.storage.chroma.PersistentClient") as mock_persistent_client:
        index = ChromaVectorIndex(path="chroma/data", collection_name="iamges_test")

        mock_client = mock_persistent_client.return_value
        mock_collection = mock_client.add.get_or_create_collection.return_value

        with pytest.raises(ValueError):
            index.query(vector=[0.1, -0.2, 0.7], k=invalid_k)
        mock_collection.query.assert_not_called()
