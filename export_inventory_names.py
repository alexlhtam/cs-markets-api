import json
from inventory_tracker import fetch_inventory

def export_inventory_names_to_file(steam_id, output_path="market_names.txt"):
    inventory = fetch_inventory(steam_id)
    names = sorted({
        item["market_hash_name"]
        for item in inventory.get("descriptions", [])
        if "market_hash_name" in item
    })
    
    with open(output_path, "w", encoding="utf-8") as f:
        for name in names:
            f.write(name + "\n")
            
            
    print(f"[INFO] Exported {len(names)} skins to {output_path}")
    
if __name__ == "__main__":
    export_inventory_names_to_file("76561199202390918")