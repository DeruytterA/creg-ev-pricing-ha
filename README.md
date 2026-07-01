# CREG EV Prices for Home Assistant

This is a custom Home Assistant integration that tracks the official Belgian CREG EV reimbursement rates (€/kWh) for charging company cars at home. 

## How it works

The CREG (Commission for the Regulation of Electricity and Gas) publishes these rates quarterly. However, because they often publish future quarters in advance, this integration is built to be smart:

- **Monthly Polling**: On the **1st of every month at 1:00 AM**, the integration wakes up and scrapes the official CREG website.
- **Current Quarter Matching**: Instead of just grabbing the latest published number, it calculates the *current* calendar quarter and dynamically searches the CREG table to extract the exact rate applicable for today.

## Sensors Provided

Once configured, the integration provides 3 separate sensors, one for each region. 
The entity names will be:
- **Flanders** (`sensor.creg_ev_price_flanders`)
- **Brussels** (`sensor.creg_ev_price_brussels`)
- **Wallonia** (`sensor.creg_ev_price_wallonia`)

All sensors use `€/kWh` as their unit of measurement and are configured with the `monetary` device class, making them perfect for use in Home Assistant's Energy Dashboard.

## Installation

### HACS (Recommended)
This integration is fully compatible with HACS (Home Assistant Community Store).
1. Open HACS in your Home Assistant instance.
2. Go to **Integrations** -> **Custom repositories** (via the 3 dots in the top right).
3. Add the URL of this repository and select **Integration** as the category.
4. Click **Install** on the CREG EV Prices card.
5. Restart Home Assistant.
6. Go to **Settings** -> **Devices & Services** -> **Add Integration** and search for "CREG EV Prices".

### Manual Installation
1. Copy the `custom_components/creg_ev_prices` folder into your Home Assistant `config/custom_components` directory.
2. Restart Home Assistant.
3. Go to **Settings** -> **Devices & Services** -> **Add Integration** and search for "CREG EV Prices".
