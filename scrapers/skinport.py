import requests
import urllib.parse
import re
from difflib import get_close_matches

def get_skinport_price(skin_name):
    try:
        # Simplify search name
        query_name = re.sub(r"\(.*?\)", "", skin_name)  # remove wear
        query_name = re.sub(r"[★™]", "", query_name)    # remove unicode
        query_name = query_name.strip()

        encoded_query = urllib.parse.quote(query_name)
        url = (
            "https://api.skinport.com/api/browse-market"
            f"?appId=730&currency=USD&sort=price&order=asc&search={encoded_query}"
        )

        headers = {"User-Agent": "Mozilla/5.0"}

        # Handle Skinport 404 with graceful fallback
        response = requests.get(url, headers=headers)
        if response.status_code == 404:
            print(f"[WARN][Skinport] No results (404) for: {skin_name}")
            return None

        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])

        if not items:
            print(f"[WARN][Skinport] No items found in response for: {skin_name}")
            return None

        # Fuzzy match from returned market names
        market_names = [item["marketHashName"] for item in items]
        match = get_close_matches(skin_name, market_names, n=1, cutoff=0.6)
        if match:
            matched_item = next(item for item in items if item["marketHashName"] == match[0])
            return {
                "market": "skinport",
                "title": matched_item["marketHashName"],
                "price": f"${matched_item['minPrice']:.2f}"
            }

        print(f"[WARN][Skinport] No close match for: {skin_name}")
        return None

    except Exception as e:
        print(f"[ERROR][Skinport] {skin_name}: {e}")
        return None
