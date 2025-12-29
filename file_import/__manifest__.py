{
    'name': 'File Import',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Import files in various formats',
    'depends': ['base', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/file_import_views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
