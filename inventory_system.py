import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

stock_data = {}

def add_item(item="default", qty=0, logs=None):
    if logs is None:
        logs = []
    
    # Validate inputs
    if not isinstance(item, str) or not isinstance(qty, int):
        logging.error("Invalid item or quantity type")
        return
    
    if qty <= 0:
        logging.warning("Quantity should be positive")
        return
    
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logging.info(f"Added {qty} of {item}")

def remove_item(item, qty):
    if not isinstance(item, str) or not isinstance(qty, int) or qty <= 0:
        logging.error("Invalid item or quantity for removal")
        return
    
    if item in stock_data:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
            logging.info(f"Removed {item} completely")
        else:
            logging.info(f"Removed {qty} of {item}")
    else:
        logging.warning(f"Item '{item}' not found")

def get_qty(item):
    return stock_data.get(item, 0)

def load_data(file="inventory.json"):
    global stock_data
    try:
        with open(file, "r") as f:
            stock_data = json.load(f)
            logging.info("Data loaded successfully")
    except FileNotFoundError:
        logging.warning("File not found, starting with empty inventory")
        stock_data = {}

def save_data(file="inventory.json"):
    with open(file, "w") as f:
        json.dump(stock_data, f)
        logging.info("Data saved successfully")

def print_data():
    print("\nItems Report")
    for item, qty in stock_data.items():
        print(f"{item} -> {qty}")

def check_low_items(threshold=5):
    return [item for item, qty in stock_data.items() if qty < threshold]

def main():
    add_item("apple", 10)
    add_item("banana", 2)
    add_item("mango", 3)
    remove_item("apple", 3)
    remove_item("orange", 1)
    
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    
    save_data()
    load_data()
    print_data()

if __name__ == "__main__":
    main()
