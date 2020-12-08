# -*- coding: utf-8 -*-
{
    'name': "wobin_logistics",

    'summary': """Management of Logistics for Transportes de Alba""",

    'description': """This application seeks to provide a new tool in order
    to give an improved administration for fleets, transportations, expenses,
    sales and accounting documents in Transportes de Alba's processes""",

    'author': "Wobin Simple Cloud",
    'website': "https://fertinova.odoo.com/web",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet', 'hr_expense', 'sale_management'],

    # always loaded
    'data': [
        #security
        'security/ir.model.access.csv',

        #views
        'views/contracts.xml',
        'views/trips.xml',
        'views/views.xml',

        #reports
        'views/templates.xml',
        'reports/contracts_reports.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}