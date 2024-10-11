# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    height = fields.Float('Height', help="Height of the user")
    math_field = fields.Char('Calculate',help="Calculate value")
