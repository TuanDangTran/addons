from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_invoice_subscription(self):
        return super(SaleOrder, self.with_context(multiple_draft_invoices=True)).action_invoice_subscription()

    def _create_invoices(self, grouped=False, final=False, date=None):
        move_id_and_type = []
        if self._context.get('multiple_draft_invoices', None):
            for order in self:
                if order.is_subscription:
                    move_ids = order.order_line.invoice_lines.move_id
                    for move_id in move_ids:
                        move_id_and_type.append([move_id, move_id.move_type])
                        move_id.move_type = 'entry'
        res =  super()._create_invoices(grouped, final, date)
        for move_id in move_id_and_type:
            move_id[0].move_type = move_id[1]
        return res

    def _get_invoiceable_lines(self, final=False):
        if self._context.get('multiple_draft_invoices', None):
            self = self.with_context({'recurring_automatic': False})
        return super()._get_invoiceable_lines(final)

    def _handle_automatic_invoices(self, auto_commit, invoices):
        if self._context.get('multiple_draft_invoices', None):
            return invoices
        return super()._handle_automatic_invoices(auto_commit, invoices)

    def _cron_recurring_create_invoice(self):
        return super(SaleOrder, self.with_context(multiple_draft_invoices=True))._cron_recurring_create_invoice()
