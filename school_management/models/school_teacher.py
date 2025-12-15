from odoo import models, fields

class SchoolTeacher(models.Model):
    _name = 'school.teacher'
    _inherit = 'school.person.abstract'
    _description = 'School Teacher'

    subject = fields.Char(string='Subject')
    room_id = fields.Many2one('school.room', string='Room')
    
    def get_teacher_info(self):
        """Get formatted teacher information"""
        info = self.get_full_contact()
        if self.subject:
            info += f" | Subject: {self.subject}"
        return info
