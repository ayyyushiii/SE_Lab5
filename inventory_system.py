"""
Inventory System Module

This module provides functions for managing a simple in-memory inventory system.
It supports adding, removing, saving, and loading inventory data with proper
logging, validation, and error handling. The module also adheres to PEP8 style
guidelines and is fully compliant with static analysis tools (Pylint, Flake8, Bandit).
"""

import json
import logging
from datetime import datetime
import ast


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# Global inventory dictionary
STOCK_DATA = {}


def add_item(item="default", qty=0, logs=None):
    """
    Add a specified quantity of an item to the inventory.

    Args:
        item (str): Name of the item to add.
        qty (int or float): Quantity to add.
        logs (list): Optional list for operation logs.

    Returns:
        None
    """
    if logs is None:
        logs = []

    if not isinstance(item, str):
        logger.warning("Invalid item type: %s", type(item))
        return

    if not isinstance(qty, (int, float)):
        logger.warning("Invalid quantity type: %s", type(qty))
        return

    STOCK_DATA[item] = STOCK_DATA.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")
    logger.info("Added %d of %s", qty, item)


def remove_item(item, qty):
    """
    Remove or decrease quantity of an item from inventory.

    Args:
        item (str): Item name.
        qty (int or float): Quantity to remove.

    Returns:
        None
    """
    if item not in STOCK_DATA:
        logger.warning("Item '%s' not found in inventory.", item)
        return

    try:
        STOCK_DATA[item] -= qty
        if STOCK_DATA[item] <= 0:
            del STOCK_DATA[item]
            logger.info("Removed %s from inventory.", item)
    except (KeyError, TypeError) as err:
        logger.error("Error removing item: %s", err)


def get_qty(item):
    """
    Retrieve quantity of a specific item.

    Args:
        item (str): Item name.

    Returns:
        int or float: Quantity of the item if it exists, otherwise 0.
    """
    return STOCK_DATA.get(item, 0)


def load_data(file_path="inventory.json"):
    """
    Load stock data from a JSON file safely.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        None
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        if isinstance(data, dict):
            STOCK_DATA.clear()
            STOCK_DATA.update(data)
            logger.info("Inventory data loaded from %s", file_path)
        else:
            logger.error("Invalid data format in %s", file_path)
    except FileNotFoundError:
        logger.warning("File %s not found. Starting with empty inventory.", file_path)
    except json.JSONDecodeError as err:
        logger.error("Invalid JSON in %s: %s", file_path, err)


def save_data(file_path="inventory.json"):
    """
    Save the stock data to a JSON file safely.

    Args:
        file_path (str): Path to the JSON file.

    Returns:
        None
    """
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(STOCK_DATA, file, indent=4)
        logger.info("Inventory data saved to %s", file_path)
    except OSError as err:
        logger.error("Error saving file %s: %s", file_path, err)


def print_data():
    """
    Print all current inventory items and their quantities.

    Returns:
        None
    """
    logger.info("Inventory Report:")
    for item, qty in STOCK_DATA.items():
        logger.info("%s -> %s", item, qty)


def check_low_items(threshold=5):
    """
    Return a list of items with quantity below the given threshold.

    Args:
        threshold (int): Quantity limit for low-stock detection.

    Returns:
        list: Items below the threshold quantity.
    """
    return [i for i, q in STOCK_DATA.items() if q < threshold]


def main():
    """
    Main function to demonstrate inventory operations.

    Returns:
        None
    """
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # Invalid types handled gracefully
    remove_item("apple", 3)
    remove_item("orange", 1)
    logger.info("Apple stock: %d", get_qty("apple"))
    logger.info("Low items: %s", check_low_items())
    save_data()
    load_data()
    print_data()

    # Safe replacement for eval
    user_input = "{'msg': 'Hello'}"
    try:
        parsed_data = ast.literal_eval(user_input)
        logger.info("Parsed data: %s", parsed_data)
    except (ValueError, SyntaxError) as err:
        logger.warning("Failed to parse input safely: %s", err)


if __name__ == "__main__":
    main()
