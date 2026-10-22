# IQ Dogsport — Complete Shopify implementation and backup log

**Documentation as of 22 October 2026.** This is a reconstructed, structured technical record of the work described in the ChatGPT conversation, supplemented by the screenshots, CSS versions, pasted terminal output and Welcome-IQ documentation provided. It is **not a verbatim ChatGPT conversation export** and does not imply that every local backup is available here. The canonical code history is in Git.

## 1. Repository and theme reference

| Resource | Identifier / link | What it contains |
| --- | --- | --- |
| Shopify store | `iqdogsport` | Merchant store; live theme changed on 22 October |
| Currently published theme | `HAMZA – SEO Übergabe – Live-Kopie 22.10.2026` | Theme `203931648264`, confirmed MAIN/live |
| Previous theme | `IQ – live` | Unpublished theme `202725884168` as shown in theme list at the time |
| Theme source repository | [knabl-florian/IQ-Shopify](https://github.com/knabl-florian/IQ-Shopify) | Theme Git history; local working directory `IQ-Shopify-live-direct` |
| Theme working branch | `shopify-live-direct` | The local branch used to commit changes |
| Confirmed snapshot branch | [live-snapshot-2026-10-22](https://github.com/knabl-florian/IQ-Shopify/tree/live-snapshot-2026-10-22) | Successfully pushed as a **separate branch** |
| Filter/video snapshot commit | [`f6cc45e`](https://github.com/knabl-florian/IQ-Shopify/commit/f6cc45e) | 18 files, 562 insertions, 15 deletions |
| Documentation repository | [dogsport/odoo-customizations](https://github.com/dogsport/odoo-customizations) | GitHub Pages and implementation notes — **not** Shopify deployment |
| Welcome-IQ page | [Welcome-IQ discount](https://dogsport.github.io/odoo-customizations/shopify/welcome-iq-discount/) | Discount setup from 21 October |

### Boundaries of what was confirmed

- `shopify theme list` showed the HAMZA theme as `[live]`; subsequent Shopify Admin API lookup returned theme role `MAIN`. The most recent check was 22 Oct 2026.
- The **filter/video commit** `f6cc45e` was created successfully and pushed under `live-snapshot-2026-10-22`. A push to `origin/shopify-live-direct` was **rejected** due to remote commits; it was **not** forced.
- The updated IQ Insider homepage file `templates/index.json` was pulled from the published theme twice and copied into the main local Git project. At that moment, `git diff --stat` showed `1 file changed, 1 insertion(+), 1 deletion(-)` (a JSON string). **A later commit and push of that last change are not confirmed in the provided evidence.**
- Local `theme-compare/live`, `theme-compare/draft`, and `backup-patricia-filters-20261022` were referenced/created on the user's Mac. These are not automatically part of the GitHub branch snapshot.
- An earlier backup tarball (`../IQ-Shopify-before-sync.tar.gz`) was *recommended*, but its existence was **not demonstrated**.

## 2. Chronological work log

| Date / sequence | Work | Outcome / evidence |
| --- | --- | --- |
| 16 Oct onward | Collection page and filter work, mobile layout tests, local CSS versions | Terminal/CSS screenshots, pasted source versions |
| Before publication | Pull current live and HAMZA draft into `theme-compare/live` and `theme-compare/draft`; compare with `git diff --no-index` | Initial comparison described 17 changed files; local draft had new native filters/videos |
| 21 Oct | Replace order-wide Welcome-IQ coupon with product-only discount; create/update automated eligible collection; exclude two new coats | Incognito checkout test documented |
| 21 Oct | Update newsletter/welcome email discount copy | DE/EN offer disclaimer; old separate-section code archived |
| 22 Oct | Publish HAMZA SEO draft `203931648264` | Shopify CLI `[live]`, API `MAIN` |
| 22 Oct | Pull newly published HAMZA theme; synchronize local theme directories; stage Patricia filter/video and mobile CSS changes | `git diff --stat`: 13 tracked files, 320 insertions, 15 deletions, plus new files |
| 22 Oct | Create commit `f6cc45e` | 18 files, 562 insertions, 15 deletions |
| 22 Oct | Attempt `git push -u origin shopify-live-direct` | Rejected: non-fast-forward; remote branch ahead/diverged |
| 22 Oct | `git fetch origin` and compare histories | Remote includes variant gallery PR #4 and earlier Patricia snapshot PR #3 |
| 22 Oct | Create local backup branch and push independent live snapshot | Local `backup-patricia-filters-20261022`; remote `live-snapshot-2026-10-22` push succeeded |
| 22 Oct | Read live theme using Shopify Admin API, inspect homepage | IQ Insider is active Custom Liquid in `templates/index.json`, not `sections/iq-insider-anmeldung.liquid` |
| 22 Oct | Pull live theme twice, then copy `templates/index.json` into local root | Diff `2 +−` lines because entire Custom Liquid serialized as one JSON string |
| 22 Oct | `jq` failed to parse Shopify template file | Top-of-file generated comment means `jq` needs comment removal / `awk` or Python parser |

## 3. Native Shopify collection filters (Patricia + mobile work)

**Admin metafields/filter sources** (final activation state still requires verification):

| Visible filter | Source | Details |
| --- | --- | --- |
| IQ Produktgruppen | `custom.iq_product_groups` | Product metafield, list of text values; audit reported 111 active products assigned |
| IQ Buchsprache | `custom.iq_book_languages` | Single-line text `de` or `en`; reported 5 active book editions (3 DE / 2 EN) |
| Größe | Existing product option | No separate size metafield |
| Passform | Existing Shopify target-gender filter | Customer-facing DE/EN labels Damen/Unisex and Women/Unisex |
| Availability / price / colour | Existing filters | Retained, not replaced |

**Product groups and intended order**

| Collection | Group labels (German) |
| --- | --- |
| Bekleidung | Jacken · Mäntel · Westen · Hosen · Shirts & Hoodies · Accessoires |
| Jacken | Winter · Multifunktion · Training · Regen & Softshell · K9 |
| Westen | Hundesport · Sommer · K9 / Dienst |
| T-Shirts & Hoodies | Hoodies · Zip-Hoodies · Trainingsshirts · T-Shirts · Tanktops |
| Accessoires | Caps & Mützen · Taschen & Gürtel · Socken · Clicker · Pflege & Ersatzteile · Schlüsselanhänger |
| Training & Hund | Fußarbeit & Clicker · Apportieren · Fährte · Geschirre & Schutzdienst · Taschen & Gürtel · Hundeplatz & Verein |
| Spielzeug | Bälle · Beißrollen · Magnetsysteme |
| K9 | Jacken · Westen · Geschirre · Taschen & Belohnung · Zubehör & Patches |
| Futter | Trainingssnacks · Kausnacks · Hauptfutter |
| Bücher | Unterordnung · Schutzdienst · Begleithundprüfung |
| Gutscheine & More | Gutscheine · Banner · Schlüsselanhänger · Bälle · Caps & Socken · Aufkleber |
| Hosen / IQ Outlet | No additional product-group row planned |

**Rules and behavior:** A product can carry multiple relevant groups; Zip-in jackets map to **Training**. Keep source values with collection prefixes, e.g. `hundesport-westen--sommer`, and translate **labels**, not metafield values. Filter links are Shopify-native URLs with counts, selected states, keyboard access and Alle/All reset. The intended behavior is OR within a group and narrowing combination between separate filter sources. Existing collection links remain fallback until group sources become available. Hosen's Passform test reportedly gave Damen→Leggings, Unisex→Trainer Pants, both→both.

**Main changed files:**

```text
assets/facets.js
assets/iq-collection-system.css
snippets/iq-collection-group-filters.liquid
snippets/iq-filter-group-order.liquid
snippets/iq-filter-label.liquid
snippets/facets.liquid
snippets/facets-active.liquid
sections/iq-collection-links.liquid
sections/main-collection-product-grid-magazine.liquid
sections/iq-responsive-collection-video.liquid
locales/de.json
locales/en.default.json
templates/collection.json
templates/collection.jacken.json
templates/collection.trainer-pants-patricia.json
templates/collection.westen.json
```

The Liquid lookup used the Search & Discovery/native filter source:

```liquid
{%- assign group_filter = collection.filters | where: 'param_name', 'filter.p.m.custom.iq_product_groups' | first -%}
```

### Mobile styling fix

Goal: one horizontal, swipeable row at narrow widths **without** breaking native link behavior, counts, selection, keyboard focus, reset, translation, pagination or desktop filtering. The selected implementation worked within shared `.iq-group-filters` CSS, not separate per-collection code.

- `flex-wrap: nowrap`, `overflow-x: auto`, `overflow-y: hidden`, and `-webkit-overflow-scrolling: touch` for mobile.
- `flex: 0 0 auto` and `white-space: nowrap` for `.iq-group-filters__option`.
- Constrain the parent/grid (`min-width:0`/`max-width:100%`) after an early Chrome emulation showed the filter container about **1069px wide at a 375px viewport**; this would otherwise prevent internal swiping.
- Top spacing at `#IQCollectionGroupFilters`: **24px desktop**, **16px mobile**.
- The supplied evidence records source edits and committed CSS; **a complete post-publication device test was not documented**.

The original source/CSS versions and screenshots are in the **offline evidence archive**, not linked publicly from this page.

## 4. Responsive video and product-gallery distinction

The HAMZA commit introduced `sections/iq-responsive-collection-video.liquid` and modified collection layouts to support responsive collection videos. This is separate from the **variant-gallery colour-filter** work already committed on the shared remote branch.

Remote history observed in Git:

```text
< f6cc45e (local snapshot) feat: Patricia collection filters and video sections
< 2a49247 Backup of current live Shopify theme
> c211604 (origin/shopify-live-direct) Merge pull request #4 from knabl-florian/feature/variant-galerie-colour-filter
> c46e86a new variant base gallery
> 071377c Product gallery: show only media of selected colour (Variant Galerie metafield)
> 232fb62 Create README.md
> 29e32c3 Merge pull request #3 from knabl-florian/shopify-patricia-direct
> 7cec49c Snapshot of Patricia Shopify theme – 2026-10-14
```

As of the comparison shown in chat, these branches differed substantially (`assets/media-gallery.js`, product section, `config/settings_data.json`, `layout/theme.liquid`, filters and locales, and many other files). **Do not treat a merge/rebase as a no-op**, and never force-push away the gallery commits without explicit review.

## 5. Welcome-IQ discount configuration (21 Oct)

### Before / after

| Aspect | Before | After |
| --- | --- | --- |
| Coupon | `Welcome-IQ` amount off order | New `Welcome-IQ`, amount off products |
| Discount | 10% of all items | 10% only for products in automated `Welcome-Rabatt` collection |
| Historical code | Order-wide coupon | Renamed `Welcome-IQ-ALT` and deactivated, 262 recorded uses through 21 Oct |
| Limits | One use/customer | One use/customer; no global end date documented |
| New arrivals | Automatically discounted | **Must add `no-discount` tag to exclude**; the generic 60-day `new` tag is not a discount exclusion |

Automated collection: product vendor `IQ Dogsport` **OR** `IQ Dogsport GmbH` and product tag **does not include** `no-discount` (match the intended ALL/ANY group logic when reviewing the actual Shopify configuration). Collection hidden from sales channels; the 21 Oct audit reported **151 → 149** products after two winter coats were excluded.

Excluded products: **IQ Winterparka Unisex** and **IQ Zip-off-Wintermantel Damen**. Exclude more products by adding `no-discount` to their Shopify product tags.

Incognito checkout verification recorded:

| Item | Observed test result |
| --- | --- |
| Nikwax Tech Wash | €11.90, no discount |
| IQ Summer Vest 3.0 | €129.90 → €116.91 (10% discount, €12.99) |
| IQ Zip-off-Wintermantel Damen | €349.00, no discount |

The newsletter Flow **10% Rabatt für Newsletter-Anmeldung** had its message updated to explain that the code is only for IQ products, excluding new products. The code appears as plain text `WELCOME-IQ` in the flow email.

**Rollback**: deactivate/rename new product-only coupon and reactivate the historical order-wide coupon only if business approves; ensure all homepage and email copy matches the intended discount policy.

## 6. Active IQ Insider: homepage Custom Liquid (22 Oct)

The previous standalone `iq-insider-anmeldung.liquid` documented on 21 Oct was **not** the active section in the new published HAMZA theme. Shopify Admin API confirmed:

```text
Published theme  : HAMZA – SEO Übergabe – Live-Kopie 22.10.2026
Theme ID         : 203931648264
Theme role       : MAIN
Theme file       : templates/index.json
Section key      : custom_liquid_EtqqpY
Section type     : custom-liquid
Section name     : Newsletter
```

The active Custom Liquid contains:

```liquid
<p class="iq-insider__note">{% if iq_en %}On your first order. Valid on IQ products, excluding new arrivals.{% else %}Auf Deine erste Bestellung. Gültig für IQ Produkte, ausgenommen Neuheiten.{% endif %}</p>
```

and:

```css
.iq-insider .iq-insider__note { margin:-12px 0 20px; font-size:14px; line-height:1.5; color:#52524F; }
```

The active Custom Liquid **does not** contain `text_36` / `text_37` fields. Those fields belong to the **historical standalone Liquid section** (kept as evidence). To edit the live text: theme editor → homepage → **Newsletter** → Custom Liquid; or edit `templates/index.json` carefully in version control.

In the homepage template, another older `custom_liquid_nmLPH3` ("Newsletter Banner") and a native `newsletter_P7pLqr` section were disabled at the time checked. Re-check their copy before re-enabling.

### Exact-code extraction on Mac

Shopify `templates/index.json` starts with an auto-generated comment, so plain `jq` fails with `Invalid numeric literal at line 2, column 0`. A robust local extractor:

```bash
python3 - "theme-compare/live/templates/index.json" <<'PY'
import json, pathlib, re, sys
raw = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8-sig')
raw = re.sub(r'^\s*/\*.*?\*/\s*', '', raw, count=1, flags=re.S)
data = json.loads(raw)
code = data['sections']['custom_liquid_EtqqpY']['settings']['custom_liquid']
print(code)
PY
```

The latest `templates/index.json` file was pulled from live using `shopify theme pull --theme 203931648264 --store iqdogsport --path ./theme-compare/live` and then copied to the theme Git working tree. The diff summary `2 +−` represents the entire serialized Custom Liquid string as one JSON line, **not only one character changed**. An updated commit/push after this copy is **not confirmed** here.

## 7. Backups — definitive inventory

| Name / location | Operation | Confirmed? | Restore / notes |
| --- | --- | --- | --- |
| `live-snapshot-2026-10-22` | `git push origin HEAD:refs/heads/live-snapshot-2026-10-22` | **YES**, GitHub reported `[new branch]` | Remote snapshot of commit `f6cc45e` |
| `f6cc45e` | `git commit` | **YES** | `git show f6cc45e`, `git show --stat f6cc45e` |
| `backup-patricia-filters-20261022` | `git branch backup-patricia-filters-20261022` | **YES**, command returned successfully | Local lightweight branch; not proven pushed remotely |
| `2a49247` | `git log --oneline` | **YES**, earlier commit was shown | Earlier "Backup of current live Shopify theme" |
| `theme-compare/live/` | Shopify CLI pull | **YES**, multiple successful pulls | Local folder; ignored by Git due to `.gitignore` |
| `theme-compare/draft/` | Shopify CLI pull | **YES**, earlier session evidence | Local folder; ignored by Git |
| `templates/index.json` after IQ Insider pull | `cp theme-compare/live/templates/index.json templates/index.json` | **YES**, local diff shown | Last commit/push unverified |
| `../IQ-Shopify-before-sync.tar.gz` | Suggested tar backup | **UNKNOWN** | Verify, don't assume exists |
| `backup-hamza-live-2026-10-22` | Suggested local branch | **UNKNOWN** | Verify with `git branch --list` |
| `origin/shopify-live-direct` after snapshot | Initial push rejected | **NOT UPDATED BY THAT PUSH** | Remote contains independent gallery commits |
| `live-snapshot-2026-10-22` with latest IQ Insider commit | Suggested follow-on push | **NOT VERIFIED** | Check `git log` and `git ls-remote` |

### Commands to audit and export actual backups

From **IQ-Shopify-live-direct**:

```bash
git status --short
git branch -avv
git log --all --decorate --oneline --graph -35
git ls-remote --heads origin live-snapshot-2026-10-22
git show --stat f6cc45e
git show f6cc45e > hamza-seo-theme-changes.patch
ls -ld theme-compare/live theme-compare/draft 2>/dev/null
ls -l ../IQ-Shopify-before-sync.tar.gz 2>/dev/null
```

For an **offline complete Git backup** (history + all refs), run the included `collect_local_backups.sh` with a private output path. It creates a Git bundle, theme working-file archives, live/draft local comparisons when present, exact Liquid export, diff snapshots and SHA-256 checksums. **It does not modify Shopify or force-push anything.**

> Security: do not upload full theme ZIPs, `config/settings_data.json`, private terminal logs or Shopify credentials to a public GitHub Pages documentation site. Save theme backups privately. This public work log links to the GitHub branch but publishes only non-sensitive descriptions and code excerpts.

## 8. Troubleshooting from the conversation

| Issue | Cause / response |
| --- | --- |
| `git push ... (non-fast-forward)` | GitHub `shopify-live-direct` contains other commits; independent snapshot branch was pushed instead of force-pushing |
| `jq: parse error: Invalid numeric literal at line 2, column 0` | Shopify theme JSON may start with a generated comment; strip it before `jq` or use Python parser above |
| `code: command not found` on Mac | VS Code Shell Command: Install 'code' command in PATH was not configured |
| `permission denied` trying to run screenshot path | Image files aren't executable commands; open in Finder or VS Code |
| Filter row 1069px wide on 375px viewport | Parent min-content width prevented nested scrolling; constrain container/grid width |
| Shopify theme vs documentation repo confusion | `knabl-florian/IQ-Shopify` stores theme source; `dogsport/odoo-customizations` is GitHub Pages documentation |
| `git diff` shows deletions of new snippets | Diff direction `HEAD origin/shopify-live-direct` reports **relative Git content**, not Shopify storefront deletions |
| Shopify code all on one JSON line | `settings.custom_liquid` is serialized as one string; extract before `diff -u` |
| Search & Discovery scope | Metafields are configured shop-wide; collection-specific presentation is in theme snippets |

## 9. Pending verification and safe next steps

- Verify final enabled state of product-group and book-language filters in Search & Discovery.
- Test group selection, OR behavior, combined size/gender/colour, reset/Alle, DE/EN, URLs, AJAX, pagination, keyboard focus.
- Test mobile swiping at 320/375/390px; confirm no outer page horizontal scroll and check desktop layout.
- Compare CLS and loading performance before/after; no confirmed measurements were provided.
- Verify tag `no-discount` for new products, two vendor spellings, and Flow email copy.
- After IQ Insider update: stage and commit `templates/index.json` separately, push snapshot only if remote branch has not moved. No force push.
- Resolve remote `shopify-live-direct` branch divergence deliberately; review gallery code before merge/rebase.

## 10. Recovery playbook

**Inspect a known Git snapshot without touching Shopify:**

```bash
git fetch origin
git show f6cc45e:snippets/iq-collection-group-filters.liquid
git show f6cc45e:assets/iq-collection-system.css
git show f6cc45e:sections/iq-responsive-collection-video.liquid
```

For a separate recovery working tree, create a new Git worktree or checkout branch; **do not** overwrite the active storefront directly. Historical code should be tested in an unpublished theme before publication.

To restore IQ Insider, use a correctly dated local `templates/index.json` or extract its Custom Liquid. The standalone 21 Oct `iq-insider-anmeldung.liquid` is an **old different implementation**, not a drop-in replacement for the homepage Custom Liquid.

## 11. Evidence index and limitations

The **offline evidence package**, not intended for automatic public GitHub upload, contains available session screenshots, CSS variants, pasted terminal logs, original 21 Oct Welcome-IQ Markdown and archival standalone section code. The **real** local `theme-compare` folders, exact new homepage template and Git history reside on the user's Mac/GitHub and must be collected by the backup script.

An exact verbatim chat transcript requires a separate ChatGPT conversation/data export. This page is a reconstructed technical activity log based on available messages and attachments, not every conversational line.

**History status:** confirmed = observed CLI/API output; reported = user audit or documentation; pending = no corresponding confirmation was shown.


## 12. Related Odoo–Shopify variant and inventory mapping case

A separate issue discussed earlier in the same Shopify/Odoo working conversation involved the **IQ Mini Dumbbell Keychain**: Shopify variants had been associated with zero-stock duplicate Odoo products, while the original Odoo product carried stock. This case is **not** fixed by the theme snapshot and must be resolved in Emipro/Odoo product-to-variant mappings rather than CSS or Liquid.

| Item | Recorded identifier / observation |
| --- | --- |
| Shopify product | `12141783613704` |
| Original Odoo Mini-Apportierholz variant | `IQD-APH-LIGHT`: 8 on hand, 7 reserved, 1 forecast at the time |
| Original Odoo Hetzarm variant | `IQD-APH-HETZ`: 0 stock |
| Shopify Hetzarm variant | `59119335440648`; inventory item `61466959053064` |
| Shopify Mini variant | `59119335473416`; inventory item `61466959085832` |
| Obsolete Mini mapping | Shopify variant `58333728243976`; inventory item `60669710696712` |
| Reported export error | `INVALID_INVENTORY_ITEM` against obsolete mapping |

**Reported cause:** The Emipro connector created/link-mapped two extra standalone Odoo products with 0 stock instead of mapping the existing Odoo product variants to the current Shopify variants. **Status:** no confirmed completed mapping fix in the supplied messages. Do not treat this as part of the 18-file theme commit; handle it in the integration/ERP workflow separately.
