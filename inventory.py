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


def find_product(inventory, sku):
    for product in inventory:
        if product["sku"] == sku:
            return product
    return None


def remove_product(inventory, sku):
    for index, product in enumerate(inventory):
        if product["sku"] == sku:
            return inventory.pop(index)
    raise KeyError(f"unknown sku: {sku}")


def search(inventory, query):
    text = query.strip().lower()
    if not text:
        return []
    return [
        product
        for product in inventory
        if text in product["sku"].lower() or text in product["name"].lower()
    ]


def low_stock(inventory):
    return [
        product
        for product in inventory
        if product["quantity"] <= product["reorder_level"]
    ]


def reorder_report(inventory):
    report = [
        {
            "sku": product["sku"],
            "name": product["name"],
            "quantity": product["quantity"],
            "reorder_level": product["reorder_level"],
            "needed": product["reorder_level"] - product["quantity"],
        }
        for product in low_stock(inventory)
    ]
    return sorted(report, key=lambda item: item["sku"])


def apply_reorders(inventory):
    """Top low-stock items up to their reorder level."""
    applied = []
    for product in low_stock(inventory):
        added = product["reorder_level"] - product["quantity"]
        if added > 0:
            product["quantity"] = product["reorder_level"]
            applied.append({"sku": product["sku"], "added": added})
    return sorted(applied, key=lambda item: item["sku"])


def total_units(inventory):
    return sum(product["quantity"] for product in inventory)


def export_csv(inventory, path):
    """Export the inventory to a CSV file."""
    import csv

    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sku", "name", "quantity", "reorder_level"])
        for product in inventory:
            writer.writerow(
                [
                    product["sku"],
                    product["name"],
                    product["quantity"],
                    product["reorder_level"],
                ]
            )
    return path
