# inventory-tracker

Track product stock levels and low-stock alerts.

## Usage

```bash
python3 -c "from inventory import *; i=add_product([], 'A1', 'Keyboard', 5, 2); print(low_stock(i))"
python3 -c "from inventory import *; i=add_product([], 'A1', 'Keyboard', 1, 5); print(reorder_report(i))"
python3 -c "from inventory import *; i=add_product([], 'A1', 'Keyboard', 1, 5); print(apply_reorders(i))"
python3 -c "from inventory import *; i=add_product([], 'A1', 'Keyboard', 5, 2); print(find_product(i, 'A1'))"
python3 -c "from inventory import *; i=add_product([], 'A1', 'Keyboard', 5, 2); print(search(i, 'keyboard'))"
```

## Features

- Products with unique SKUs and reorder levels
- Stock adjustments that cannot go negative
- Reorder reports with reorder_report(inventory)
- Apply reorders with apply_reorders(inventory)
- CSV export with export_csv(inventory, path)
- Look up and remove products with find_product(inventory, sku) and remove_product(inventory, sku)
- Search by SKU or name with search(inventory, query)

## Tests

```bash
python3 -m unittest -q
```

## Additional API

- `stock_summary(inventory)` reports product, unit, and low-stock counts.

## License

MIT
