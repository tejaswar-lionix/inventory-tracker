#!/usr/bin/env python3
"""Track product stock levels in a JSON file."""
import json
import os

DEFAULT_PATH = os.path.expanduser("~/.inventory.json")


def load(path=DEFAULT_PATH):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def save(inventory, path=DEFAULT_PATH):
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(inventory, handle, indent=2)


def add_product(inventory, sku, name, quantity=0, reorder_level=0):
    if not sku.strip() or not name.strip():
        raise ValueError("sku and name must not be empty")
    if any(product["sku"] == sku for product in inventory):
        raise ValueError("duplicate sku")
    if quantity < 0 or reorder_level < 0:
        raise ValueError("quantities must not be negative")
    inventory.append(
        {
            "sku": sku.strip(),
            "name": name.strip(),
            "quantity": quantity,
            "reorder_level": reorder_level,
        }
    )
    return inventory


def adjust(inventory, sku, delta):
    for product in inventory:
        if product["sku"] == sku:
            if product["quantity"] + delta < 0:
                raise ValueError("stock cannot go negative")
            product["quantity"] += delta
            return product
    raise KeyError(f"unknown sku: {sku}")


def low_stock(inventory):
    return [
        product
        for product in inventory
        if product["quantity"] <= product["reorder_level"]
    ]


def total_units(inventory):
    return sum(product["quantity"] for product in inventory)
