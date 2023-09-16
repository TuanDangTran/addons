# -*- coding: utf-8 -*-

from odoo import models
from dateutil.relativedelta import relativedelta


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        res = super()._prepare_invoice_line(**optional_values)
        if res.get('subscription_end_date') and self.order_id.is_subscription:
            self.order_id.next_invoice_date = res.get('subscription_end_date') + relativedelta(days=1)
        return res

