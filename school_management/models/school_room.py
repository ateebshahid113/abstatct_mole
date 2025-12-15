from odoo import models, fields

class SchoolRoom(models.Model):
    _name = 'school.room'
    _description = 'School Room'

    name = fields.Char(string='Room Name', required=True)
    capacity = fields.Integer(string='Capacity')
    building = fields.Char(string='Building')
    floor = fields.Integer(string='Floor')
    student_ids = fields.One2many('school.student', 'room_id', string='Students')
    teacher_ids = fields.One2many('school.teacher', 'room_id', string='Teachers')
