"""DataUpdateCoordinator for CREG EV Prices."""
import logging
from datetime import timedelta
import aiohttp

from bs4 import BeautifulSoup

from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_change
import homeassistant.util.dt as dt_util

from .const import DOMAIN

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
            update_interval=None,
        )
        
        # Schedule the update for the 1st of the month at 1:00 AM
        async_track_time_change(
            hass,
            self._async_scheduled_update,
            hour=1,
            minute=0,
            second=0
        )

    @callback
    async def _async_scheduled_update(self, now):
        """Update data if it's the first day of the month."""
        if now.day == 1:
            _LOGGER.debug("First of the month, requesting data update.")
            await self.async_request_refresh()

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
                
                # Calculate current quarter string (e.g. "Q2/2026")
                now = dt_util.now()
                current_quarter = (now.month - 1) // 3 + 1
                target_quarter_str = f"Q{current_quarter}/{now.year}"

                tbody = table.find("tbody")
                if not tbody:
                    raise UpdateFailed("Could not find tbody in the price table.")
                    
                # Find the row matching the current quarter
                target_row = None
                for row in tbody.find_all("tr"):
                    th = row.find("th")
                    if th and th.text.strip().replace(" ", "") == target_quarter_str:
                        target_row = row
                        break
                        
                if not target_row:
                    raise UpdateFailed(f"Could not find row for current quarter: {target_quarter_str}")
                    
                cols = target_row.find_all("td")
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
