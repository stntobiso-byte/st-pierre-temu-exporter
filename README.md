# StPierre&Co. Temu Importer — prototype

This is a starter prototype, not a published Shopify app. It demonstrates bulk CSV import, fixed ZAR markup calculations, product validation, and a fulfilment queue export. It does not scrape Temu, bypass access controls, or place Temu orders.

## Files
- `products-template.csv`: sample import format
- `importer.py`: validates CSV rows and computes suggested prices
- `shopify-app-plan.md`: production Shopify integration plan

## Run
Requires Python 3.10+.
```bash
python importer.py products-template.csv --markup-zar 100 --output imported-products.csv
```
The output is a Shopify-ready *draft import file*, not a direct connection to your store. Review product rights, images, stock, delivery, tax, and final price before publishing.

## Important limits
- Temu retail checkout is not assumed to have a supported public dropshipping API.
- Do not store Shopify access tokens in this prototype or upload secrets into a spreadsheet.
- A production app needs a Shopify Partner app, OAuth, approved scopes, a secure backend, webhooks, privacy policy, and a verified product/order data source.
- Automatic Temu ordering must stay off unless Temu explicitly authorizes that workflow for your account/region.
