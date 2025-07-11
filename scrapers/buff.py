import requests
import urllib.parse

def get_buff_price(skin_name):
    query = urllib.parse.quote(skin_name)
    url = f"https://buff.163.com/api/market/goods?game=csgo&page_num=1&search={query}"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://buff.163.com/market/csgo",
        "Accept": "application/json",
    }

    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()

        items = data.get("data", {}).get("items", [])
        if not items:
            print(f"[WARN][Buff] No match for: {skin_name}")
            return None

        item = items[0]
        return {
            "market": "buff163",
            "title": item["goods_info"]["market_hash_name"],
            "price": f'{item["sell_min_price"]} ¥'
        }

    except Exception as e:
        print(f"[ERROR][Buff] {skin_name}: {e}")
        return None
