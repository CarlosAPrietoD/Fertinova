# Copyright 2019 Vauxoo
# License AGPL-3 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Instance Creator',
    'summary': '''
    Instance creator for fertinova. This is the app.
    ''',
    'author': 'Vauxoo',
    'website': 'https://fertinova.mx',
    'license': 'AGPL-3',
    'category': 'Installer',
    'version': '12.0.1.0.0',
    'depends': [
        'account_accountant',
        'company_country',
        'crm',
        'l10n_mx_avoid_reversal_entry',
        'l10n_mx_cash_basis_entries',
        'l10n_mx_edi_cancellation_complement',
        'l10n_mx_edi_discount',
        'l10n_mx_edi_partner_defaults',
        'l10n_mx_edi_reports',
        'l10n_mx_reports_closing',
        'l10n_mx_edi_hr_expense',
        'mrp',
        'purchase',
        'sale_management',
        'currency_rate_live',
    ],
    'data': [
        'data/res_company.xml',
        'data/res_currency_data.xml',
        'security/security.xml',
        'wizards/internal_transfer_multicurrency_view.xml',
        'views/account_payment.xml',
        'views/hr_expense.xml',
        'views/sale_views.xml',
        'views/stock_picking_views.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
