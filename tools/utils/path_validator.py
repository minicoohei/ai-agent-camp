from pathlib import Path
from typing import Iterable, Optional, Union


def validate_path(
    path_input: Union[str, Path],
    *,
    must_exist: bool = True,
    must_be_file: bool = False,
    must_be_dir: bool = False,
    allowed_extensions: Optional[Iterable[str]] = None,
) -> Path:
    """ユーザー入力のパスを検証して安全に扱う."""
    if path_input is None:
        raise ValueError("Path is required")

    path = Path(path_input).expanduser().resolve()

    if must_exist and not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    if must_be_file and not path.is_file():
        raise ValueError(f"Not a file: {path}")

    if must_be_dir and not path.is_dir():
        raise ValueError(f"Not a directory: {path}")

    if allowed_extensions:
        allowed = {ext.lower() for ext in allowed_extensions}
        if path.suffix.lower() not in allowed:
            raise ValueError(f"Invalid extension: {path.suffix}")

    return path
