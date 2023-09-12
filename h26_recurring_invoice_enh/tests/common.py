# -*- coding: utf-8 -*-
# Part of IT IS AG. See LICENSE file for full copyright and licensing details.

from odoo.tests.common import TransactionCase, tagged
from datetime import datetime
from dateutil.relativedelta import relativedelta


class TestSaleOrderCommon(TransactionCase):

    def setUp(self):
        super(TestSaleOrderCommon, self).setUp()
        self.SaleOrder = self.env['sale.order']
        self.SaleOrderLine = self.env['sale.order.line']
        self.ResPartner = self.env['res.partner']
        self.ProductPricelist = self.env['product.pricelist']
        self.ProductTemplate = self.env['product.template']

        self.Pricelist = self.ProductPricelist.create({
            'name': 'Pricelist Test'
        })
        self.Partner = self.ResPartner.create({
            'name': 'Partner Test'
        })
        self.Product = self.env.ref('sale_subscription.product_car_leasing')

        self.Subscriptions = self.SaleOrder.create({
            'partner_id': self.Partner.id,
            'is_subscription': True,
            'pricelist_id': self.Pricelist.id,
            'recurrence_id': self.env.ref('sale_temporal.recurrence_daily').id,
            'stage_id': self.env['sale.order.stage'].search([], order='sequence', limit=1).id
        })
        self.OrderLine = self.SaleOrderLine.create({
                'name': self.Product.name,
                'order_id': self.Subscriptions.id,
                'product_id': self.Product.id,
                'product_uom_qty': 3,
                'product_uom': self.Product.uom_id.id,
                'price_unit': 42,
                'display_type': False
        }
        )
        self.Subscriptions.action_confirm()
