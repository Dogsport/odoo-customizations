# Scheduled action 'Send Shopify POS Invoice (Cash)' – every 2 minutes (existing, NOT changed) – reference only
# Sends paid CASH invoices of Shopify POS orders (no delivery, direct stock move) to customers with an email.

# =========================================================
# Send Shopify POS invoices by email - CASH payments only.
# Runs as a Scheduled Action every 5 minutes.
#
# Flow: find posted + fully PAID + unsent POS cash invoices,
# delete any stale pre-generated PDF, regenerate fresh
# (always shows PAID / 0.00 due), email it, mark as sent.
# =========================================================
template = env.ref(
    'account.email_template_edi_invoice',
    raise_if_not_found=False,
)
pdf_report = env.ref(
    'account.account_invoices',
    raise_if_not_found=False,
)
if not template or not pdf_report:
    log(
        'POS invoice cron aborted: missing email template or PDF report.',
        level='error',
    )
else:
    # -----------------------------------------------------
    # 1. Candidate invoices: posted, FULLY PAID, not yet
    #    sent by this automation, final number, after cutoff
    # -----------------------------------------------------
    invoices = env['account.move'].search([
        ('move_type', '=', 'out_invoice'),
        ('state', '=', 'posted'),
        ('payment_state', '=', 'paid'),
        ('x_studio_shopify_pos_invoice_sent', '=', False),
        ('name', 'not in', [False, '/']),
        ('create_date', '>=', '2026-07-13 09:15:59'),
    ])
    for invoice in invoices:
        # -------------------------------------------------
        # 2. Only invoices paid via a CASH journal
        # -------------------------------------------------
        pay_journal_types = invoice.matched_payment_ids.mapped('journal_id.type')
        if 'cash' not in pay_journal_types:
            continue
        # -------------------------------------------------
        # 3. Related sales orders
        # -------------------------------------------------
        sale_lines = invoice.invoice_line_ids.sale_line_ids
        sale_orders = sale_lines.order_id
        if not sale_orders:
            log('Invoice %s skipped: no related sales order.' % invoice.name, level='info')
            continue
        # -------------------------------------------------
        # 4. Skip orders that have a Delivery Order
        # -------------------------------------------------
        if sale_orders.picking_ids:
            log('Invoice %s skipped: has a delivery order.' % invoice.name, level='info')
            continue
        # -------------------------------------------------
        # 5. Require direct stock move (POS signature)
        # -------------------------------------------------
        direct_stock_move = env['stock.move'].search([
            ('sale_line_id', 'in', sale_lines.ids),
            ('picking_id', '=', False),
        ], limit=1)
        if not direct_stock_move:
            log('Invoice %s skipped: no direct stock move.' % invoice.name, level='info')
            continue
        # -------------------------------------------------
        # 6. Not already sent elsewhere
        # -------------------------------------------------
        if invoice.is_move_sent:
            log('Invoice %s skipped: already marked as sent.' % invoice.name, level='warning')
            continue
        # -------------------------------------------------
        # 7. Customer must have an email
        # -------------------------------------------------
        if not invoice.partner_id.email:
            log(
                'Invoice %s skipped: customer %s has no email.'
                % (invoice.name, invoice.partner_id.display_name),
                level='warning',
            )
            continue
        # -------------------------------------------------
        # 7b. Delete any pre-generated PDF (created during
        #     the Shopify import, before the payment was
        #     reconciled), so step 8 renders a FRESH one
        #     that shows PAID / 0.00 due
        # -------------------------------------------------
        if invoice.invoice_pdf_report_id:
            log(
                'Invoice %s: deleting stale pre-generated PDF.'
                % invoice.name,
                level='info',
            )
            invoice.invoice_pdf_report_id.sudo().unlink()
            invoice.invalidate_recordset(['invoice_pdf_report_id'])
        log(
            'Sending POS cash invoice %s: payment_state=%s, residual=%s.'
            % (invoice.name, invoice.payment_state, invoice.amount_residual),
            level='info',
        )
        # -------------------------------------------------
        # 8. Send; one failing invoice is logged and
        #    skipped, the loop continues
        # -------------------------------------------------
        try:
            env['account.move.send'].sudo()._generate_and_send_invoices(
                invoice.sudo(),
                sending_methods={'email'},
                mail_template=template.sudo(),
                mail_partner_ids=invoice.partner_id.ids,
                pdf_report=pdf_report.sudo(),
                allow_raising=True,
            )
            invoice.invalidate_recordset([
                'is_move_sent',
                'invoice_pdf_report_id',
            ])
            # ---------------------------------------------
            # 9. Verify PDF, then mark as completed
            # ---------------------------------------------
            if invoice.invoice_pdf_report_id:
                invoice.sudo().write({
                    'x_studio_shopify_pos_invoice_sent': True,
                })
                log('Shopify POS cash invoice %s sent successfully.' % invoice.name, level='info')
            else:
                log(
                    'Invoice %s: email sent but PDF was not generated - NOT marked as sent, will retry.'
                    % invoice.name,
                    level='error',
                )
        except Exception as e:
            log('Invoice %s FAILED to send: %s' % (invoice.name, e), level='error')
            continue