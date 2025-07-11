from fastapi import FastAPI, Query
from inventory_tracker import get_prices_for_inventory

app = FastAPI()

@app.get("/inventory-prices")
def inventory_prices(steam_id: str = Query(..., description="Your 64-bit SteamID")):
    try:
        result = get_prices_for_inventory(steam_id)
        return {"status": "ok", "inventory": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}
