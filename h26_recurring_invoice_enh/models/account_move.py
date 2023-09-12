# -*- coding: utf-8 -*-
# Part of IT IS AG. See LICENSE file for full copyright and licensing details.

from odoo import models, api, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    # move_type = fields.Selection(selection_add=[('subscription', 'Subscription')], ondelete={'subscription': 'cascade'})
    def button_cancel(self):
        if self._context.get('multiple_draft_invoices', None):
            return True
        return super(AccountMove, self).button_cancel()

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        if self._context.get('multiple_draft_invoices') and self.state == 'draft':
            self.name = '/'
        else:
            super()._compute_name()

