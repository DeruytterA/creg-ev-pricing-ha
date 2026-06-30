"""DataUpdateCoordinator for CREG EV Prices."""
import logging
from datetime import timedelta
import aiohttp

from bs4 import BeautifulSoup

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, UPDATE_INTERVAL_HOURS

_LOGGER = logging.getLogger(__name__)

class CregEvPricesDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching CREG EV Prices data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize."""
        self.session = async_get_clientsession(hass)
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=UPDATE_INTERVAL_HOURS),
        )

    async def _async_update_data(self):
        """Fetch data from CREG."""
        try:
            url = "https://www.creg.be/nl/consumenten/prijzen-en-tarieven/creg-tarief-voor-terugbetaling-thuisladen-bedrijfswagens"
            
            # Using Home Assistant's built-in aiohttp session
            async with self.session.get(url, timeout=10) as response:
                response.raise_for_status()
                html_content = await response.text()
                
                soup = BeautifulSoup(html_content, "html.parser")
                
                # Find the table by class
                table = soup.find("table", class_="table-bordered")
                if not table:
                    raise UpdateFailed("Could not find the price table on the CREG website.")
                
                # We need the first row from the tbody (latest quarter)
                tbody = table.find("tbody")
                if not tbody:
                    raise UpdateFailed("Could not find tbody in the price table.")
                    
                first_row = tbody.find("tr")
                if not first_row:
                    raise UpdateFailed("Could not find any rows in the price table.")
                    
                cols = first_row.find_all("td")
                if len(cols) < 3:
                    raise UpdateFailed("Unexpected table structure: less than 3 columns in a row.")
                    
                # Extract and parse values. Replace ',' with '.' and divide by 100 (c€ -> €)
                try:
                    flanders_price = float(cols[0].text.strip().replace(",", ".")) / 100.0
                    brussels_price = float(cols[1].text.strip().replace(",", ".")) / 100.0
                    wallonia_price = float(cols[2].text.strip().replace(",", ".")) / 100.0
                except ValueError as err:
                    raise UpdateFailed(f"Could not parse price values: {err}") from err
                    
                _LOGGER.debug(
                    "Fetched new CREG prices: Flanders: %s, Brussels: %s, Wallonia: %s", 
                    flanders_price, brussels_price, wallonia_price
                )
                
                return {
                    "Flanders": flanders_price,
                    "Brussels": brussels_price,
                    "Wallonia": wallonia_price
                }
                
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err
        except Exception as err:
            raise UpdateFailed(f"Unexpected error: {err}") from err
