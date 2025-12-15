from odoo import models, fields, api

class SchoolStudent(models.Model):
    _name = 'school.student'
    _inherit = 'school.person.abstract'
    _description = 'School Student'

    age = fields.Integer(string='Age')
    grade = fields.Char(string='Grade')
    room_id = fields.Many2one('school.room', string='Room')



    def get_student_info(self):
        """Get formatted student information"""
        info = self.get_full_contact()
        if self.age:
            info += f" | Age: {self.age}"
        if self.grade:
            info += f" | Grade: {self.grade}"
        return info



    @api.model
    def get_students_by_grade(self, grade):
        """Get all students in a specific grade"""
        return self.search([('grade', '=', grade), ('active', '=', True)])
