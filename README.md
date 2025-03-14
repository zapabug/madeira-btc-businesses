# Madeira Bitcoin Businesses

This tool fetches and processes data about Bitcoin-accepting businesses in Madeira, Portugal.

## Overview

The script fetches data from the BTCMap API and filters for businesses located in Madeira. It identifies businesses through:

1. Location filtering (matching city and region names)
2. Geographical proximity to Funchal
3. Exclusion of non-Madeira locations with similar names

## Features

- Fetches data from the BTCMap API
- Filters businesses in Madeira locations
- Excludes businesses from non-Madeira locations (e.g., Santa Cruz de Tenerife)
- Calculates distance using the Haversine formula
- Formats and saves business information to a JSON file
- Organizes businesses by location

## Usage

1. Install requirements: `pip install -r requirements.txt`
2. Run the script: `python madeira_btc_businesses.py`

The script will output a JSON file with all Bitcoin-accepting businesses in Madeira.

## Data Format

The data is structured as follows:

```json
[
  {
    "name": "Business Name",
    "type": "Business Type",
    "address": {
      "street": "Street Address",
      "housenumber": "Number",
      "city": "City",
      "region": "Region",
      "postcode": "Postal Code"
    },
    "contact": {
      "phone": "Phone Number",
      "website": "Website URL"
    },
    "opening_hours": "Opening Hours",
    "coordinates": [longitude, latitude],
    "bitcoin_payment": {
      "bitcoin": "yes/no/unknown",
      "lightning": "yes/no/unknown",
      "onchain": "yes/no/unknown"
    }
  }
]
```

## License

MIT 