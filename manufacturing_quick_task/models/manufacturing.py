from odoo import fields, models, Command


class ManufacturingQuickTask(models.Model):
    _inherit = 'mrp.production'

    cost_of_components = fields.Float('Cost of components', compute='_compute_cost_of_components',
                                      help="Cost of used components")
    invoice_ids = fields.One2many('account.move', 'manufacture_id', 'Invoice id')
    extra_cost_ids = fields.One2many('extra.cost', 'manufacture_id', string="Extra cost")

    def _compute_cost_of_components(self):
        """computing cost of components"""
        for rec in self:
            total_cost = 0
            for val in self.move_raw_ids:
                total_cost += (val.product_id.standard_price * val.product_uom_qty)
            rec.cost_of_components = total_cost

    def action_create_bill(self):
        """creating bill"""
        billing_line = []
        for rec in self.move_raw_ids:
            if rec.picked:
                billing_line.append(Command.create({
                    'product_id': rec.product_id.id,
                    'quantity': rec.quantity,
                }))
        for rec in self.extra_cost_ids:
            billing_line.append(Command.create({
                'price_unit': rec.charge,
                'name': rec.description,
            }))
        bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.user_id.id,
            'invoice_line_ids': billing_line,
            'manufacture_id': self.id,
        })
        return {
            'name': 'customer invoice',
            'res_model': 'account.move',
            'type': 'ir.actions.act_window',
            'view_type': 'tree,form',
            'view_mode': 'form',
            'target': 'current',
            'res_id': bill.id,
        }
