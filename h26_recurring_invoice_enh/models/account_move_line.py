# -*- coding: utf-8 -*-
from odoo import _, api, fields, models, tools
from dateutil.relativedelta import relativedelta


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.model
    def create(self, value):
        res = super().create(value)
        res.update_subscription_next_invoice()
        return res

    def update_subscription_next_invoice(self):
        order_id = self.sale_line_ids.order_id
        if order_id.is_subscription:
            order_id.next_invoice_date = self.subscription_end_date + relativedelta(days=1)