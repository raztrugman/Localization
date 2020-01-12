# -*- encoding: utf-8 -*-

{
    'name': 'Israel - System 1000 Import files',
    'version': '1.0',
    'category': 'Accounting',
    'description': """
        Import files from System 1000
    """,
    'website': '',
    'depends': [
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/ilSystem1000ImportFiles.xml',
        'views/wizard_view.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml'
    ],
    'installable': True,
}
