# -*- coding: utf-8 -*-

from odoo import models, fields


class PosCategoryWiseDiscount(models.TransientModel):
    _inherit = "res.config.settings"

    pos_discount_limit_bool = fields.Boolean('Discount limit', related='pos_config_id.is_pos_discount_limit',
                                             readonly=False)
    pos_disc_limit = fields.Float('Limit', related='pos_config_id.pos_discount_limit', readonly=False)
