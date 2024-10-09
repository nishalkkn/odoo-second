from odoo import models

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        message = "Your quotation has been confirmed and is now a sale order."
        for order in self:
            order.message_post(body=message)
            if order.partner_id:
                order.partner_id.message_post(body=message)
        return res
