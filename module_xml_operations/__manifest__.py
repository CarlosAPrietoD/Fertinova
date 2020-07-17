# -*- coding: utf-8 -*-
{
    'name': "module_xml_operations",

    'summary': """Module for read XML files""",

    'description': """Module with the purposee for read XML files in order to retrieve data from FERTICO""",

    'author': "FERTICO",
    'website': "http://www.fertico.com/web",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '11.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}