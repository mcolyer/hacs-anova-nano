"""AnovaNanoEntity class."""
from __future__ import annotations

from typing import Any

from homeassistant.helpers.entity import DeviceInfo, EntityDescription
from homeassistant.components.bluetooth.passive_update_coordinator import (
    PassiveBluetoothCoordinatorEntity,
)
from pyanova_nano.types import SensorValues

from .const import ATTRIBUTION, DOMAIN, NAME, VERSION
from .coordinator import AnovaNanoDataUpdateCoordinator


class AnovaNanoEntity(PassiveBluetoothCoordinatorEntity[AnovaNanoDataUpdateCoordinator]):
    """AnovaNanoEntity class."""

    _attr_attribution = ATTRIBUTION
    _attr_has_entity_name = True

    def __init__(self, coordinator: AnovaNanoDataUpdateCoordinator) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_unique_id = coordinator.config_entry.entry_id
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self.unique_id)},
            name=NAME,
            model=VERSION,
            manufacturer=NAME,
        )
        self.coordinator: AnovaNanoDataUpdateCoordinator = coordinator

    @property
    def status(self) -> SensorValues:
        return self.coordinator.status

    @property
    def parsed_data(self) -> dict[str, Any]:
        """Return parsed device data for this entity."""
        return self.coordinator.status.__dict__


class AnovaNanoDescriptionEntity(AnovaNanoEntity):
    """Defines an Anova Nano entity that uses a description."""

    def __init__(
        self,
        coordinator: AnovaNanoDataUpdateCoordinator,
        description: EntityDescription,
    ) -> None:
        """Initialize the entity and declare unique id based on description key."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{coordinator.config_entry.entry_id}_{description.key}"
