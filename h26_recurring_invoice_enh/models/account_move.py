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
