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


class ProductLookupTests(unittest.TestCase):
    def setUp(self):
        self.inventory = []
        add_product(self.inventory, "A1", "Keyboard", 5, 2)
        add_product(self.inventory, "B2", "Mouse", 1, 3)

    def test_find_existing_product(self):
        from inventory import find_product

        product = find_product(self.inventory, "A1")
        self.assertEqual(product["name"], "Keyboard")

    def test_find_unknown_product_returns_none(self):
        from inventory import find_product

        self.assertIsNone(find_product(self.inventory, "ZZ"))

    def test_remove_existing_product(self):
        from inventory import remove_product

        removed = remove_product(self.inventory, "A1")
        self.assertEqual(removed["name"], "Keyboard")
        self.assertEqual(len(self.inventory), 1)
        self.assertEqual(self.inventory[0]["sku"], "B2")

    def test_remove_unknown_product_raises(self):
        from inventory import remove_product

        with self.assertRaises(KeyError):
            remove_product(self.inventory, "ZZ")


class SearchTests(unittest.TestCase):
    def setUp(self):
        self.inventory = []
        add_product(self.inventory, "A1", "Keyboard", 5, 2)
        add_product(self.inventory, "B2", "Mouse", 1, 3)
        add_product(self.inventory, "C3", "Keyboard Cover", 2, 1)

    def test_sku_match(self):
        from inventory import search

        self.assertEqual([item["sku"] for item in search(self.inventory, "B2")], ["B2"])

    def test_name_match(self):
        from inventory import search

        self.assertEqual(
            [item["sku"] for item in search(self.inventory, "Keyboard")],
            ["A1", "C3"],
        )

    def test_case_insensitive(self):
        from inventory import search

        self.assertEqual(
            [item["sku"] for item in search(self.inventory, "keyboard")],
            ["A1", "C3"],
        )

    def test_no_match(self):
        from inventory import search

        self.assertEqual(search(self.inventory, "monitor"), [])

    def test_empty_query_returns_empty(self):
        from inventory import search

        self.assertEqual(search(self.inventory, ""), [])


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


class ApplyReorderTests(unittest.TestCase):
    def test_tops_multiple_low_items(self):
        from inventory import apply_reorders

        inventory = []
        add_product(inventory, "A1", "Keyboard", 0, 2)
        add_product(inventory, "B2", "Mouse", 1, 3)
        apply_reorders(inventory)
        self.assertEqual(inventory[0]["quantity"], 2)
        self.assertEqual(inventory[1]["quantity"], 3)

    def test_only_changed_items_reported(self):
        from inventory import apply_reorders

        inventory = []
        add_product(inventory, "A1", "Keyboard", 0, 2)
        add_product(inventory, "B2", "Mouse", 5, 3)
        self.assertEqual(apply_reorders(inventory), [{"sku": "A1", "added": 2}])

    def test_above_threshold_untouched(self):
        from inventory import apply_reorders

        inventory = []
        add_product(inventory, "A1", "Keyboard", 5, 2)
        apply_reorders(inventory)
        self.assertEqual(inventory[0]["quantity"], 5)

    def test_empty_inventory(self):
        from inventory import apply_reorders

        self.assertEqual(apply_reorders([]), [])


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


class StockSummaryTests(unittest.TestCase):
    def test_summary_counts(self):
        from inventory import add_product, stock_summary

        inventory = add_product([], "A1", "Keyboard", 5, 2)
        add_product(inventory, "A2", "Mouse", 1, 3)
        self.assertEqual(
            stock_summary(inventory),
            {"products": 2, "total_units": 6, "low_stock": 1},
        )

    def test_empty(self):
        from inventory import stock_summary

        self.assertEqual(
            stock_summary([]),
            {"products": 0, "total_units": 0, "low_stock": 0},
        )


if __name__ == "__main__":
    unittest.main()
