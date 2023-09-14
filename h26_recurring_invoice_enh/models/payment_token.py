# -*- coding: utf-8 -*-
from odoo import models, api, fields


class PaymentToken(models.Model):
    _inherit = 'payment.token'

    tmp_payment_token = fields.Boolean()
