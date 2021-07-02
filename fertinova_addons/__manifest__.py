# -*- coding: utf-8 -*-
{
    'name': "fertinova_addons",
    'summary': """Custom addons for enterprise Fertinova""",
    'description': """Módulo que gestiona las distintas personalizaciones que requiere la empresa FERTINOVA en su gestión de Odoo""",
    'author': "Sebastian Ayala Mendez",
    'website': "https://fertinova.odoo.com/web",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '12.0.1.0.1',
    # any module necessary for this one to work correctly
    'depends': ['account', 'purchase_stock', 'sale_management'],
    # always loaded
    'data': [
        #Security Files:
        'security/ir.model.access.csv',
        'security/account_security.xml',     
        
        #Views:
        'views/account_move.xml',        
        #'views/account_payments_inherited_view.xml', DESARROLLO CANCELADO        
        'views/product_template_inherited_view.xml',
        'views/purchase_inherited_view.xml',
        'views/res_partner_inherited_view.xml',
        'views/sale_inherited_view.xml',       
        'views/stock_move_inherited_view.xml',
        'views/sequences.xml',
        'views/stock_picking_inherited_view.xml',
        'views/cfdi.xml',
        #'views/reporting_stock_sales_purchases.xml', DESARROLLO CANCELADO
        'views/reporteo_fletes.xml',
        'views/report.xml',

        #Wizards:
        'wizard/account_move_inherited_view.xml',
        'wizard/fuel_invoice.xml',     

        #reports
        'reports/trial_report.xml',  
        'reports/reporte_lin_ped_venta.xml', 
        'reports/reporte_orden_servicio_fletes.xml', 
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
