# Copyright 2017, Vauxoo, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Xunnel Bank',
    'summary': '''
        Use Xunnel Bank to retrieve bank statements.
    ''',
    'version': '12.0.1.0.55',
    'author': 'Jarsa Sistemas,Vauxoo',
    'category': 'Accounting',
    'website': 'http://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'account_accountant',
        'account_online_sync',
    ],
    'data': [
        'data/config_parameters.xml',
        'views/account_config_settings.xml',
        'views/accountant_dashboard.xml',
        'security/account_xunnel_security.xml',
        'views/assets.xml',
        'wizards/change_date.xml',
    ],
    'qweb': [
        'views/account_templates.xml'
    ],
    'demo': [
        'demo/res_company.xml',
        'demo/online_providers.xml',
        'demo/online_journals.xml',
        'demo/account_journals.xml',
    ],
    'installable': True,
}
