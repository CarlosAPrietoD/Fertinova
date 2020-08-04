# -*- coding: utf-8 -*-
{
    'name': "transportes_alba_customs",

    'summary': """Module for Transportes de Alba in order to add new functionalities in its Logistics
                  concernings Quotations and Trips Process""",

    'description': """Module which looks for improving a new whole area in Logistics, adding 
                      effectual controls, views, validations, models for integrating CRM with
                      new aspects of Quotations and  Trips""",

    'author': "Wobin Simple CLoud",
    'website': "https://fertinova.odoo.com/web",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'crm'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}