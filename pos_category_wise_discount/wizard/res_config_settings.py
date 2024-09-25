# -*- coding: utf-8 -*-

from odoo import models, fields


class PosCategoryWiseDiscount(models.TransientModel):
    _inherit = "res.config.settings"

    _is_pos_discount_limit = fields.Boolean('Discount limit', config_parameter='pos_category_wise_discount._is_pos_discount_limit',
                                        help='Check this field for enabling discount limit')
    pos_discount_limit = fields.Float('Limit', config_parameter='pos_category_wise_discount.pos_discount_limit',
                                        help='The discount limit')