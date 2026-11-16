import unittest

from inventory import add_product, adjust, low_stock, reorder_report, total_units


class InventoryTests(unittest.TestCase):
    def setUp(self):
        self.inventory = []
        add_product(self.inventory, "A1", "Keyboard", 5, 2)
        add_product(self.inventory, "B2", "Mouse", 1, 3)

    def test_add_product(self):
        self.assertEqual(self.inventory[0]["name"], "Keyboard")

    def test_add_rejects_duplicate_sku(self):
        with self.assertRaises(ValueError):
            add_product(self.inventory, "A1", "Other")

    def test_add_rejects_negative_quantity(self):
        with self.assertRaises(ValueError):
            add_product(self.inventory, "C3", "Cable", -1)

    def test_adjust_changes_stock(self):
        adjust(self.inventory, "A1", -2)
        self.assertEqual(self.inventory[0]["quantity"], 3)

    def test_adjust_rejects_negative_stock(self):
        with self.assertRaises(ValueError):
            adjust(self.inventory, "A1", -6)

    def test_adjust_unknown_sku(self):
        with self.assertRaises(KeyError):
            adjust(self.inventory, "ZZ", 1)

    def test_low_stock(self):
        self.assertEqual([item["sku"] for item in low_stock(self.inventory)], ["B2"])

    def test_total_units(self):
        self.assertEqual(total_units(self.inventory), 6)


class ReorderReportTests(unittest.TestCase):
    def test_only_low_stock_items_included(self):
        inventory = []
        add_product(inventory, "A1", "Keyboard", 5, 2)
        add_product(inventory, "B2", "Mouse", 1, 3)
        add_product(inventory, "C3", "Cable", 0, 4)
        report = reorder_report(inventory)
        self.assertEqual([item["sku"] for item in report], ["B2", "C3"])

    def test_needed_is_reorder_level_minus_quantity(self):
        inventory = []
        add_product(inventory, "B2", "Mouse", 1, 3)
        self.assertEqual(reorder_report(inventory)[0]["needed"], 2)

    def test_report_sorted_by_sku(self):
        inventory = []
        add_product(inventory, "C3", "Cable", 0, 4)
        add_product(inventory, "A1", "Keyboard", 0, 2)
        add_product(inventory, "B2", "Mouse", 1, 3)
        report = reorder_report(inventory)
        self.assertEqual([item["sku"] for item in report], ["A1", "B2", "C3"])

    def test_empty_inventory(self):
        self.assertEqual(reorder_report([]), [])


class ExportTests(unittest.TestCase):
    def test_export_csv(self):
        import csv
        import os
        import tempfile

        from inventory import add_product, export_csv

        inventory = []
        add_product(inventory, "A1", "Keyboard", 5, 2)
        add_product(inventory, "B2", "Mouse", 1, 3)
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "inventory.csv")
            export_csv(inventory, path)
            with open(path, encoding="utf-8") as handle:
                rows = list(csv.reader(handle))
        self.assertEqual(rows[0], ["sku", "name", "quantity", "reorder_level"])
        self.assertEqual(rows[1][0], "A1")
        self.assertEqual(len(rows), 3)


if __name__ == "__main__":
    unittest.main()
