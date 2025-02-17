import meilisearch
from django.conf import settings
from loguru import logger

MEILI_URL = settings.MEILI_URL if hasattr(settings, "MEILI_URL") else None

MEILI_MASTER_KEY = (
    settings.MEILI_MASTER_KEY if hasattr(settings, "MEILI_MASTER_KEY") else None
)

if MEILI_URL:
    meili_client = meilisearch.Client(
        MEILI_URL,
        MEILI_MASTER_KEY,
    )
    logger.success(f"MeiliSearch client connected to {MEILI_URL}")
