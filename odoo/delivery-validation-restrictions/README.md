# Deliveries: only authorised users release Waiting deliveries (21.10.2026)

**Status 21.10.2026: Studio changes live and tested · Automation rule live, Barcode test open.**
Odoo 19 Production (iq-dogsport.odoo.com) · Inventory → Delivery Orders (`stock.picking`, outgoing).

## 1. Why

- Deliveries were moved from **Waiting → Ready** and then validated by the shared user **Office** (e.g. WH1/OUT/06785 on 21.10.2026: Waiting → Ready at 10:38, label created at 10:56).
- A Waiting delivery should only be released by people who know the order is really ready to ship. Customs (**Zoll**) deliveries need their papers before they leave.
- Hiding buttons is not enough: the **Barcode app** has its own Validate and does not use the form buttons. So there is also a server-side rule.

## 2. Overview

| # | What | Where | Effect |
|---|---|---|---|
| 1 | New group **Check Availability erlaubt** | Settings → Users & Companies → Groups | The users allowed to release Waiting deliveries |
| 2 | **Check Availability** button only for the group | Studio → Delivery form | Office doesn't see it |
| 3 | Grey **Validate** button (Waiting) only for the group | Studio → Delivery form | Office can't validate a Waiting delivery in the form |
| 4 | Automation rule **Waiting-Lieferung: nur berechtigte Benutzer** | Settings → Technical → Automation Rules | Blocks Waiting → Done for everyone outside the group, in every app (form, Barcode, list) |

Unchanged: the highlighted **Validate** on **Ready** deliveries is visible for everyone, so Office can still ship deliveries that are Ready.

## 3. Group "Check Availability erlaubt"

| Setting | Value |
|---|---|
| Name | Check Availability erlaubt |
| Record ID | 150 |
| External ID | `studio_customization.group_check_availability_erlaubt` |
| Users (5) | Anastasiia Derkach, Christina Helm, Dr. Florian Knabl, Elena Kistritz, Hamza Mohsin |

**Why the External ID:** Studio only accepts groups with an External ID. Without it, Studio shows *"Only groups with an external ID can be used here"*. A group created in the UI has none, so one was added manually:
Settings → Technical → Sequences & Identifiers → External Identifiers → New → Module `studio_customization`, Name `group_check_availability_erlaubt`, Model `res.groups`, Record ID `150`.

**Add or remove a user:** open the group → tab *Users*. No Studio change needed.

## 4. Studio: buttons on the delivery form

Changed on the form view of **Transfers** (`stock.picking`) with Studio, on a Waiting delivery.

| Button | Method | Before | After | Invisible condition |
|---|---|---|---|---|
| **Check Availability** | `action_assign` | Allow visibility to groups: *Role / User* (everyone) | **Check Availability erlaubt** | unchanged: `not show_check_availability` |
| **Validate** (grey, class `o_btn_validate`, shown in Waiting) | `button_validate` | everyone | **Check Availability erlaubt** | unchanged (conditional) |
| **Validate** (highlighted, shown in Ready) | `button_validate` | everyone | unchanged | unchanged |

Why groups and not a condition: Studio's *Invisible* condition only knows the record, not the user's groups. `uid in [ids]` would work but hard-codes user IDs. The **Responsible** field is the assigned user, not the current user, so it can't be used either.

### Result (tested 21.10.2026)

| User | Waiting delivery | Ready delivery |
|---|---|---|
| Office | no Check Availability, no Validate | Validate ✅ |
| 5 users in the group | Check Availability + Validate | Validate ✅ |

## 5. Automation rule: no Waiting → Done outside the group

The Barcode app validates without the form buttons, so the rule checks **who** changes the status, not which screen is used.

| Setting | Value |
|---|---|
| Name | Waiting-Lieferung: nur berechtigte Benutzer |
| Model | Transfer |
| Trigger | On create and edit |
| When updating | Status |
| Before Update Domain | Status = **Waiting** |
| Apply on | Status = **Done** |
| Action | Execute Code |

The two domains make the rule fire **only** when a delivery goes directly from Waiting to Done. Validating a Ready delivery is not affected. Receipts and internal transfers are skipped by the code (`outgoing` only).

```python
if not env.user.has_group('studio_customization.group_check_availability_erlaubt'):
    for rec in records:
        if rec.picking_type_id.code == 'outgoing':
            raise UserError('LIEFERUNG %s ist noch nicht freigegeben (Status Waiting). Bitte warten, bis sie Ready ist, oder an Florian, Anastasiia, Elena, Christina oder Hamza weitergeben. / This delivery is not released yet.' % rec.name)
```

`UserError` stops the save, so the delivery stays as it was and no label is created.

### Test still open: Barcode app

As **Office** in the Barcode app: open a Waiting delivery, scan, Validate.

- Error message → done.
- Goes through → the Barcode app moved it to Ready first. Then change *Apply on* to Status **in Ready, Done**. Risk: if Office validates a **receipt**, Odoo may reserve waiting deliveries as Office and the rule would block the receipt. Test a receipt as Office afterwards.

If pick/pack steps are used later, add **Waiting Another Operation** to the Before Update Domain.

## 6. Related rules

| Rule | Blocks |
|---|---|
| Block delivery if not paid (existing) | Unpaid Shopify orders, except whitelisted B2B customers and the allowed users |
| Waiting-Lieferung: nur berechtigte Benutzer (new) | Waiting → Done outside the group |

### Planned: Zoll deliveries (not created yet)

- Field **Versandhinweise**: `x_studio_many2many_field_8oe_1jp7bngnk` (tags, `crm.tag`). Only visible while the delivery is Waiting (`invisible: state != "confirmed"`).
- Field **Paperwork Done**: `x_studio_paperwork_done` – read-only in the form, so not usable as a manual tick without a view change.
- Idea: keep the tag **Zoll**, add a second tag **Zollpapiere OK** when the papers are ready. A rule blocks Validate for Zoll deliveries without *Zollpapiere OK*. No new field needed.

## 7. Rollback

1. **Buttons:** Studio → click the button → *Allow visibility to groups* → remove *Check Availability erlaubt*, add *Role / User* back.
2. **Automation rule:** archive it (Settings → Technical → Automation Rules).
3. **Group:** can stay. Delete it only after both steps above, otherwise the buttons are hidden for everyone.
