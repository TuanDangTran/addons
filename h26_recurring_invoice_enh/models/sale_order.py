# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from ast import literal_eval


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_invoice_subscription(self):
        if self.payment_exception or not self.is_subscription:
            return
        return super(SaleOrder, self.with_context(multiple_draft_invoices=True)).action_invoice_subscription()

    def _create_recurring_invoice(self, automatic=False, batch_size=30):
        order_not_payment_token = self._get_order_with_payment_info()
        result = super()._create_recurring_invoice(automatic, batch_size)
        if len(order_not_payment_token):
            self.after_create_recurring_invoice(order_not_payment_token)
        return result

    def _get_order_with_payment_info(self):
        order_not_payment_token = []
        order_ids = self._get_sale_order_ids()
        for rec in order_ids.filtered(lambda x: not  x.payment_token_id):
            rec.payment_token_id = rec._get_payment_token_id().id
            order_not_payment_token.append(rec)
        return order_not_payment_token

    def after_create_recurring_invoice(self, order_not_payment_token):
        for order in order_not_payment_token:
            order.payment_token_id = False
            if order.payment_token_id.tmp_payment_token:
                order.payment_token_id.unlink()

    def _get_sale_order_ids(self):
        if not len(self) and self._context.get('multiple_draft_invoices'):
            search_domain = self._recurring_invoice_domain()
            return self.search(search_domain)
        return self

    def _create_invoices(self, grouped=False, final=False, date=None):
        move_id_and_type = []
        if self._context.get('multiple_draft_invoices', None):
            move_ids = self.filtered(lambda x: x.is_subscription).order_line.invoice_lines.move_id
            for move_id in move_ids:
                move_id_and_type.append([move_id, move_id.move_type])
                move_id.move_type = 'entry'
        res =  super()._create_invoices(grouped, final, date)
        for move_id in move_id_and_type:
            move_id[0].move_type = move_id[1]
        return res

    def _get_payment_token_id(self):
        field_name = 'payment_token_id'
        models = self.fields_get([field_name])[field_name].get('relation')
        domain = [('partner_id', 'child_of', self.partner_id.id), ('company_id', '=', self.env.company.id)]
        payment_token_id = self.env[models].search(domain, limit=1)
        if payment_token_id:
            return payment_token_id
        return self.env[models].create(self._prepare_payment_token_vals())

    def _prepare_payment_token_vals(self):
        return {
            'partner_id': self.partner_id.id,
            'provider_ref': 'tmp payment',
            'provider_id': self.env['payment.provider'].search([], limit=1).id,
            'tmp_payment_token': True
        }

    def _get_invoiceable_lines(self, final=False):
        if self._context.get('multiple_draft_invoices', None):
            self = self.with_context({'recurring_automatic': False})
        return super()._get_invoiceable_lines(final)

    def _handle_automatic_invoices(self, auto_commit, invoices):
        if self._context.get('multiple_draft_invoices', None):
            return invoices
        return super()._handle_automatic_invoices(auto_commit, invoices)

    def _cron_recurring_create_invoice(self):
        res =  super(SaleOrder, self.with_context(multiple_draft_invoices=True))._cron_recurring_create_invoice()
        self._update_subcriptions_is_invoice_cron()
        return res

    def _update_subcriptions_is_invoice_cron(self):
        search_domain = self._recurring_invoice_domain()
        all_subscriptions = self.search(search_domain)
        all_subscriptions.write({'is_invoice_cron': False})
