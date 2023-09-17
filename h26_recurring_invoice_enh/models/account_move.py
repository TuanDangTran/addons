# -*- coding: utf-8 -*-
from odoo import models, api, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    def button_cancel(self):
        if self._context.get('multiple_draft_invoices', None):
            return True
        return super(AccountMove, self).button_cancel()

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        if self._context.get('multiple_draft_invoices') and self.state == 'draft':
            for rec in self:
                rec.name = '/'
        else:
            super()._compute_name()

    def _post(self, soft=True):
        mapped_invoice_subscription_data = self._handel_mapped_invoice_subscriptions_data()
        res =  super()._post(soft)
        for invoice_line in mapped_invoice_subscription_data:
            invoice_line[0].subscription_id = invoice_line[1]
        return res

    def _handel_mapped_invoice_subscriptions_data(self):
        mapped_invoice_subscription_data = list()
        for rec in self.invoice_line_ids.filtered(lambda x: x.subscription_id):
            mapped_invoice_subscription_data.append([rec, rec.subscription_id])
            rec.subscription_id = False
        return mapped_invoice_subscription_data
