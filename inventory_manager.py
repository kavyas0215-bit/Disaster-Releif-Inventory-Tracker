import json
import os
from datetime import datetime

DEFAULT_FILE_PATH = os.path.join(os.path.dirname(__file__), "inventory.json")

def load_inventory(file_path=DEFAULT_FILE_PATH):
    """
    Loads the inventory from the specified JSON file.
    Returns an empty dictionary if the file does not exist or contains invalid JSON.
    """
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def save_inventory(inventory, file_path=DEFAULT_FILE_PATH):
    """
    Saves the inventory dictionary to the specified JSON file.
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(inventory, f, indent=2, ensure_ascii=False)
        return True
    except IOError:
        return False

def add_item(inventory, name, category, quantity, unit, threshold, file_path=DEFAULT_FILE_PATH):
    """
    Adds a new item to the inventory or updates an existing item.
    """
    name = name.strip()
    if not name:
        raise ValueError("Item name cannot be empty.")
    
    # Capitalize item name for consistency
    name = name.title()
    
    inventory[name] = {
        "category": category,
        "quantity": int(quantity),
        "unit": unit,
        "threshold": int(threshold),
        "last_updated": datetime.now().isoformat()
    }
    
    return save_inventory(inventory, file_path)

def update_stock(inventory, name, quantity_change, file_path=DEFAULT_FILE_PATH):
    """
    Updates the stock quantity of an existing item.
    quantity_change can be positive (replenishment) or negative (distribution).
    """
    if name not in inventory:
        return False
        
    current_qty = inventory[name]["quantity"]
    new_qty = current_qty + int(quantity_change)
    
    if new_qty < 0:
        raise ValueError(f"Insufficient stock. Cannot reduce stock by {-quantity_change}. Current stock is {current_qty}.")
        
    inventory[name]["quantity"] = new_qty
    inventory[name]["last_updated"] = datetime.now().isoformat()
    
    return save_inventory(inventory, file_path)

def delete_item(inventory, name, file_path=DEFAULT_FILE_PATH):
    """
    Removes an item from the inventory.
    """
    if name in inventory:
        del inventory[name]
        return save_inventory(inventory, file_path)
    return False

def get_low_stock_alerts(inventory):
    """
    Identifies items that are at or below their safety threshold.
    Returns a dictionary of low stock items.
    """
    alerts = {}
    for name, details in inventory.items():
        if details["quantity"] <= details["threshold"]:
            alerts[name] = details
    return alerts

def get_inventory_report(inventory):
    """
    Generates summary report statistics from the inventory.
    """
    total_items = len(inventory)
    total_quantities = sum(item["quantity"] for item in inventory.values())
    
    category_summary = {}
    for item in inventory.values():
        cat = item["category"]
        category_summary[cat] = category_summary.get(cat, 0) + item["quantity"]
        
    low_stock_count = len(get_low_stock_alerts(inventory))
    
    return {
        "total_items": total_items,
        "total_quantities": total_quantities,
        "category_summary": category_summary,
        "low_stock_count": low_stock_count
    }
