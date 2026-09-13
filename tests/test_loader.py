from v_crop_rag.service.dataset_loader import list_dataset_images


def test_list_dataset_images_filters_and_sorts(tmp_path):
    (tmp_path / "b.jpg").touch()
    (tmp_path / "a.png").touch()
    (tmp_path / "notes.txt").touch()

    result = list_dataset_images(tmp_path)

    assert len(result) == 2
    assert result[0].name == "a.png"
    assert result[1].name == "b.jpg"
