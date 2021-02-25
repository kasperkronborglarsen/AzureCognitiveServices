from typing import Optional
from pathlib import Path

import click


def validate_file(
    ctx: click.Context,
    param: click.Parameter,
    value: Optional[str],
    must_exists: Optional[bool],
) -> Optional[Path]:
    """Validates whether a path exists or does not exists."""
    if value is None:
        return None
    file_path = Path(value)
    if file_path.exists() != must_exists:
        exists_text = "" if must_exists else "not "
        raise click.BadParameter(f"Path {file_path} does {exists_text}exist.")
    return file_path


def validate_file_exists(
    ctx: click.Context, param: click.Parameter, value: Optional[str]
) -> Optional[Path]:
    """Ensures that the given file path exists."""
    return validate_file(ctx, param, value, must_exists=True)


def validate_file_not_exists(
    ctx: click.Context, param: click.Parameter, value: Optional[str]
) -> Optional[Path]:
    """Ensures that the given file path does not exists."""
    return validate_file(ctx, param, value, must_exists=False)
