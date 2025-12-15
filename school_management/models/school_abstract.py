from odoo import models, fields, api

class SchoolPersonAbstract(models.AbstractModel):
    _name = 'school.person.abstract'
    _description = 'Abstract Model for School Persons'

    name = fields.Char(string='Name', required=True)
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    active = fields.Boolean(string='Active', default=True)
    
    @api.model
    def get_full_contact(self):
        """Return formatted contact information"""
        contact = self.name
        if self.email:
            contact += f" ({self.email})"
        if self.phone:
            contact += f" - {self.phone}"
        return contact
    
    def toggle_active(self):
        """Toggle active status"""
        self.active = not self.active
        return True
    
    @api.model
    def search_by_contact(self, search_term):
        """Search by name, email or phone"""
        domain = [
            '|', '|',
            ('name', 'ilike', search_term),
            ('email', 'ilike', search_term),
            ('phone', 'ilike', search_term)
        ]
        return self.search(domain)
