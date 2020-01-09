# -*- encoding: utf-8 -*-

{
    'name': 'Israel - System 1000 Export file',
    'version': '1.0',
    'category': 'Accounting',
    'description': """
        System 1000 Export file for Israel
    """,
    'website': '',
    'depends': [

    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/ilSystem1000ExportFile.xml',
        'views/wizard_view.xml',
        'views/res_company_views.xml',
        'views/res_partner_views.xml'
    ],
    'installable': True,
}
