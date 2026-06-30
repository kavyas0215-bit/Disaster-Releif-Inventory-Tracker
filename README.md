# Disaster-Releif-Inventory-Tracker
# Implementation Plan - Disaster Relief Inventory Tracker

This plan outlines the design and implementation of a **Disaster Relief Inventory Tracker** in Python and Streamlit. The application will store inventory data in a JSON file and provide an interactive dashboard for managing supplies, updating stocks, generating reports, and tracking low-stock alerts.

## Proposed Project Structure

We will organize the code cleanly:
* `inventory.json`: Data store for the supplies.
* `inventory_manager.py`: Core python functions containing functions for loading, saving, adding, updating, and analyzing inventory.
* `app.py`: Streamlit-based web dashboard.
* `requirements.txt`: Python package dependencies.

---

## Technical Specifications

### 1. JSON Data Structure (`inventory.json`)
The inventory will be stored as a dictionary of items. Each item will have properties representing its category, quantity, unit, threshold (for low-stock alerts), and last updated timestamp:
```json
{
  "Water Bottles": {
    "category": "Water & Sanitation",
    "quantity": 1200,
    "unit": "liters",
    "threshold": 500,
    "last_updated": "2026-06-30T12:00:00"
  },
  "First Aid Kit": {
    "category": "Medical Supplies",
    "quantity": 45,
    "unit": "boxes",
    "threshold": 50,
    "last_updated": "2026-06-30T11:45:00"
  }
}
```

### 2. Core Logic (`inventory_manager.py`)
This file will contain pure Python functions demonstrating the use of **dictionaries**, **JSON operations**, and modular code:
- `load_inventory()`: Load inventory from `inventory.json`.
- `save_inventory(inventory)`: Save dictionary back to `inventory.json`.
- `add_item(name, category, quantity, unit, threshold)`: Add a new supply item or increment if it exists.
- `update_stock(name, quantity_change)`: Adjust stock levels (positive for replenishment, negative for distribution).
- `get_stock_report()`: Return summary statistics (total items, categories, critical low stock list).

### 3. Streamlit Interface (`app.py`)
A highly polished, responsive dashboard containing:
* **Sidebar**: Navigation (Dashboard, Manage Supplies, Transactions / Log).
* **Extended Dashboard & Report Section**:
  * Visual metrics (total inventory count, category breakdowns).
  * **Low-Stock Alerts**: Warning banners if items fall below their threshold.
  * Searchable and filterable data table of current inventory.
* **Manage Supplies Form (Basic / Intermediate)**:
  * Add new item with category, unit, quantity, and safety threshold.
  * Dropdown selector to update stock (distribution/replenishment) for existing items with simple visual indicators.

---

## Proposed Changes

### [NEW] [requirements.txt](file:///c:/Users/AnudipCOA/OneDrive/Desktop/disaster%20relief%20management/requirements.txt)
Defines project dependencies.
- `streamlit`

### [NEW] [inventory_manager.py](file:///c:/Users/AnudipCOA/OneDrive/Desktop/disaster%20relief%20management/inventory_manager.py)
Core utility module for file storage and inventory logic.

### [NEW] [app.py](file:///c:/Users/AnudipCOA/OneDrive/Desktop/disaster%20relief%20management/app.py)
Streamlit application.

### [NEW] [inventory.json](file:///c:/Users/AnudipCOA/OneDrive/Desktop/disaster%20relief%20management/inventory.json)
Initial dataset with template inventory items.

---

## Verification Plan

### Automated/Manual Validation
1. Install dependencies via pip.
2. Run the application locally: `streamlit run app.py`
3. Test core operations:
   - Add a new item and verify it is written to `inventory.json`.
   - Update quantity and verify that negative changes decrement the stock and generate low-stock warnings when appropriate.
   - Verify searching and category filtering on the main dashboard.
