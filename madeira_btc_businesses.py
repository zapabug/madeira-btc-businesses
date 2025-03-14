import requests
import json
from datetime import datetime
from math import radians, cos, sin, sqrt, atan2

# Function to calculate distance between two points using the Haversine formula
def haversine(lon1, lat1, lon2, lat2):
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r

# Coordinates for Funchal, Madeira
funchal_lon, funchal_lat = -16.9186, 32.6669

def fetch_btc_businesses():
    # BTCMap API endpoint
    api_url = "https://api.btcmap.org/v2/elements"
    
    # Major cities/areas in Madeira for filtering
    madeira_locations = ['funchal', 'caniço', 'machico', 'santa cruz', 'câmara de lobos', 
                        'ribeira brava', 'ponta do sol', 'calheta', 'porto moniz',
                        'são vicente', 'santana', 'camacha', 'porto santo']
    
    # Locations to exclude (not part of Madeira)
    exclude_locations = ['santa cruz de tenerife', 'santa cruz de la sierra', 
                         'santa cruz do sul', 'santa cruz cabrália', 'santa cruz la laguna',
                         'feira de santana']
    
    # Search radius in km from Funchal (covers most of Madeira island)
    search_radius = 50
    
    try:
        # Fetch data from API
        print(f"Fetching data from {api_url}...")
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        
        print(f"Received {len(data)} elements from the API")
        
        # Extract Madeira businesses
        madeira_businesses = []
        for entry in data:
            osm_json = entry.get('osm_json', {})
            tags = osm_json.get('tags', {})
            
            # Skip if no tags
            if not tags:
                continue
                
            # Get location information
            city = tags.get('addr:city', '').lower()
            region = tags.get('addr:region', '').lower()
            
            # Check coordinates
            lat = osm_json.get('lat', 0)
            lon = osm_json.get('lon', 0)
            
            # Check if the business is in Madeira (any of these conditions)
            in_madeira = False
            
            # Exclude any cities that are explicitly not in Madeira
            if any(excluded in city for excluded in exclude_locations):
                continue
                
            # 1. Check if region is Madeira
            if 'madeira' in region:
                in_madeira = True
                
            # 2. Check if city is in one of the Madeira locations
            if any(location in city for location in madeira_locations):
                in_madeira = True
                
            # 3. Check if within the search radius of Funchal
            if lat and lon:  # If coordinates are available
                distance = haversine(funchal_lon, funchal_lat, lon, lat)
                if distance <= search_radius:
                    in_madeira = True
            
            # If the business is in Madeira, add it to our list
            if in_madeira:
                business_info = {
                    'name': tags.get('name', 'Unknown'),
                    'type': tags.get('amenity') or tags.get('shop') or 'Unknown',
                    'address': {
                        'street': tags.get('addr:street', ''),
                        'housenumber': tags.get('addr:housenumber', ''),
                        'city': city,
                        'region': region,
                        'postcode': tags.get('addr:postcode', ''),
                    },
                    'contact': {
                        'phone': tags.get('phone', ''),
                        'website': tags.get('website', ''),
                    },
                    'opening_hours': tags.get('opening_hours', ''),
                    'coordinates': [lon, lat],
                    'bitcoin_payment': {
                        'bitcoin': tags.get('payment:bitcoin', 'unknown'),
                        'lightning': tags.get('payment:lightning', 'unknown'),
                        'onchain': tags.get('payment:onchain', 'unknown'),
                    },
                    'tags': tags
                }
                madeira_businesses.append(business_info)
        
        print(f"Found {len(madeira_businesses)} Bitcoin-accepting businesses in Madeira")
        
        # Save to JSON file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = f'madeira_btc_businesses_{timestamp}.json'
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(madeira_businesses, f, indent=2, ensure_ascii=False)
            
        print(f"Data saved to {output_file}")
        
        # Print a few sample businesses by city
        print("\nSample businesses by location:")
        cities = {}
        for business in madeira_businesses:
            city = business['address']['city']
            if city:
                if city not in cities:
                    cities[city] = []
                cities[city].append(business['name'])
        
        for city, businesses in cities.items():
            print(f"\n{city.title()}: {len(businesses)} businesses")
            for name in businesses[:3]:  # Show up to 3 businesses per city
                print(f"- {name}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Print traceback for debugging
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fetch_btc_businesses() 