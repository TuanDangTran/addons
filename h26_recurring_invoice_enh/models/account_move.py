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
        subscription_ids = list()
        invoice_line_ids = self.invoice_line_ids.filtered(lambda x: x.subscription_id)
        for rec in invoice_line_ids:
            rec.subscription_id = False
            subscription_ids.append([rec, rec.subscription_id])

        res =  super()._post(soft=soft)

        for invoice_line in subscription_ids:
            invoice_line[0].subscription_id = invoice_line[1]

        return res
