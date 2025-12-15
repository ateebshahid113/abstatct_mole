{
    'name': 'School Management',
    'version': '18.0.1.0.0',
    'category': 'Education',
    'summary': 'Manage students, teachers and rooms',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/school_student_views.xml',
        'views/school_teacher_views.xml',
        'views/school_room_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
}
