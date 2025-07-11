import requests
from bs4 import BeautifulSoup

def get_steam_price(skin_name):
    query = skin_name.replace(" ", "+")
    url = f"https://steamcommunity.com/market/search?q={query}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    item = soup.find("span", class_="market_listing_item_name")
    price = soup.find("span", class_="normal_price")
    if not item or not price:
        return None
    
    return {"market": "steam", "title": item.text.strip(), "price": price.text.strip()}