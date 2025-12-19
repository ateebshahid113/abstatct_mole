from odoo import models, fields, api

class StudentTeacherWizard(models.TransientModel):
    _name = 'student.teacher.wizard'
    _description = 'Student Teacher Assignment Wizard'

    student_id = fields.Many2one('school.student', string='Student', required=True)
    teacher_id = fields.Many2one('school.teacher', string='Teacher', required=True)
    room_id = fields.Many2one('school.room', string='Room')

    def assign_student_teacher(self):
        if self.room_id:
            self.student_id.room_id = self.room_id
            self.teacher_id.room_id = self.room_id
        return {'type': 'ir.actions.act_window_close'}
