# -*- coding: utf-8 -*-
{
    'name': "Reciba",

    'summary': """Módulo para la gestión de Recepción de grano y control de inventarios, calidad, liquidaciones e informes""",

    'description': """Este módulo procura facilitar la administración de la Recepción de grano
                      de los productores, fomentar un mayor control de calidad, asignación de
                      almacenes o ubicaciones; así como la administración de liquidaciones y 
                      visualización de informes""",

    'author': "WOBIN simple cloud",
    'website': "https://fertinova.odoo.com/web",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'stock', 'sale'],

    # always loaded
    'data': [
        #security
        'security/ir.model.access.csv',

        #reports
        'reports/reporte_liquidaciones.xml',         
        
        #reports
        'reports/reporte_liquidaciones.xml',           
        
        #views
        'views/reciba.xml',  
        'views/prestamos_abonos.xml', 
        'views/liquidaciones.xml',               
        'views/templates.xml',
        'views/views.xml',     
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
