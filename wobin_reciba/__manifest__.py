# -*- coding: utf-8 -*-
{
    'name': "Wobin Reciba",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Wobin",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '2.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'purchase', 'sale'],

    # always loaded
    'data': [
        # security
        'security/reciba_security.xml',
        'security/ir.model.access.csv',

        #views
        'views/views.xml',
        'views/templates.xml',
        'views/print.xml',
        'views/tickets.xml',
        'views/reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}