# -*- coding: utf-8 -*-

from odoo import models, fields


class PosConfig(models.Model):
    _inherit = "pos.config"

    is_pos_discount_limit = fields.Boolean('Discount limit', help='Check this field for enabling discount limit')
    pos_discount_limit = fields.Float('Limit', help='The discount limit')
