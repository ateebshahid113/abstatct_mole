from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_type = fields.Selection(
        [
            ('customer', 'Customer'),
            ('vendor', 'Vendor'),
        ],
        string="Partner Type",
        default='customer',
        tracking=True
    )

    @api.onchange('partner_type')
    def _onchange_partner_type(self):
        for partner in self:
            if partner.partner_type == 'vendor':
                if partner.supplier_rank < 1:
                    partner.supplier_rank = 1
            elif partner.partner_type == 'customer':
                if partner.customer_rank < 1:
                    partner.customer_rank = 1
