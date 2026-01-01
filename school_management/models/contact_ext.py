from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_role = fields.Selection(
        [('customer', 'Customer'), ('vendor', 'Vendor')],
        compute='_compute_partner_role',
        store=False
    )

    @api.depends('partner_id', 'move_type')
    def _compute_partner_role(self):
        for move in self:
            move.partner_role = False
            if not move.partner_id:
                continue

            if move.move_type in ('out_invoice', 'out_refund'):
                move.partner_role = 'customer'
            elif move.move_type in ('in_invoice', 'in_refund'):
                move.partner_role = 'vendor'
