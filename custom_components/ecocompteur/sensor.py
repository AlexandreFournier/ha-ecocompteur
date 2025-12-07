"""Support for Ecocompteur sensors."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.components.sensor.const import (
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.const import UnitOfEnergy, UnitOfPower, UnitOfVolume
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .api import Ecocompteur
from .const import DOMAIN, MANUFACTURER, MODEL
from .coordinator import EcocompteurDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from . import EcocompteurConfigEntry

_LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, kw_only=True)
class EcocompteurSensorEntityDescription(SensorEntityDescription):
    """Represent the ecocompteur sensor entity description."""

    config_idx: int


TIC_SENSORS: tuple[SensorEntityDescription, ...] = (
    SensorEntityDescription(
        key="base",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="hc",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="hp",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="hc_b",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="hp_b",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="hc_w",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="hp_w",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="hc_r",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=3,
    ),
    SensorEntityDescription(
        key="hp_r",
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.ENERGY,
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        suggested_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        suggested_display_precision=3,
    ),
)

SENSORS: tuple[EcocompteurSensorEntityDescription, ...] = (
    EcocompteurSensorEntityDescription(
        key="data1",
        config_idx=0,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    EcocompteurSensorEntityDescription(
        key="data2",
        config_idx=1,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    EcocompteurSensorEntityDescription(
        key="data3",
        config_idx=2,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    EcocompteurSensorEntityDescription(
        key="data4",
        config_idx=3,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    EcocompteurSensorEntityDescription(
        key="data5",
        config_idx=4,
        state_class=SensorStateClass.MEASUREMENT,
        device_class=SensorDeviceClass.POWER,
        native_unit_of_measurement=UnitOfPower.WATT,
    ),
    EcocompteurSensorEntityDescription(
        key="data6",
        config_idx=5,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.WATER,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
    ),
    EcocompteurSensorEntityDescription(
        key="data7",
        config_idx=6,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.WATER,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
    ),
    EcocompteurSensorEntityDescription(
        key="CIR1_Nrj",
        config_idx=7,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.GAS,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
    ),
    EcocompteurSensorEntityDescription(
        key="CIR2_Nrj",
        config_idx=8,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.GAS,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
    ),
    EcocompteurSensorEntityDescription(
        key="CIR3_Nrj",
        config_idx=9,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.GAS,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
    ),
    EcocompteurSensorEntityDescription(
        key="CIR4_Nrj",
        config_idx=10,
        state_class=SensorStateClass.TOTAL_INCREASING,
        device_class=SensorDeviceClass.GAS,
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: EcocompteurConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Ecocompteur sensors."""
    entry_id = config_entry.entry_id

    client = Ecocompteur(hass, config_entry.runtime_data.host)
    coordinator = EcocompteurDataUpdateCoordinator(hass, entry_id, client)

    await coordinator.async_config_entry_first_refresh()

    device_info = DeviceInfo(
        identifiers={(DOMAIN, entry_id)},
        manufacturer=MANUFACTURER,
        model=MODEL,
        name=config_entry.runtime_data.name,
    )

    async_add_entities(
        EcocompteurTicSensor(description, coordinator, device_info, entry_id)
        for description in TIC_SENSORS
    )

    async_add_entities(
        EcocompteurSensor(description, coordinator, device_info, entry_id)
        for description in SENSORS
    )


class EcocompteurTicSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Ecocompteur sensor."""

    _attr_has_entity_name = True

    def __init__(
        self,
        entity_description: SensorEntityDescription,
        coordinator: EcocompteurDataUpdateCoordinator,
        device_info: DeviceInfo,
        entry_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, context=entity_description.key)
        self.entity_description = entity_description
        self._coordinator = coordinator
        self._attr_device_info = device_info
        self._attr_unique_id = f"{entry_id}_conso_{entity_description.key}"

    def _update_attrs(self) -> None:
        """Update state attributes."""
        config = self._coordinator.data["config"]["conso"]
        key = self.entity_description.key
        self._attr_name = key.upper().replace("_", " ")
        self._attr_native_value = config[key]

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_attrs()
        self.async_write_ha_state()


class EcocompteurSensor(CoordinatorEntity, SensorEntity):
    """Representation of an Ecocompteur sensor."""

    entity_description: EcocompteurSensorEntityDescription

    _attr_has_entity_name = True

    def __init__(
        self,
        entity_description: EcocompteurSensorEntityDescription,
        coordinator: EcocompteurDataUpdateCoordinator,
        device_info: DeviceInfo,
        entry_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator, context=entity_description.key)
        self.entity_description = entity_description
        self._coordinator = coordinator
        self._attr_device_info = device_info
        self._attr_unique_id = f"{entry_id}_{entity_description.key}"

    def _update_attrs(self) -> None:
        """Update state attributes."""
        config = self._coordinator.data["config"]
        config_idx = self.entity_description.config_idx

        self._attr_name = config["inputs"][config_idx]["label"]
        self._attr_available = not config["inputs"][config_idx]["disabled"]
        if self._attr_available:
            key = self.entity_description.key
            values = self._coordinator.data["values"]
            self._attr_native_value = values[key]

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._update_attrs()
        self.async_write_ha_state()
