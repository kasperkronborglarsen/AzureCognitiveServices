from pathlib import Path
from dataclasses import dataclass

import yaml


@dataclass(frozen=True)
class AzureCredentials:
    """Represents database configuration settings."""

    endpoint: str
    key: str

    @staticmethod
    def load(cred_path: Path):
        """Loads configuration from YAML file."""
        if not cred_path.exists():
            raise Exception(f"Authentication file {cred_path} does not exist.")

        with open(cred_path, mode="r", encoding="utf-8") as cred:
            content = yaml.full_load(cred)
            return AzureCredentials(
                endpoint=content.get("endpoint"),
                key=content.get("key"),
            )
