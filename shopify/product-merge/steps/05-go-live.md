# Step 5: Go live – handles, status, redirects

Takes about 2 minutes. Do the steps directly after each other.

## Before
- New product: all checks from steps 2–4 done, Preview looks right.
- Decide the final URL. We keep the old main product's URL (it has the Google ranking),
  e.g. `iq-multifunktionsjacke-3-0-unisex`.

## Do
1. **Old main product** (e.g. Schwarz) → Search engine listing → handle → add `-alt`
   (e.g. `iq-multifunktionsjacke-3-0-unisex-alt`) → **untick "Create URL redirect"** → Save.
2. **New product** → handle = the freed URL (e.g. `iq-multifunktionsjacke-3-0-unisex`) → Save.
   "Create URL redirect" may stay ticked (temporary handle → final handle).
3. **New product** → Status **Active**.
4. **Old products** → Status **Draft** (all of them).
5. **Online Store → Navigation → URL Redirects** → create, each pointing to the new URL:
   - `/products/<old-main>-alt`
   - `/products/<old-olive-handle>`
   - `/products/<old-blau-handle>`
   Test the `/en/` versions; add them only if they show 404.

## Errors we saw
- **"Handle already in use"**: the old product still has it. Do step 1 first.
- **"Target can't redirect to another redirect"**: a redirect already exists *from* the
  target URL. Delete it in URL Redirects first (no chains A → B → C).

## Rollback
New product → Draft; old products → Active; swap the handles back. Odoo keeps
syncing both, as long as the old links in Odoo are not removed yet.
