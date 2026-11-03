# ORIGINAL code of the Cybrosys module (NOT changed) – reference only
# Module: automatic_invoice_and_post 19.0.1.0.0 (Cybrosys, AGPL-3), file models/stock_picking.py
# Lines 83-84 send ALL invoices of the order on EVERY validated transfer (also returns/exchanges).

from odoo import models
import base64
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        """Validate delivery and optionally create, post, and email the invoice."""

        res = super().button_validate()

        auto_validate_invoice = self.env['ir.config_parameter'].sudo().get_param(
            'automatic_invoice_and_post.is_create_invoice_delivery_validate')
        auto_send_invoice = self.env['ir.config_parameter'].sudo().get_param(
            'automatic_invoice_and_post.is_auto_send_invoice')

        if auto_validate_invoice or auto_send_invoice:
            if any(rec.product_id.invoice_policy == 'delivery' for rec in
                   self.move_ids) or not self.sale_id.invoice_ids:

                invoice_created = self.sale_id._create_invoices(
                    self.sale_id) if self.sale_id else False

                # if invoice_created or self.sale_id.invoice_ids:
                #     invoice_created.action_post()

            if auto_send_invoice and self.sale_id.invoice_ids.partner_id.mapped('email'):
                self._send_invoice_email(self.sale_id.invoice_ids)

        return res

    def _send_invoice_email(self, invoice):
        """Send invoice with PDF attachment via message_post"""
        report = self.env.ref('account.account_invoices')

        for move in invoice:
            try:
                # Use credit-note template for refunds and invoice template otherwise.
                template = move._get_mail_template()
                # Render the mail/PDF using the customer's language.
                mail_lang = template._render_lang(move.ids).get(move.id) or move.partner_id.lang or self.env.lang
                report_lang = report.with_context(lang=mail_lang)
                template_lang = template.with_context(lang=mail_lang)

                pdf_content, _ = report_lang._render_qweb_pdf(report.id, res_ids=move.ids)
                pdf_base64 = base64.b64encode(pdf_content)

                if move.name and move.name != '/':
                    file_name = move.name.replace('/', '_')
                else:
                    file_name = f"Draft_Invoice_{move.invoice_origin or move.id}"

                attachment = self.env['ir.attachment'].create({
                    'name': f"{file_name}.pdf",
                    'type': 'binary',
                    'datas': pdf_base64,
                    'res_model': 'account.move',
                    'res_id': move.id,
                    'mimetype': 'application/pdf',
                })

                body_html = template_lang._render_field('body_html', move.ids)[move.id]

                if move.state == 'draft':
                    subject = f"{move.company_id.name} Invoice (Draft) - Ref {move.invoice_origin or ''}"
                else:
                    subject = template_lang._render_field('subject', move.ids)[move.id]

                move.with_context(lang=mail_lang).message_post(
                    body=body_html,
                    subject=subject,
                    message_type='email',
                    partner_ids=[move.partner_id.id],
                    attachment_ids=[attachment.id],
                    subtype_xmlid='mail.mt_comment',
                )

                move.is_move_sent = True

            except Exception:
                _logger.exception("Failed to send invoice email for invoice id %s", move.id)
