from pathlib import Path

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png"}


def _get_root_dir() -> Path:
    """
    Returns the root directory of the project as a Path object.

    Returns:
        Path: The root directory of the project.
    """
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError("Could not find the root directory containing pyproject.toml")


# for indexation
def list_dataset_images(dataset_dir: Path | str = "dataset") -> list[Path]:
    """
    Lists all supported image files in the dataset directory.

    Args:
        dataset_dir (Path): The path to the dataset directory.

    Returns:
        list[Path]: A sorted list of paths to the supported image files.
    """
    root_path = _get_root_dir()
    dataset_dir = root_path / dataset_dir
    if not dataset_dir.exists():
        raise FileNotFoundError(f"Dataset directory not found: {dataset_dir}")
    if not dataset_dir.is_dir():
        raise NotADirectoryError(f"Provided path is not a directory: {dataset_dir}")

    return sorted(f for f in dataset_dir.iterdir() if f.suffix.lower() in SUPPORTED_EXTENSIONS)
