"""Sensor platform for CREG EV Prices."""
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.const import CURRENCY_EURO

from .const import DOMAIN, REGIONS
from .coordinator import CregEvPricesDataUpdateCoordinator

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: CregEvPricesDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [
        CregEvPriceSensor(coordinator, region)
        for region in REGIONS
    ]
    
    async_add_entities(sensors)

class CregEvPriceSensor(CoordinatorEntity[CregEvPricesDataUpdateCoordinator], SensorEntity):
    """Representation of a CREG EV Price Sensor."""

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.MONETARY
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = f"{CURRENCY_EURO}/kWh" # Usually €/kWh

    def __init__(
        self,
        coordinator: CregEvPricesDataUpdateCoordinator,
        region: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.region = region
        self._attr_unique_id = f"creg_ev_price_{region.lower()}"
        
        # Name will be translated or use fallback
        self._attr_translation_key = f"price_{region.lower()}"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data is not None:
            return self.coordinator.data.get(self.region)
        return None

    @property
    def device_info(self):
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, "creg_ev_prices")},
            "name": "CREG EV Prices",
            "manufacturer": "CREG",
            "entry_type": "service",
        }
