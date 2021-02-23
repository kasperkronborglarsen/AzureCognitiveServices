from pathlib import Path
from dataclasses import dataclass

import yaml


@dataclass(frozen=True)
class AzureCredentials:
    """Represents database configuration settings."""

    endpoint: str
    key: str

    @staticmethod
    def load(db_path: Path):
        """Loads configuration from YAML file."""
        if not db_path.exists():
            raise Exception(f"Authentication file {db_path} does not exist.")

        with open(db_path, mode="r", encoding="utf-8") as cred:
            content = yaml.full_load(cred)
            return AzureCredentials(
                endpoint=content.get("endpoint"),
                key=content.get("key"),
            )
