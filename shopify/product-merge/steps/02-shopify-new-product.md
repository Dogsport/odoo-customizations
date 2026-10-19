# Step 2: Build and import the new Shopify product (Draft)

**Why a new product instead of editing an old one:** the old products stay
untouched and live until the switch, so nothing breaks while we build.

## 1. Export the old products
Shopify → Products → tick the old colour products → **Export** → *Selected products* →
*CSV for Excel*.

## 2. Build the import CSV
One product, all variants. From the export:
- **Handle:** a temporary one, e.g. `iq-multifunktionsjacke-3-0-damen-neu`
- **Title:** without colour, e.g. `IQ Multifunktionsjacke 3.0 Damen`
- **Option1 Name = Farbe**, **Option2 Name = Größe**
- Colour values exactly as in the theme swatch list: `Schwarz`, `Graublau`, `Olive`
- Copy per variant: **SKU, barcode, price, compare-at price, cost, weight** (unchanged)
- **Variant Inventory Qty: empty** (Odoo sends stock later)
- **Status: draft**
- Vendor `IQ Dogsport`, Type `Bekleidung`, tags from the old products
- Images: all images of the old products; each colour's first image as its variant image
- Remove product-level values that belong to one colour (e.g. `Color` metafield, review count)

Example: [../merges/mfj-3-0-damen/MFJ3-Damen-new-product-import.csv](../merges/mfj-3-0-damen/MFJ3-Damen-new-product-import.csv)

## 3. Import
Products → **Import** → upload → **don't** tick "Overwrite products with matching handles" →
preview must show 1 product with all variants → **Import products**.

## 4. Check and complete the product
- Status **Draft**, all variants, price, images
- **Category** (often empty after import): e.g. *Sport Jackets*
- **Vendor** `IQ Dogsport` (not "IQ Dogsport GmbH")
- **Description:** no fixed review numbers ("aus 102 Bewertungen" → "Alle Bewertungen lesen")
- **Publishing:** tick all sales channels (Online Store etc.). Status stays Draft.
  Needed so Judge.me can see the product.
- **Variant Galerie** metafield per variant: that colour's images, front view first
