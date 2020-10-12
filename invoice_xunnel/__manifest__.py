# Copyright 2018, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Xunnel Invoice',
    'summary': '''
        Use Xunnel Invoice to retrieve invoices from SAT.
    ''',
    'version': '12.0.1.0.55',
    'author': 'Jarsa Sistemas,Vauxoo',
    'category': 'Accounting',
    'website': 'http://www.jarsa.com.mx',
    'license': 'LGPL-3',
    'depends': [
        'account_xunnel',
        'documents',
        'l10n_mx_edi',
    ],
    'data': [
        'data/folder.xml',
        'views/assets.xml',
        'views/documents.xml',
        'views/ir_attachment_views.xml',
        'security/groups.xml',
        'wizards/attach_xmls_wizard_view.xml',
        'wizards/attachments.xml',
        'views/account_config_settings.xml',
    ],
    'demo': [
        'demo/res_company.xml',
    ],
    'qweb': [
        'static/src/xml/*.xml'
    ],
    'installable': True,
}
