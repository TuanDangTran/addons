# -*- coding: utf-8 -*-

from odoo import fields, models, api, _, Command


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = super()._prepare_invoice_line(**optional_values)
        if res.get('subscription_start_date'):
            self.order_id.next_invoice_date = res.get('subscription_start_date')
        return res

