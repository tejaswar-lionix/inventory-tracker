import unittest

from inventory import add_product, adjust, low_stock, total_units


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


if __name__ == "__main__":
    unittest.main()
