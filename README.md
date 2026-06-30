# CREG EV Prices for Home Assistant

This is a custom integration for Home Assistant that tracks the Belgian CREG EV reimbursement rates (€/kWh) for Flanders, Brussels, and Wallonia.

The rates are updated quarterly by the CREG. This integration fetches the data once a day to ensure you always have the latest values without overloading their servers.

## Features
- Provides 3 sensors, one for each region (Flanders, Brussels, Wallonia).
- Setup entirely via the Home Assistant UI (Config Flow).
- Compatible with HACS.

## Installation

### HACS (Recommended)
1. Open HACS in your Home Assistant instance.
2. Go to **Integrations** -> **Custom repositories**.
3. Add the URL of this repository and select **Integration** as the category.
4. Click **Install** on the CREG EV Prices card.
5. Restart Home Assistant.
6. Go to **Settings** -> **Devices & Services** -> **Add Integration** and search for "CREG EV Prices".

### Manual Installation
1. Copy the `custom_components/creg_ev_prices` folder into your Home Assistant `config/custom_components` directory.
2. Restart Home Assistant.
3. Go to **Settings** -> **Devices & Services** -> **Add Integration** and search for "CREG EV Prices".
