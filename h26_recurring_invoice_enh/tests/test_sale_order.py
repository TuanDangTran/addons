# -*- coding: utf-8 -*-
# Part of IT IS AG. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import tagged
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from .common import TestSaleOrderCommon


lop_number = 5
model = 'account.move'


class TestSaleOrder(TestSaleOrderCommon):

    def setUp(self):
        super(TestSaleOrder, self).setUp()

    # def test_action_create_invoice(self):
    #     for i in range(lop_number):
    #         self.Subscriptions.action_invoice_subscription()
    #     account_move = self.env[model].search([('invoice_line_ids.sale_line_ids.order_id', '=', self.Subscriptions.id)])
    #     self.assertEqual(lop_number, len(account_move))
    #
    # def test_cron_job_recurring_invoices(self):
    #     account_move = self.env[model].search(
    #                 [('invoice_line_ids.sale_line_ids.order_id', '=', self.Subscriptions.id)])
    #     for i in range(lop_number):
    #         self.Subscriptions.next_invoice_date = date.today()
    #         self.env['sale.order']._cron_recurring_create_invoice()
    #     account_move1 = self.env[model].search(
    #                 [('invoice_line_ids.sale_line_ids.order_id', '=', self.Subscriptions.id)])
    #     self.assertEqual(lop_number + len(account_move), len(account_move1))
    #
    # def test_subscriptions_have_payment_exception(self):
    #     subscriptions = self.Subscriptions.copy()
    #     subscriptions.action_confirm()
    #     subscriptions.payment_exception = True
    #     account_move1 = len(self.env[model].search(
    #         [('invoice_line_ids.sale_line_ids.order_id', '=', subscriptions.id)]))
    #     subscriptions.action_invoice_subscription()
    #     account_move = len(self.env[model].search([('invoice_line_ids.sale_line_ids.order_id', '=', subscriptions.id)]))
    #     self.assertEqual(account_move1, account_move)
    #
    # def test_subscriptions_have_is_subscription(self):
    #     subscriptions = self.Subscriptions.copy()
    #     subscriptions.action_confirm()
    #     subscriptions.is_subscription = False
    #     account_move1 = len(self.env[model].search(
    #         [('invoice_line_ids.sale_line_ids.order_id', '=', subscriptions.id)]))
    #     subscriptions.action_invoice_subscription()
    #     account_move = len(self.env[model].search([('invoice_line_ids.sale_line_ids.order_id', '=', subscriptions.id)]))
    #     self.assertEqual(account_move1, account_move)

    def test_sub_next_to_invoice(self):
        next_invoice_date = self.Subscriptions.next_invoice_date
        for i in range(lop_number):
            self.Subscriptions.action_invoice_subscription()
            next_invoice_date2 = self.env['account.move.line'].search([('sale_line_ids.order_id', '=', self.Subscriptions.id)]
                                                                      , order="id desc", limit=1).subscription_end_date
            self.assertEqual(next_invoice_date + relativedelta(days=self.Subscriptions.recurrence_id.duration), next_invoice_date2 + relativedelta(days=1))
            account_moves = self.env[model].search([('invoice_line_ids.sale_line_ids.order_id', '=', self.Subscriptions.id), ('state', '=', 'draft')])
            for account_move in account_moves:
                account_move._post()
                next_invoice_date = self.Subscriptions.next_invoice_date
                self.assertEqual(next_invoice_date, next_invoice_date2 + relativedelta(days=1))
