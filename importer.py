#!/usr/bin/env python3
"""CSV-based StPierre&Co. product import prototype. No network access or scraping."""
import argparse, csv, sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

REQUIRED = ["temu_url", "title", "source_price_zar"]
OPTIONAL = ["description", "image_url", "variant", "source_shipping_zar", "sku"]

def money(value, field, row_num):
    try:
        result = Decimal((value or "0").strip())
        if result < 0:
            raise ValueError
        return result.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        raise ValueError(f"Row {row_num}: {field} must be a non-negative number.")

def main():
    p = argparse.ArgumentParser(description="Validate a CSV and add a fixed ZAR markup.")
    p.add_argument("input_csv")
    p.add_argument("--markup-zar", required=True, help="Fixed markup in ZAR, e.g. 100")
    p.add_argument("--output", default="imported-products.csv")
    args = p.parse_args()
    try:
        markup = Decimal(args.markup_zar)
        if markup < 0: raise ValueError
    except InvalidOperation:
        sys.exit("--markup-zar must be a number.")
    if markup < 0: sys.exit("--markup-zar cannot be negative.")
    source = Path(args.input_csv)
    if not source.exists(): sys.exit(f"Input file not found: {source}")
    with source.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        missing = [h for h in REQUIRED if h not in (reader.fieldnames or [])]
        if missing: sys.exit("Missing required columns: " + ", ".join(missing))
        rows = []
        for n, r in enumerate(reader, start=2):
            title = (r.get("title") or "").strip()
            url = (r.get("temu_url") or "").strip()
            if not title or not url:
                print(f"Skipping row {n}: title or URL is blank.", file=sys.stderr)
                continue
            cost = money(r.get("source_price_zar"), "source_price_zar", n)
            shipping = money(r.get("source_shipping_zar"), "source_shipping_zar", n)
            # Markup is added after source shipping; excludes payment fees, taxes, returns and FX risk.
            sell = (cost + shipping + markup).quantize(Decimal("0.01"))
            rows.append({
                "Handle": f"spc-{(r.get('sku') or str(n)).strip().lower()}",
                "Title": title,
                "Body (HTML)": (r.get("description") or "").strip(),
                "Vendor": "StPierre&Co.",
                "Type": "",
                "Tags": "Temu-import-review-required",
                "Published": "FALSE",
                "Option1 Name": "Title",
                "Option1 Value": "Default Title",
                "Variant SKU": (r.get("sku") or "").strip(),
                "Variant Price": f"{sell:.2f}",
                "Cost per item": f"{cost:.2f}",
                "Image Src": (r.get("image_url") or "").strip(),
                "Source URL (prototype)": url,
                "Source Shipping ZAR (prototype)": f"{shipping:.2f}",
                "Fixed Markup ZAR (prototype)": f"{markup:.2f}",
                "Review before publish": "Confirm rights, product data, stock, shipping, tax, and price",
            })
    if not rows:
        sys.exit("No valid product rows found.")
    with open(args.output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Prepared {len(rows)} draft rows: {args.output}")
    print("Nothing was published to Shopify and no Temu orders were placed.")

if __name__ == "__main__":
    main()
