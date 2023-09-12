# -*- coding: utf-8 -*-
# Part of IT IS AG. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import tagged
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from .common import TestSaleOrderCommon


lop_number = 5


class TestSaleOrder(TestSaleOrderCommon):

    def setUp(self):
        super(TestSaleOrder, self).setUp()

    def test_action_create_invoice(self):
        for i in range(lop_number):
            self.Subscriptions.action_invoice_subscription()
        account_move = self.env['account.move'].search([('invoice_line_ids.sale_line_ids.order_id', '=', self.Subscriptions.id)])
        self.assertEqual(lop_number, len(account_move))
    #
    def test_cron_job_recurring_invoices(self):
        account_move = self.env['account.move'].search(
                    [('invoice_line_ids.sale_line_ids.order_id', '=', self.Subscriptions.id)])
        for i in range(lop_number):
            self.env['sale.order']._cron_recurring_create_invoice()
        account_move1 = self.env['account.move'].search(
                    [('invoice_line_ids.sale_line_ids.order_id', '=', self.Subscriptions.id)])
        self.assertEqual(lop_number + len(account_move), len(account_move1))
