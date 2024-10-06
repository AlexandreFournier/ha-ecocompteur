"""Constants for the ecocompteur integration."""

from datetime import timedelta

DOMAIN = "ecocompteur"
MANUFACTURER = "Legrand"
MODEL = "412000"  # 412005 for radio
DEFAULT_NAME = "Ecocompteur"

ATTR_CONFIG_ENTRY_ID = "entry_id"

DEFAULT_SCAN_INTERVAL = timedelta(seconds=5)
