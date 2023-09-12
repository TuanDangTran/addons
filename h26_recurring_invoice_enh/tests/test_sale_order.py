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

    # def test_action_create_invoice(self):
    #     for i in range(lop_number):
    #         self.Subscriptions.action_invoice_subscription()
    #     account_move = self.env['account.move'].search([('invoice_line_ids.sale_line_ids.order_id', '=', self.Subscriptions.id)])
    #     self.assertEqual(lop_number, len(account_move))
    #
    def test_cron_job_recurring_invoices(self):
        domain = self.SaleOrder._recurring_invoice_domain()
        subscriptions = self.env['sale.order'].search(domain)

        len_account_move = []
        to_day = date.today()
        for sub in subscriptions:
            sub.next_invoice_date = to_day
            sub.end_date = to_day
            account_move = self.env['account.move'].search(
                [('invoice_line_ids.sale_line_ids.order_id', '=', sub.id)])
            len_account_move.append([sub.id, len(account_move)])
        for i in range(lop_number):
            self.env['sale.order']._cron_recurring_create_invoice()

        for sub in subscriptions:
            if sub:
                print('''----''')
                account_move = self.env['account.move'].search(
                    [('invoice_line_ids.sale_line_ids.order_id', '=', sub.id)])
                for i in len_account_move:
                    if i[0] == sub.id:
                        self.assertEqual(lop_number + i[1], len(account_move))
