# Production implementation plan

## Admin workflow
1. Install app in Shopify using OAuth.
2. Upload CSV of products the merchant is permitted to import.
3. Validate title, variants, images, source URL, price, shipping estimate and currency.
4. Convert source cost to ZAR using a configurable, timestamped exchange rate if needed.
5. Suggested price = source item cost + source shipping + fixed ZAR markup.
6. Preview and publish as **draft products** through Shopify Admin GraphQL API.
7. Monitor Shopify order webhooks and map order line items to source URLs.
8. Put orders in a fulfilment queue; only auto-submit when an authorized Temu API or approved fulfillment partner supports it.
9. Record supplier order IDs, shipment status and tracking, then update Shopify fulfillment through authorized APIs.

## Suggested technical stack
- Shopify app template (Remix/React Router, as supported by current Shopify CLI)
- Node.js + TypeScript backend
- Shopify Admin GraphQL API with least-privilege scopes
- PostgreSQL for product mapping and order status
- Shopify webhooks: orders/paid, orders/cancelled, app/uninstalled
- Secret storage for OAuth tokens; never expose tokens to browser code
- Idempotency keys, retry queue, audit logs, and human approval for supplier purchases

## Security and compliance gates
- Verify Temu Partner Platform eligibility, approved permissions, and region coverage.
- Do not scrape Temu or automate consumer checkout with browser bots unless Temu expressly permits it.
- Do not assume seller APIs grant access to retail product catalogue or retail purchasing.
- Confirm permission to reuse product images/descriptions and the applicable shipping, returns, tax and consumer-law obligations.
- Require merchant approval before publishing products or placing any supplier order.
- Keep auto-fulfilment disabled until a supported supplier order API is tested end-to-end.
