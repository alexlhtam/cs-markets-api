import requests
from scrapers.skinport import get_skinport_price
from scrapers.steam import get_steam_price
from scrapers.buff import get_buff_price

def load_tracked_skins(path="tracked_skins.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        print(f"[WARN] No tracked_skins.txt found at {path}")
        return set()

def fetch_inventory(steam_id):
    url = f"https://steamcommunity.com/inventory/{steam_id}/730/2"
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

def get_skin_names_from_inventory(inventory_json):
    return list({
        item['market_hash_name']
        for item in inventory_json.get("descriptions", [])
        if "market_hash_name" in item
    })
    
def get_prices_for_inventory(steam_id):
    print(f"[DEBUG] Fetching inventory for {steam_id}")
    
    inventory = fetch_inventory(steam_id)
    all_names = get_skin_names_from_inventory(inventory)
    tracked_skins = load_tracked_skins()
    
    names = [name for name in all_names if name in tracked_skins]
    print(f"[DEBUG] Matched tracked skins: {names}")
    
   
    
    results = []
    for name in names:
        skin_data = {"name": name}
        for fetcher in [get_skinport_price, get_steam_price, get_buff_price]:
            try:
                result = fetcher(name)
                print(f"[DEBUG] fetcher: {fetcher.__name__}, result: {result}")
                if isinstance(result, dict) and "market" in result and "price" in result:
                    skin_data[result["market"]] = result["price"]
                else:
                    skin_data[fetcher.__name__] = "not_found"
            except Exception as e:
                skin_data[fetcher.__name__] = f"error: {str(e)}"
        results.append(skin_data)
        
    print(f"[DEBUG] Final result: {results}")

    return results