from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_invoice_subscription(self):
        return super(SaleOrder, self.with_context(multiple_draft_invoices=True)).action_invoice_subscription()

    def _create_recurring_invoice(self, automatic=False, batch_size=30):
        if self._context.get('multiple_draft_invoices', None):
            automatic = True
        invoices = super()._create_recurring_invoice(automatic, batch_size)
        return invoices

    def _get_invoiceable_lines(self, final=False):
        return super(SaleOrder, self.with_context(recurring_automatic=False))._get_invoiceable_lines(final)

    def _handle_automatic_invoices(self, auto_commit, invoices):
        if self._context.get('multiple_draft_invoices', None):
            return invoices
        return super()._handle_automatic_invoices(auto_commit, invoices)

    def _cron_recurring_create_invoice(self):
        return super(SaleOrder, self.with_context(multiple_draft_invoices=True))._cron_recurring_create_invoice()
