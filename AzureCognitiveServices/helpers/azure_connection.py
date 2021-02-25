from pathlib import Path
from dataclasses import dataclass

import yaml

from AzureCognitiveServices.helpers.logging_helpers import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class AzureCredentials:
    """Represents database configuration settings."""

    endpoint: str
    key: str

    @staticmethod
    def load(cred_path: Path):
        """Loads configuration from YAML file."""
        logger.debug(f"Retrieving credentials from {cred_path}")
        if not cred_path.exists():
            raise Exception(f"Authentication file {cred_path} does not exist.")

        with open(cred_path, mode="r", encoding="utf-8") as cred:
            content = yaml.full_load(cred)
            return AzureCredentials(
                endpoint=content.get("endpoint"), key=content.get("key"),
            )
