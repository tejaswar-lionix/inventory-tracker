# inventory-tracker

Track product stock levels and low-stock alerts.

## Usage

```bash
python3 -c "from inventory import *; i=add_product([], 'A1', 'Keyboard', 5, 2); print(low_stock(i))"
python3 -c "from inventory import *; i=add_product([], 'A1', 'Keyboard', 1, 5); print(reorder_report(i))"
```

## Features

- Products with unique SKUs and reorder levels
- Stock adjustments that cannot go negative
- Reorder reports with reorder_report(inventory)
- CSV export with export_csv(inventory, path)

## Tests

```bash
python3 -m unittest -q
```

## License

MIT
