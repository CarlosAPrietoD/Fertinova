from odoo import models, fields, api

#==================================================================================================

#======================================= Account module ===========================================

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    access_token = fields.Char(track_visibility='onchange')
    access_url = fields.Char(track_visibility='onchange')
    access_warning = fields.Text(track_visibility='onchange')
    account_id = fields.Many2one(track_visibility='onchange')
    activity_date_deadline = fields.Date(track_visibility='onchange')
    activity_ids = fields.One2many(track_visibility='onchange')
    activity_summary = fields.Char(track_visibility='onchange')
    activity_type_id =  fields.Many2one(track_visibility='onchange')
    activity_user_id = fields.Many2one(track_visibility='onchange')
    sequence_number_next = fields.Char(track_visibility='onchange')
    sequence_number_next_prefix = fields.Char(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    payment_term_id = fields.Many2one(track_visibility='onchange')
    partner_shipping_id = fields.Many2one(track_visibility='onchange')
    payment_term_id = fields.Many2one(track_visibility='onchange')
    l10n_mx_edi_partner_bank_id = fields.Many2one(track_visibility='onchange')
    l10n_mx_edi_payment_method_id = fields.Many2one(track_visibility='onchange')
    l10n_mx_edi_usage = fields.Selection([
        ('G01', 'Acquisition of merchandise'),
        ('G02', 'Returns, discounts or bonuses'),
        ('G03', 'General expenses'),
        ('I01', 'Constructions'),
        ('I02', 'Office furniture and equipment investment'),
        ('I03', 'Transportation equipment'),
        ('I04', 'Computer equipment and accessories'),
        ('I05', 'Dices, dies, molds, matrices and tooling'),
        ('I06', 'Telephone communications'),
        ('I07', 'Satellite communications'),
        ('I08', 'Other machinery and equipment'),
        ('D01', 'Medical, dental and hospital expenses.'),
        ('D02', 'Medical expenses for disability'),
        ('D03', 'Funeral expenses'),
        ('D04', 'Donations'),
        ('D05', 'Real interest effectively paid for mortgage loans (room house)'),
        ('D06', 'Voluntary contributions to SAR'),
        ('D07', 'Medical insurance premiums'),
        ('D08', 'Mandatory School Transportation Expenses'),
        ('D09', 'Deposits in savings accounts, premiums based on pension plans.'),
        ('D10', 'Payments for educational services (Colegiatura)'),
        ('P01', 'To define'),
    ],track_visibility='onchange')
    date_invoice = fields.Date(track_visibility='onchange')
    date_due = fields.Date(track_visibility='onchange')
    user_id = fields.Many2one(track_visibility='onchange')
    team_id = fields.Many2one(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    l10n_mx_edi_origin = fields.Char(track_visibility='onchange')
    invoice_line_ids = fields.One2many(track_visibility='onchange')
    journal_id = fields.Many2one(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    reference = fields.Char(track_visibility='onchange')
    name = fields.Char(track_visibility='onchange')
    incoterm_id = fields.Many2one(track_visibility='onchange')
    fiscal_position_id = fields.Many2one(track_visibility='onchange')
    origin = fields.Char(track_visibility='onchange')
    partner_bank_id = fields.Many2one(track_visibility='onchange')
    tax_line_ids = fields.One2many(track_visibility='onchange')
    state = fields.Selection([
            ('draft','Draft'),
            ('open', 'Open'),
            ('in_payment', 'In Payment'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),],track_visibility='onchange')


class AccountJournal(models.Model):
    _name = 'account.journal'
    _inherit = ['account.journal', 'mail.thread']

    account_control_ids = fields.Many2many(track_visibility='onchange')
    account_online_journal_id = fields.Many2one(track_visibility='onchange')
    account_online_provider_id = fields.Many2one(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    alias_domain = fields.Char(track_visibility='onchange')
    alias_id = fields.Many2one(track_visibility='onchange')
    alias_name = fields.Char(track_visibility='onchange')
    amount_authorized_diff = fields.Float(track_visibility='onchange')
    at_least_one_inbound = fields.Boolean(track_visibility='onchange')
    at_least_one_outbound = fields.Boolean(track_visibility='onchange')
    bank_acc_number = fields.Char(track_visibility='onchange')
    bank_account_id = fields.Many2one(track_visibility='onchange')
    bank_id = fields.Many2one(track_visibility='onchange')
    bank_statement_creation = fields.Selection([('none', 'Create one statement per synchronization'),
                ('day', 'Create daily statements'),
                ('week', 'Create weekly statements'),
                ('bimonthly', 'Create bi-monthly statements'),
                ('month', 'Create monthly statements')], track_visibility='onchange')
    bank_statements_source = fields.Selection([('undefined', 'Undefined Yet')], track_visibility='onchange')
    belongs_to_company = fields.Boolean(track_visibility='onchange')
    check_manual_sequencing = fields.Boolean(track_visibility='onchange')
    check_next_number = fields.Integer(track_visibility='onchange')
    check_printing_payment_method_selected = fields.Boolean(track_visibility='onchange')
    check_sequence_id = fields.Many2one(track_visibility='onchange')
    code = fields.Char(track_visibility='onchange')
    color = fields.Integer(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    company_partner_id = fields.Many2one(track_visibility='onchange')
    create_date = fields.Datetime(track_visibility='onchange')
    create_uid = fields.Many2one(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    default_credit_account_id = fields.Many2one(track_visibility='onchange')
    default_debit_account_id = fields.Many2one(track_visibility='onchange')
    display_name = fields.Char(track_visibility='onchange')
    group_invoice_lines = fields.Boolean(track_visibility='onchange')
    has_synchronized_xunnel = fields.Boolean(track_visibility='onchange')
    id = fields.Integer(track_visibility='onchange')
    inbound_payment_method_ids = fields.Many2many(track_visibility='onchange')
    journal_user = fields.Boolean(track_visibility='onchange')
    kanban_dashboard = fields.Text(track_visibility='onchange')
    kanban_dashboard_graph = fields.Text(track_visibility='onchange')
    l10n_mx_address_issued_id = fields.Many2one(track_visibility='onchange')
    l10n_mx_edi_payment_method_id = fields.Many2one(track_visibility='onchange')
    loss_account_id = fields.Many2one(track_visibility='onchange')
    name = fields.Char(track_visibility='onchan')
    next_synchronization = fields.Datetime(track_visibility='onchange')
    online_journal_last_sync = fields.Date(track_visibility='onchange')
    outbound_payment_method_ids	= fields.Many2many(track_visibility='onchange')
    post_at_bank_rec = fields.Boolean(track_visibility='onchange')
    profit_account_id = fields.Many2one(track_visibility='onchange')
    refund_sequence = fields.Boolean(track_visibility='onchange')
    refund_sequence_id = fields.Many2one(track_visibility='onchange')
    refund_sequence_number_next = fields.Integer(track_visibility='onchange')
    sequence = fields.Integer(track_visibility='onchange')
    sequence_id = fields.Many2one(track_visibility='onchange')
    sequence_number_next = fields.Integer(track_visibility='onchange')
    show_on_dashboard = fields.Boolean(track_visibility='onchange')
    synchronization_status = fields.Char(track_visibility='onchange')
    type = fields.Selection([
            ('sale', 'Sale'),
            ('purchase', 'Purchase'),
            ('cash', 'Cash'),
            ('bank', 'Bank'),
            ('general', 'Miscellaneous'),
        ], track_visibility='onchange')
    type_control_ids = fields.Many2many(track_visibility='onchange')
    update_posted = fields.Boolean(track_visibility='onchange')
    write_date = fields.Datetime(track_visibility='onchange')
    write_uid = fields.Many2one(track_visibility='onchange')


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    payment_type = fields.Selection([('inbound', 'Inbound'), ('outbound', 'Outbound'),('transfer', 'Internal Transfer')],track_visibility='onchange')
    partner_type = fields.Selection([('customer', 'Customer'), ('supplier', 'Vendor')], track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    amount = fields.Monetary(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    journal_id = fields.Many2one(track_visibility='onchange')
    l10n_mx_edi_payment_method_id = fields.Many2one(track_visibility='onchange')
    x_studio_contacto_deudor_acreedor_1 = fields.Many2one(track_visibility='onchange')
    payment_date = fields.Date(track_visibility='onchange')
    communication = fields.Char(track_visibility='onchange')
    l10n_mx_edi_partner_bank_id = fields.Many2one(track_visibility='onchange')
    l10n_mx_edi_pac_status = fields.Selection([
            ('none', 'CFDI not necessary'),
            ('retry', 'Retry'),
            ('to_sign', 'To sign'),
            ('signed', 'Signed'),
            ('to_cancel', 'To cancel'),
            ('cancelled', 'Cancelled')
        ], track_visibility='onchange')
    l10n_mx_edi_sat_status = fields.Selection([
            ('none', 'State not defined'),
            ('undefined', 'Not Synced Yet'),
            ('not_found', 'Not Found'),
            ('cancelled', 'Cancelled'),
            ('valid', 'Valid'),
        ],track_visibility='onchange')
    l10n_mx_edi_origin = fields.Char(track_visibility='onchange')
    payment_transaction_id = fields.Many2one(track_visibility='onchange')
    destination_journal_id = fields.Many2one(track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'), ('posted', 'Posted'), ('sent', 'Sent'), ('reconciled', 'Reconciled'), ('cancelled', 'Cancelled')], track_visibility='onchange')
    
    
'''class ProductProduct(models.Model):
    _inherit = 'product.product'

    name = fields.Char(track_visibility='onchange')
    sale_ok = fields.Boolean(track_visibility='onchange')
    purchase_ok = fields.Boolean(track_visibility='onchange')
    type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Storable Product')],track_visibility='onchange')
    default_code = fields.Char(track_visibility='onchange')
    barcode = fields.Char(track_visibility='onchange')
    categ_id = fields.Many2one(track_visibility='onchange')
    lst_price = fields.Monetary(track_visibility='onchange')
    standard_price = fields.Float(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    uom_po_id = fields.Many2one(track_visibility='onchange')
    description = fields.Text(track_visibility='onchange')
    email_template_id = fields.Many2one(track_visibility='onchange')
    description_sale = fields.Text(track_visibility='onchange')
    seller_ids = fields.Many2one(track_visibility='onchange')
    produce_delay = fields.Float(track_visibility='onchange')
    sale_delay = fields.Float(track_visibility='onchange')
    weight =  fields.Float(track_visibility='onchange')
    volume = fields.Float(track_visibility='onchange')
    description_pickingout = fields.Text(track_visibility='onchange')
    description_pickingin = fields.Text(track_visibility='onchange')
    description_picking = fields.Text(track_visibility='onchange')
    property_stock_production = fields.Many2one(track_visibility='onchange')
    property_stock_inventory = fields.Many2one(track_visibility='onchange')
    property_account_income_id = fields.Many2one(track_visibility='onchange')
    l10n_mx_edi_code_sat_id = fields.Many2one(track_visibility='onchange')
    property_account_expense_id = fields.Many2one(track_visibility='onchange')
    asset_category_id = fields.Many2one(track_visibility='onchange')
    property_account_creditor_price_difference = fields.Many2one(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    mrp_product_qty = fields.Float(track_visibility='onchange')
    bom_count = fields.Integer(track_visibility='onchange')
    purchased_product_qty = fields.Float(track_visibility='onchange')
    sales_count = fields.Float(track_visibility='onchange')
    image_medium = fields.Binary(track_visibility='onchange')'''
    
    
class AccountMove(models.Model):
    _inherit = 'account.move'  
    
    date = fields.Date(track_visibility='onchange')
    ref = fields.Char(track_visibility='onchange')
    parent_id = fields.Many2one(track_visibility='onchange')
    journal_id = fields.Many2one(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    line_ids = fields.One2many(track_visibility='onchange')
    narration = fields.Text(track_visibility='onchange')
    auto_reverse = fields.Boolean(track_visibility='onchange')
    l10n_mx_closing_move = fields.Boolean(track_visibility='onchange')
    state = fields.Selection([('draft', 'Unposted'), ('posted', 'Posted')], track_visibility='onchange')
    
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line' 

    name = fields.Char(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    account_id = fields.Many2one(track_visibility='onchange')
    debit = fields.Monetary(track_visibility='onchange')
    credit = fields.Monetary(track_visibility='onchange')
    quantity = fields.Float(track_visibility='onchange')
    date = fields.Date(track_visibility='onchange')
    date_maturity = fields.Date(track_visibility='onchange')
    blocked = fields.Boolean(track_visibility='onchange')
    move_id = fields.Many2one(track_visibility='onchange')
    amount_currency = fields.Monetary(track_visibility='onchange')
    analytic_account_id = fields.Many2one(track_visibility='onchange')
    analytic_tag_ids = fields.Many2many(track_visibility='onchange')
    analytic_line_ids = fields.One2many(track_visibility='onchange')

class AccountAnalyticLine(models.Model):
    _name = 'account.analytic.line'
    _inherit = ['account.analytic.line', 'mail.thread']

    name =  fields.Char(track_visibility='onchange')
    account_id = fields.Many2one(track_visibility='onchange')
    tag_ids = fields.Many2many(track_visibility='onchange')
    ref = fields.Char(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    date = fields.Date(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    amount =  fields.Monetary(track_visibility='onchange')
    unit_amount = fields.Float(track_visibility='onchange')
    product_id = fields.Many2one(track_visibility='onchange')
    product_uom_id = fields.Many2one(track_visibility='onchange')
    general_account_id = fields.Many2one(track_visibility='onchange')
    move_id = fields.Many2one(track_visibility='onchange')
    
class CrossoveredBudget(models.Model):
    _inherit = 'crossovered.budget'   
    
    name = fields.Char(track_visibility='onchange')
    user_id = fields.Many2one(track_visibility='onchange')
    date_from = fields.Date(track_visibility='onchange')
    date_to = fields.Date(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    crossovered_budget_line = fields.One2many(track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancelled'),
        ('confirm', 'Confirmed'),
        ('validate', 'Validated'),
        ('done', 'Done')
        ], track_visibility='onchange')
    
class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'  
    
    name = fields.Char(track_visibility='onchange')
    category_id = fields.Many2one(track_visibility='onchange')
    code = fields.Char(track_visibility='onchange')
    date = fields.Date(track_visibility='onchange')
    date_first_depreciation = fields.Selection([
        ('last_day_period', 'Based on Last Day of Purchase Period'),
        ('manual', 'Manual (Defaulted on Purchase Date)')], track_visibility='onchange')
    first_depreciation_manual_date = fields.Date(track_visibility='onchange')
    account_analytic_id = fields.Many2one(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    value = fields.Float(track_visibility='onchange')
    salvage_value = fields.Float(track_visibility='onchange')
    value_residual = fields.Float(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    invoice_id = fields.Many2one(track_visibility='onchange')
    analytic_tag_ids = fields.Many2many(track_visibility='onchange')
    depreciation_line_ids = fields.One2many(track_visibility='onchange')
    method = fields.Selection([('linear', 'Linear'), ('degressive', 'Degressive')], track_visibility='onchange')
    prorata = fields.Boolean(track_visibility='onchange')
    method_number = fields.Integer(track_visibility='onchange')
    method_period = fields.Integer(track_visibility='onchange')
    entry_count = fields.Integer(track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'), ('open', 'Running'), ('close', 'Close')], track_visibility='onchange')
    
class ResCurrency(models.Model):
    _name = 'res.currency'
    _inherit = ['res.currency', 'mail.thread']
    
    name = fields.Char(track_visibility='onchange')
    rate = fields.Float(track_visibility='onchange')
    rounding = fields.Float(track_visibility='onchange')
    decimal_places = fields.Integer(track_visibility='onchange')
    currency_unit_label = fields.Char(track_visibility='onchange')
    currency_subunit_label = fields.Char(track_visibility='onchange')
    symbol = fields.Char(track_visibility='onchange')
    position = fields.Selection([('after', 'After Amount'), ('before', 'Before Amount')], track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')


class AccountAccount(models.Model):
    _name = 'account.account'
    _inherit = ['account.account', 'mail.thread']


    code = fields.Char(track_visibility='onchange')
    name = fields.Char(track_visibility='onchange')
    user_type_id = fields.Many2one(track_visibility='onchange')
    tax_ids = fields.Many2many(track_visibility='onchange')
    tag_ids = fields.Many2many(track_visibility='onchange')
    group_id = fields.Many2one(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    reconcile = fields.Boolean(track_visibility='onchange')
    deprecated = fields.Boolean(track_visibility='onchange')
    realizable_account = fields.Boolean(track_visibility='onchange')


class AccountTax(models.Model):
    _name = 'account.tax'
    _inherit = ['account.tax', 'mail.thread']

    name = fields.Char(track_visibility='onchange')
    type_tax_use = fields.Selection([('sale', 'Sales'), ('purchase', 'Purchases'), ('none', 'None'), ('adjustment', 'Adjustment')], track_visibility='onchange')
    amount_type = fields.Selection([('group', 'Group of Taxes'), ('fixed', 'Fixed'), ('percent', 'Percentage of Price'), ('division', 'Percentage of Price Tax Included')], track_visibility='onchange')
    amount = fields.Float(track_visibility='onchange')
    account_id = fields.Many2one(track_visibility='onchange')
    refund_account_id = fields.Many2one(track_visibility='onchange')
    description = fields.Char(track_visibility='onchange')
    tax_group_id = fields.Many2one(track_visibility='onchange')
    tag_ids = fields.Many2many(track_visibility='onchange')
    l10n_mx_cfdi_tax_type = fields.Selection(
        [('Tasa', 'Tasa'),
         ('Cuota', 'Cuota'),
         ('Exento', 'Exento')], track_visibility='onchange')
    analytic_id = fields.Boolean(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    price_include = fields.Boolean(track_visibility='onchange')
    include_base_amount = fields.Boolean(track_visibility='onchange')
    tax_exigibility = fields.Selection(
        [('on_invoice', 'Based on Invoice'),
         ('on_payment', 'Based on Payment'),
        ], track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')


class AccountFiscalPosition(models.Model):
    _name = 'account.fiscal.position'
    _inherit = ['account.fiscal.position', 'mail.thread']
    
    name = fields.Char(track_visibility='onchange')
    l10n_mx_edi_code = fields.Char(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    auto_apply = fields.Boolean(track_visibility='onchange')
    tax_ids = fields.One2many(track_visibility='onchange')
    note = fields.Text(track_visibility='onchange')
    account_ids = fields.One2many(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    
    
class AccountFiscalPosition(models.Model):
    _name = 'account.incoterms'
    _inherit = ['account.incoterms', 'mail.thread']


    name = fields.Char(track_visibility='onchange')
    code = fields.Char(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')

class AccountAccountTag(models.Model):
    _name = 'account.account.tag'
    _inherit = ['account.account.tag', 'mail.thread']

    name = fields.Char(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')


class AccountGroup(models.Model):
    _name = 'account.group'
    _inherit = ['account.group', 'mail.thread']
    
    name = fields.Char(track_visibility='onchange')
    code_prefix = fields.Char(track_visibility='onchange')
    parent_id = fields.Many2one(track_visibility='onchange')

class AccountReconcileModel(models.Model):
    _name = 'account.reconcile.model'
    _inherit = ['account.reconcile.model', 'mail.thread']

    
    name =  fields.Char(track_visibility='onchange')
    rule_type = fields.Selection(selection=[
        ('writeoff_button', 'Manually create a write-off on clicked button.'),
        ('writeoff_suggestion', 'Suggest counterpart values.'),
        ('invoice_matching', 'Match existing invoices/bills.')
    ], track_visibility='onchange')
    match_journal_ids = fields.Many2many(track_visibility='onchange')
    account_id = fields.Many2one(track_visibility='onchange')
    amount_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('percentage', 'Percentage of balance')
        ], track_visibility='onchange')
    tax_id = fields.Many2one(track_visibility='onchange')
    analytic_account_id = fields.Many2one(track_visibility='onchange')
    analytic_tag_ids = fields.Many2many(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    has_second_line = fields.Boolean(track_visibility='onchange')
    label = fields.Char(track_visibility='onchange')
    amount = fields.Float(track_visibility='onchange')
    journal_id = fields.Many2one(track_visibility='onchange')
    

class AccountPaymentTerm(models.Model):
    _name = 'account.payment.term'
    _inherit = ['account.payment.term', 'mail.thread']
    
    name = fields.Char(track_visibility='onchange')
    note = fields.Text(track_visibility='onchange')
    line_ids = fields.One2many(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')


class ProductCategory(models.Model):
    _name = 'product.category'
    _inherit = ['product.category', 'mail.thread']
    
    name =  fields.Char(track_visibility='onchange')
    parent_id = fields.Many2one(track_visibility='onchange')
    property_cost_method = fields.Selection([
        ('standard', 'Standard Price'),
        ('fifo', 'First In First Out (FIFO)'),
        ('average', 'Average Cost (AVCO)')], track_visibility='onchange')
    property_valuation = fields.Selection([
        ('manual_periodic', 'Manual'),
        ('real_time', 'Automated')], track_visibility='onchange')
    property_account_creditor_price_difference_categ = fields.Many2one(track_visibility='onchange')
    property_account_income_categ_id = fields.Many2one(track_visibility='onchange')
    property_account_expense_categ_id = fields.Many2one(track_visibility='onchange')
    property_stock_account_input_categ_id = fields.Many2one(track_visibility='onchange')
    property_stock_account_output_categ_id = fields.Many2one(track_visibility='onchange')
    property_stock_valuation_account_id = fields.Many2one(track_visibility='onchange')
    property_stock_journal = fields.Many2one(track_visibility='onchange')
    route_ids = fields.Many2many(track_visibility='onchange')
    removal_strategy_id = fields.Many2one(track_visibility='onchange')
    
    
class AccountBudgetPost(models.Model):
    _name = 'account.budget.post'
    _inherit = ['account.budget.post', 'mail.thread']


    name = fields.Char(track_visibility='onchange')
    company_id =  fields.Many2one(track_visibility='onchange')
    account_ids = fields.Many2many(track_visibility='onchange')


class AccountAssetCategory(models.Model):
    _name = 'account.asset.category'
    _inherit = ['account.asset.category', 'mail.thread'] 
    
    name = fields.Char(track_visibility='onchange')
    journal_id = fields.Many2one(track_visibility='onchange')
    account_asset_id = fields.Many2one(track_visibility='onchange')
    account_depreciation_id = fields.Many2one(track_visibility='onchange')
    account_depreciation_expense_id = fields.Many2one(track_visibility='onchange')
    account_analytic_id = fields.Many2one(track_visibility='onchange')
    analytic_tag_ids = fields.Many2many(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    method_time = fields.Selection([('number', 'Number of Entries'), ('end', 'Ending Date')], track_visibility='onchange')
    method_number = fields.Integer(track_visibility='onchange')
    method_period = fields.Integer(track_visibility='onchange')
    method_end = fields.Date(track_visibility='onchange')
    open_asset = fields.Boolean(track_visibility='onchange')
    group_entries = fields.Boolean(track_visibility='onchange')
    date_first_depreciation = fields.Selection([
        ('last_day_period', 'Based on Last Day of Purchase Period'),
        ('manual', 'Manual (Defaulted on Purchase Date)')], track_visibility='onchange')
    method = fields.Selection([('linear', 'Linear'), ('degressive', 'Degressive')], track_visibility='onchange')
    method_progress_factor = fields.Float(track_visibility='onchange')


class AccountFinancialHtmlReport(models.Model):
    _name = 'account.financial.html.report'
    _inherit = ['account.financial.html.report', 'mail.thread'] 


    name = fields.Char(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    date_range = fields.Boolean(track_visibility='onchange')
    tax_report = fields.Boolean(track_visibility='onchange')
    debit_credit = fields.Boolean(track_visibility='onchange')
    generated_menu_id = fields.Many2one(track_visibility='onchange')
    comparison = fields.Boolean(track_visibility='onchange')
    cash_basis = fields.Boolean(track_visibility='onchange')
    unfol_all_filters = fields.Boolean(track_visibility='onchange')
    hierarchy_option = fields.Boolean(track_visibility='onchange')
    show_journal_filter = fields.Boolean(track_visibility='onchange')
    analytic = fields.Boolean(track_visibility='onchange')
    applicable_filters_ids = fields.Many2many(track_visibility='onchange')
    line_ids = fields.One2many(track_visibility='onchange')


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account' 

    name = fields.Char(track_visibility='onchange')
    code = fields.Char(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    vehicle_id = fields.Many2one(track_visibility='onchange')
    group_id = fields.Many2one(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    crossovered_budget_line = fields.One2many(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')

class AccountAnalyticTag(models.Model):
    _name = 'account.analytic.tag'
    _inherit = ['account.analytic.tag', 'mail.thread']   
    
    name = fields.Char(track_visibility='onchange')
    active_analytic_distribution = fields.Boolean(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    analytic_distribution_ids = fields.One2many(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')


class AccountAnalyticGroup(models.Model):
    _name = 'account.analytic.group'
    _inherit = ['account.analytic.group', 'mail.thread']

    name = fields.Char(track_visibility='onchange')
    parent_id = fields.Many2one(track_visibility='onchange')
    description = fields.Text(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')


class UomUom(models.Model):
    _name = 'uom.uom'
    _inherit = ['uom.uom', 'mail.thread']

    name = fields.Char(track_visibility='onchange')
    category_id = fields.Many2one(track_visibility='onchange')
    uom_type = fields.Selection([
        ('bigger', 'Bigger than the reference Unit of Measure'),
        ('reference', 'Reference Unit of Measure for this category'),
        ('smaller', 'Smaller than the reference Unit of Measure')], track_visibility='onchange')
    l10n_mx_edi_code_sat_id = fields.Many2one(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    rounding = fields.Float(track_visibility='onchange')


class PaymentAcquirer(models.Model):
    _name = 'payment.acquirer'
    _inherit = ['payment.acquirer', 'mail.thread']

    name = fields.Char(track_visibility='onchange')
    provider = fields.Selection(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    post_msg = fields.Html(track_visibility='onchange')
    pending_msg = fields.Html(track_visibility='onchange')
    journal_id = fields.Many2one(track_visibility='onchange')
    specific_countries = fields.Boolean(track_visibility='onchange')
    qr_code = fields.Boolean(track_visibility='onchange')
    view_template_id = fields.Many2one(track_visibility='onchange')
    registration_view_template_id = fields.Many2one(track_visibility='onchange')
    payment_icon_ids = fields.Many2many(track_visibility='onchange')
    so_reference_type = fields.Selection([
            ('so_name', 'Based on Document Reference'),
            ('partner', 'Based on Customer ID')], track_visibility='onchange')
    image = fields.Binary(track_visibility='onchange')
    website_published = fields.Boolean(track_visibility='onchange')


class PaymentToken(models.Model):
    _name = 'payment.token'
    _inherit = ['payment.token', 'mail.thread']


    name = fields.Char(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    acquirer_id = fields.Many2one(track_visibility='onchange')
    acquirer_ref = fields.Char(track_visibility='onchange')


class PaymentIcon(models.Model):
    _name = 'payment.icon'
    _inherit = ['payment.icon', 'mail.thread']


    name = fields.Char(track_visibility='onchange')
    acquirer_ids = fields.Many2many(track_visibility='onchange')
    image = fields.Binary(track_visibility='onchange')


'''class L10n_mx_ediPaymentMethod(models.Model):
    _name = 'l10n_mx_edi.payment.method'
    _inherit = ['l10n_mx_edi.payment.method', 'mail.thread']


    code = fields.Char(track_visibility='onchange')
    name = fields.Char(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')'''


#===============================================================================================
#===============================================================================================

#================================== Sale module ================================================

class SaleOrder(models.Model):
    _inherit = 'sale.order' 

    partner_id = fields.Many2one(track_visibility='onchange')
    partner_invoice_id = fields.Many2one(track_visibility='onchange')
    partner_shipping_id = fields.Many2one(track_visibility='onchange')
    validity_date = fields.Date(track_visibility='onchange')
    pricelist_id = fields.Many2one(track_visibility='onchange')
    payment_term_id = fields.Many2one(track_visibility='onchange')
    order_line = fields.One2many(track_visibility='onchange')
    note = fields.Text(track_visibility='onchange')
    amount_untaxed = fields.Monetary(track_visibility='onchange')
    amount_tax = fields.Monetary(track_visibility='onchange')
    amount_total = fields.Monetary(track_visibility='onchange')
    sale_order_option_ids = fields.One2many(track_visibility='onchange')
    warehouse_id = fields.Many2one(track_visibility='onchange')
    picking_policy = fields.Selection([
        ('direct', 'Deliver each product when available'),
        ('one', 'Deliver all products at once')], track_visibility='onchange')
    expected_date = fields.Datetime(track_visibility='onchange')
    commitment_date = fields.Datetime(track_visibility='onchange')
    effective_date = fields.Date(track_visibility='onchange')
    date_order = fields.Datetime(track_visibility='onchange')
    fiscal_position_id = fields.Many2one(track_visibility='onchange')
    user_id = fields.Many2one(track_visibility='onchange')
    #tag_ids = fields.Many2many(track_visibility='onchange')
    team_id = fields.Many2one(track_visibility='onchange')
    client_order_ref = fields.Char(track_visibility='onchange')
    require_signature = fields.Boolean(track_visibility='onchange')
    require_payment = fields.Boolean(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    analytic_account_id = fields.Many2one(track_visibility='onchange')
    origin = fields.Char(track_visibility='onchange')
    campaign_id = fields.Many2one(track_visibility='onchange')
    medium_id = fields.Many2one(track_visibility='onchange')
    source_id = fields.Many2one(track_visibility='onchange')
    opportunity_id = fields.Many2one(track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
        ], track_visibility='onchange')


class ResPartner(models.Model):
    _inherit = 'res.partner' 

    company_type = fields.Selection(string='Company Type',
        selection=[('person', 'Individual'), ('company', 'Company')], track_visibility='onchange')
    name = fields.Char(track_visibility='onchange')
    parent_id = fields.Many2one(track_visibility='onchange')
    vat = fields.Char(track_visibility='onchange')
    street = fields.Char(track_visibility='onchange')
    street_number = fields.Char(track_visibility='onchange')
    street_number2 = fields.Char(track_visibility='onchange')
    l10n_mx_edi_colony = fields.Char(track_visibility='onchange')
    l10n_mx_edi_locality = fields.Char(track_visibility='onchange')
    city = fields.Char(track_visibility='onchange')
    state_id = fields.Many2one(track_visibility='onchange')
    zip = fields.Char(track_visibility='onchange')
    country_id = fields.Many2one(track_visibility='onchange')
    l10n_mx_edi_curp = fields.Char(track_visibility='onchange')
    function = fields.Char(track_visibility='onchange')
    phone = fields.Char(track_visibility='onchange')
    mobile = fields.Char(track_visibility='onchange')
    email = fields.Char(track_visibility='onchange')
    website = fields.Char(track_visibility='onchange')
    title = fields.Many2one(track_visibility='onchange')
    category_id = fields.Many2many(track_visibility='onchange')
    child_ids = fields.One2many(track_visibility='onchange')
    comment = fields.Text(track_visibility='onchange')
    customer = fields.Boolean(track_visibility='onchange')
    user_id = fields.Many2one(track_visibility='onchange')
    message_bounce = fields.Integer(track_visibility='onchange')
    property_payment_term_id = fields.Many2one(track_visibility='onchange')
    property_product_pricelist = fields.Many2one(track_visibility='onchange')
    ref = fields.Char(track_visibility='onchange')
    barcode = fields.Char(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    property_stock_customer = fields.Many2one(track_visibility='onchange')
    property_stock_supplier = fields.Many2one(track_visibility='onchange')
    property_supplier_payment_term_id = fields.Many2one(track_visibility='onchange')
    property_purchase_currency_id = fields.Many2one(track_visibility='onchange')
    property_account_position_id = fields.Many2one(track_visibility='onchange')
    bank_ids = fields.One2many(track_visibility='onchange')
    l10n_mx_nationality = fields.Char(track_visibility='onchange')
    l10n_mx_type_of_operation = fields.Selection([
        ('03', ' 03 - Provision of Professional Services'),
        ('06', ' 06 - Renting of buildings'),
        ('85', ' 85 - Others')], track_visibility='onchange')
    property_account_receivable_id = fields.Many2one(track_visibility='onchange')
    property_account_payable_id = fields.Many2one(track_visibility='onchange')
    image = fields.Binary(track_visibility='onchange')
    opportunity_count = fields.Integer(track_visibility='onchange')
    meeting_count = fields.Integer(track_visibility='onchange')
    sale_order_count = fields.Integer(track_visibility='onchange')
    purchase_order_count = fields.Integer(track_visibility='onchange')
    total_invoiced = fields.Monetary(track_visibility='onchange')
    supplier_invoice_count = fields.Integer(track_visibility='onchange')
    partner_ledger_label = fields.Char(track_visibility='onchange')
    contracts_count = fields.Integer(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    
    
class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = ['sale.order.line', 'mail.thread']    
    
    
    display_name = fields.Char(track_visibility='onchange')
    order_partner_id = fields.Many2one(track_visibility='onchange')
    order_id = fields.Many2one(track_visibility='onchange')
    product_id = fields.Many2one(track_visibility='onchange')
    name = fields.Text(track_visibility='onchange')
    product_uom_qty = fields.Float(track_visibility='onchange')
    qty_delivered = fields.Float(track_visibility='onchange')
    qty_invoiced = fields.Float(track_visibility='onchange')
    product_uom = fields.Many2one(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    price_unit = fields.Float(track_visibility='onchange')
    price_subtotal = fields.Monetary(track_visibility='onchange')
    tax_id = fields.Many2many(track_visibility='onchange')
    price_tax = fields.Float(track_visibility='onchange')
    price_total = fields.Monetary(track_visibility='onchange')
    invoice_lines = fields.Many2many(track_visibility='onchange')
    move_ids = fields.One2many(track_visibility='onchange')

class ProductTemplate(models.Model):
    _inherit = 'product.template' 

    name = fields.Char(track_visibility='onchange')
    sale_ok = fields.Boolean(track_visibility='onchange')
    can_be_expensed = fields.Boolean(track_visibility='onchange')
    purchase_ok = fields.Boolean(track_visibility='onchange')
    type = fields.Selection([
        ('consu', 'Consumable'),
        ('service', 'Service'),
        ('product', 'Storable Product')], track_visibility='onchange')
    categ_id = fields.Many2one(track_visibility='onchange')
    default_code = fields.Char(track_visibility='onchange')
    barcode = fields.Char(track_visibility='onchange')
    list_price = fields.Float(track_visibility='onchange')
    taxes_id = fields.Many2many(track_visibility='onchange')
    standard_price = fields.Float(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    uom_id = fields.Many2one(track_visibility='onchange')
    uom_po_id = fields.Many2one(track_visibility='onchange')
    description = fields.Text(track_visibility='onchange')
    available_in_pos = fields.Boolean(track_visibility='onchange')
    invoice_policy = fields.Selection([
        ('order', 'Ordered quantities'),
        ('delivery', 'Delivered quantities')], track_visibility='onchange')
    expense_policy = fields.Selection(
        [('no', 'No'), ('cost', 'At cost'), ('sales_price', 'Sales price')], track_visibility='onchange')
    optional_product_ids = fields.Many2many(track_visibility='onchange')
    description_sale = fields.Text(track_visibility='onchange')
    seller_ids = fields.One2many(track_visibility='onchange')
    purchase_requisition = fields.Selection(
        [('rfq', 'Create a draft purchase order'),
         ('tenders', 'Propose a call for tenders')], track_visibility='onchange')
    valid_price_unit = fields.Boolean(track_visibility='onchange')
    supplier_taxes_id = fields.Many2many(track_visibility='onchange')
    purchase_method = fields.Selection([
        ('purchase', 'On ordered quantities'),
        ('receive', 'On received quantities'),
    ], track_visibility='onchange')
    description_purchase = fields.Text(track_visibility='onchange')
    route_ids = fields.Many2many(track_visibility='onchange')
    produce_delay = fields.Float(track_visibility='onchange')
    sale_delay = fields.Float(track_visibility='onchange')
    property_stock_production = fields.Many2one(track_visibility='onchange')
    property_stock_inventory = fields.Many2one(track_visibility='onchange')
    weight = fields.Float(track_visibility='onchange')
    volume = fields.Float(track_visibility='onchange')
    responsible_id = fields.Many2one(track_visibility='onchange')
    description_pickingout = fields.Text(track_visibility='onchange')
    description_pickingin = fields.Text(track_visibility='onchange')
    description_picking = fields.Text(track_visibility='onchange')
    property_account_income_id = fields.Many2one(track_visibility='onchange')
    property_account_expense_id = fields.Many2one(track_visibility='onchange')
    asset_category_id = fields.Many2one(track_visibility='onchange')
    property_account_creditor_price_difference = fields.Many2one(track_visibility='onchange')
    #l10n_mx_edi_code_sat_id = fields.Many2one(track_visibility='onchange')
    multi_images = fields.One2many(track_visibility='onchange')


class ProductPricelist(models.Model):
    _name = 'product.pricelist'
    _inherit = ['product.pricelist', 'mail.thread']


    name = fields.Char(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    country_group_ids = fields.Many2many(track_visibility='onchange')
    item_ids = fields.One2many(track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')


class CRMTeam(models.Model):
    _inherit = 'crm.team'

    name = fields.Char(track_visibility='onchange')
    use_quotations = fields.Boolean(track_visibility='onchange')
    use_opportunities = fields.Boolean(track_visibility='onchange')
    use_leads = fields.Boolean(track_visibility='onchange')
    team_type = fields.Selection([('sales', 'Sales'), ('website', 'Website'), ('pos', 'Point of Sale')], track_visibility='onchange')
    user_id = fields.Many2one(track_visibility='onchange')
    alias_name = fields.Char(track_visibility='onchange')
    alias_contact = fields.Selection([
        ('everyone', 'Everyone'),
        ('partners', 'Authenticated Partners'),
        ('followers', 'Followers only'),
        ('employees', 'Authenticated Employees')], track_visibility='onchange')
    member_ids = fields.One2many(track_visibility='onchange')
    use_invoices = fields.Boolean(track_visibility='onchange')
    invoiced_target = fields.Integer(track_visibility='onchange')
    dashboard_graph_model = fields.Selection([
        ('sale.report', 'Sales'),
        ('account.invoice.report', 'Invoices'),
        ('crm.lead', 'Pipeline')
    ], track_visibility='onchange')
    dashboard_graph_period_pipeline = fields.Selection([
        ('week', 'Within a Week'),
        ('month', 'Within a Month'),
        ('year', 'Within a Year'),
    ], track_visibility='onchange')
    dashboard_graph_group_pipeline = fields.Selection([
        ('day', 'Expected Closing Day'),
        ('week', 'Expected Closing Week'),
        ('month', 'Expected Closing Month'),
        ('user', 'Salesperson'),
        ('stage', 'Stage'),
    ], track_visibility='onchange')
    active = fields.Boolean(track_visibility='onchange')
    dashboard_graph_period = fields.Selection([
        ('week', 'Last Week'),
        ('month', 'Last Month'),
        ('year', 'Last Year'),
    ], track_visibility='onchange')
    dashboard_graph_group = fields.Selection([
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('user', 'Salesperson'),
    ], track_visibility='onchange')
    dashboard_graph_group_pos = fields.Selection([
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month'),
        ('user', 'Salesperson'),
        ('pos', 'Point of Sale'),
    ], track_visibility='onchange')


class UomCategory(models.Model):
    _name = 'uom.category'
    _inherit = ['uom.category', 'mail.thread']
    
    name = fields.Char(track_visibility='onchange')
    is_pos_groupable = fields.Boolean(track_visibility='onchange')
    measure_type = fields.Selection([
        ('unit', 'Units'),
        ('weight', 'Weight'),
        ('time', 'Time'),
        ('length', 'Length'),
        ('volume', 'Volume'),
    ], track_visibility='onchange')


class MailActivityType(models.Model):
    _name = 'mail.activity.type'
    _inherit = ['mail.activity.type', 'mail.thread']

    name = fields.Char(track_visibility='onchange')
    category = fields.Selection([('default', 'Other'), ('meeting', 'Meeting')], track_visibility='onchange')
    res_model_id = fields.Many2one(track_visibility='onchange')
    summary = fields.Char(track_visibility='onchange')
    icon = fields.Char(track_visibility='onchange')
    decoration_type = fields.Selection([
        ('warning', 'Alert'),
        ('danger', 'Error')], track_visibility='onchange')
    delay_count = fields.Integer(track_visibility='onchange')
    delay_unit = fields.Selection([
        ('days', 'days'),
        ('weeks', 'weeks'),
        ('months', 'months')], track_visibility='onchange')
    delay_from = fields.Selection([
        ('current_date', 'after validation date'),
        ('previous_activity', 'after previous activity deadline')], track_visibility='onchange')
    force_next = fields.Boolean(track_visibility='onchange')
    default_next_type_id = fields.Many2one(track_visibility='onchange')
    next_type_ids = fields.Many2many(track_visibility='onchange')
    mail_template_ids = fields.Many2many(track_visibility='onchange')


#===================================================================================================
#===================================================================================================

#================================== Purchase module ================================================

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    name = fields.Char(track_visibility='onchange')
    partner_ref = fields.Char(track_visibility='onchange')
    requisition_id = fields.Many2one(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    date_order = fields.Datetime(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    order_line = fields.One2many(track_visibility='onchange')
    notes = fields.Text(track_visibility='onchange')
    amount_untaxed = fields.Monetary(track_visibility='onchange')
    amount_tax = fields.Monetary(track_visibility='onchange')
    amount_total = fields.Monetary(track_visibility='onchange')
    date_planned = fields.Datetime(track_visibility='onchange')
    picking_type_id = fields.Many2one(track_visibility='onchange')
    incoterm_id = fields.Many2one(track_visibility='onchange')
    user_id = fields.Many2one(track_visibility='onchange')
    invoice_status = fields.Selection([
        ('no', 'Nothing to Bill'),
        ('to invoice', 'Waiting Bills'),
        ('invoiced', 'No Bill to Receive'),
    ], track_visibility='onchange')
    payment_term_id = fields.Many2one(track_visibility='onchange')
    fiscal_position_id = fields.Many2one(track_visibility='onchange')
    date_approve = fields.Date(track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], track_visibility='onchange')
    picking_count = fields.Integer(track_visibility='onchange')


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'


    name = fields.Char(track_visibility='onchange')
    user_id = fields.Many2one(track_visibility='onchange')
    type_id = fields.Many2one(track_visibility='onchange')
    vendor_id = fields.Many2one(track_visibility='onchange')
    currency_id = fields.Many2one(track_visibility='onchange')
    date_end = fields.Datetime(track_visibility='onchange')
    ordering_date = fields.Date(track_visibility='onchange')
    schedule_date = fields.Date(track_visibility='onchange')
    origin = fields.Char(track_visibility='onchange')
    picking_type_id = fields.Many2one(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    line_ids = fields.One2many(track_visibility='onchange')
    description = fields.Text(track_visibility='onchange')
    state = fields.Selection([
    ('draft', 'Draft'),
    ('ongoing', 'Ongoing'),
    ('in_progress', 'Confirmed'),
    ('open', 'Bid Selection'),
    ('done', 'Closed'),
    ('cancel', 'Cancelled')], track_visibility='onchange')


class ProductSupplierInfo(models.Model):
    _name = 'product.supplierinfo'
    _inherit = ['product.supplierinfo', 'mail.thread']


    name = fields.Many2one(track_visibility='onchange')
    product_name = fields.Char(track_visibility='onchange')
    product_code = fields.Char(track_visibility='onchange')
    delay = fields.Integer(track_visibility='onchange')
    product_tmpl_id = fields.Many2one(track_visibility='onchange')
    min_qty = fields.Float(track_visibility='onchange')
    price = fields.Float(track_visibility='onchange')
    curency_id = fields.Many2one(track_visibility='onchange')
    date_start = fields.Date(track_visibility='onchange')
    date_end = fields.Date(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')


class PurchaseOrderLine(models.Model):
    _name = 'purchase.order.line'
    _inherit = ['purchase.order.line', 'mail.thread']

    order_id = fields.Many2one(track_visibility='onchange')
    date_order = fields.Datetime(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    product_id = fields.Many2one(track_visibility='onchange')
    product_qty = fields.Float(track_visibility='onchange')
    qty_received = fields.Float(track_visibility='onchange')
    qty_invoiced = fields.Float(track_visibility='onchange')
    price_unit = fields.Float(track_visibility='onchange')
    name = fields.Text(track_visibility='onchange')
    taxes_id = fields.Many2many(track_visibility='onchange')
    date_planned = fields.Datetime(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    account_analytic_id = fields.Many2one(track_visibility='onchange')
    invoice_lines = fields.One2many(track_visibility='onchange')
    move_ids = fields.One2many(track_visibility='onchange')


class StockMove(models.Model):
    _name = 'stock.move'
    _inherit = ['stock.move', 'mail.thread']


    reference = fields.Char(track_visibility='onchange')
    location_id = fields.Many2one(track_visibility='onchange')
    location_dest_id = fields.Many2one(track_visibility='onchange')
    product_id = fields.Many2one(track_visibility='onchange')
    product_uom_qty = fields.Float(track_visibility='onchange')
    product_uom = fields.Many2one(track_visibility='onchange')
    origin = fields.Char(track_visibility='onchange')
    group_id = fields.Many2one(track_visibility='onchange')
    procure_method = fields.Selection([
        ('make_to_stock', 'Default: Take From Stock'),
        ('make_to_order', 'Advanced: Apply Procurement Rules')], track_visibility='onchange')
    purchase_line_id = fields.Many2one(track_visibility='onchange')
    move_orig_ids = fields.Many2many(track_visibility='onchange')
    move_dest_ids = fields.Many2many(track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'New'), ('cancel', 'Cancelled'),
        ('cancel', 'Cancelled'),
        ('waiting', 'Waiting Another Move'),
        ('confirmed', 'Waiting Availability'),
        ('partially_available', 'Partially Available'),
        ('assigned', 'Available'),
        ('done', 'Done')], track_visibility='onchange')


class PurchaseRequisitionType(models.Model):
    _name = 'purchase.requisition.type'
    _inherit = ['purchase.requisition.type', 'mail.thread']

    name = fields.Char(track_visibility='onchange')
    exclusive = fields.Selection([
        ('exclusive', 'Select only one RFQ (exclusive)'), ('multiple', 'Select multiple RFQ')], track_visibility='onchange')
    line_copy = fields.Selection([
        ('copy', 'Use lines of agreement'), ('none', 'Do not create RfQ lines automatically')], track_visibility='onchange')
    quantity_copy = fields.Selection([
        ('copy', 'Use quantities of agreement'), ('none', 'Set quantities manually')], track_visibility='onchange')
    

class StockPicking(models.Model):
    _inherit = 'stock.picking'
    
    partner_id = fields.Many2one(track_visibility='onchange')
    picking_type_id = fields.Many2one(track_visibility='onchange')
    location_id = fields.Many2one(track_visibility='onchange')
    location_dest_id = fields.Many2one(track_visibility='onchange')
    x_studio_aplica_flete = fields.Boolean(track_visibility='onchange')
    schedule_date = fields.Datetime(track_visibility='onchange')
    origin = fields.Char(track_visibility='onchange')
    move_ids_without_package = fields.One2many(track_visibility='onchange')
    move_type = fields.Selection([
        ('direct', 'As soon as possible'), ('one', 'When all products are ready')], track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    group_id = fields.Many2one(track_visibility='onchange')
    note = fields.Text(track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], track_visibility='onchange')


class StockInventory(models.Model):
    _name = 'stock.inventory'
    _inherit = ['stock.inventory', 'mail.thread']

    name = fields.Char(track_visibility='onchange')
    location_id = fields.Many2one(track_visibility='onchange')
    filter = fields.Selection([
            ('none', 'All products'),
            ('category', 'One product category'),
            ('product', 'One product only'),
            ('partial', 'Select products manually')], track_visibility='onchange')
    date = fields.Datetime(track_visibility='onchange')
    accounting_date = fields.Date(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    exhausted = fields.Boolean(track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('cancel', 'Cancelled'),
        ('confirm', 'In Progress'),
        ('done', 'Validated')], track_visibility='onchange')
    
    
#===================================================================================================
#===================================================================================================

#================================== INVENTORY Module ===============================================

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    partner_id = fields.Many2one(track_visibility='onchange')
    picking_type_id = fields.Many2one(track_visibility='onchange')
    location_dest_id = fields.Many2one(track_visibility='onchange')
    x_studio_aplica_flete = fields.Boolean(track_visibility='onchange')
    scheduled_date = fields.Datetime(track_visibility='onchange')
    date_done = fields.Datetime(track_visibility='onchange')
    origin = fields.Char(track_visibility='onchange')
    reciba_id = fields.Many2one(track_visibility='onchange')
    move_ids_without_package = fields.Many2many(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    group_id = fields.Many2one(track_visibility='onchange')
    note = fields.Text(track_visibility='onchange')



class StockInventory(models.Model):
    _inherit = ['stock.inventory', 'mail.thread']

    #See a more detailed inheritance in 2 stanzas above with all fields already defined
    line_ids = fields.One2many(track_visibility='onchange')
    move_ids = fields.One2many(track_visibility='onchange')



class StockScrap(models.Model):
    _inherit = ['stock.scrap', 'mail.thread']

    name = fields.Char(track_visibility='onchange')
    product_id = fields.Many2one(track_visibility='onchange')
    scrap_qty = fields.Float(track_visibility='onchange')
    product_uom_id = fields.Many2one(track_visibility='onchange')
    location_id = fields.Many2one(track_visibility='onchange')
    scrap_location_id = fields.Many2one(track_visibility='onchange')
    origin = fields.Char(track_visibility='onchange')
    date_expected = fields.Datetime(track_visibility='onchange')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done')], string='Status', default="draft", track_visibility='onchange')



class ProductTemplate(models.Model):
    _inherit = 'product.template' 

    #In "Sales Module" is already and more completely defined all fields of this view
    email_template_id = fields.Many2one(track_visibility='onchange')



class StockWarehouseOrderpoint(models.Model):
    _inherit = ['stock.warehouse.orderpoint', 'mail.thread']

    name = fields.Char(track_visibility='onchange')
    product_id = fields.Many2one(track_visibility='onchange')
    product_id = fields.Many2one(track_visibility='onchange')
    warehouse_id = fields.Many2one(track_visibility='onchange')
    product_uom = fields.Many2one(track_visibility='onchange')
    location_id = fields.Many2one(track_visibility='onchange')
    group_id = fields.Many2one(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    product_min_qty = fields.Float(track_visibility='onchange')
    product_max_qty = fields.Float(track_visibility='onchange')
    qty_multiple = fields.Float(track_visibility='onchange')
    lead_type = fields.Integer(track_visibility='onchange')
    lead_type = fields.Selection(
        [('net', 'Day(s) to get the products'), 
         ('supplier', 'Day(s) to purchase')], 
        'Lead Type',
        required=True, default='supplier', track_visibility='onchange')    



class StockMove(models.Model):
    _inherit = ['stock.move', 'mail.thread']

    #In "Purchase Module" is already and more completely defined all fields of this view
    date = fields.Datetime(track_visibility='onchange')



class StockMoveLine(models.Model):
    _inherit = ['stock.move.line', 'mail.thread']

    date = fields.Datetime(track_visibility='onchange')
    reference = fields.Char(track_visibility='onchange')
    picking_id = fields.Many2one(track_visibility='onchange')
    product_id = fields.Many2one(track_visibility='onchange')
    location_id = fields.Many2one(track_visibility='onchange')
    location_dest_id = fields.Many2one(track_visibility='onchange')
    x_studio_asiento_contable = fields.Many2one(track_visibility='onchange')
    x_studio_fecha_contable = fields.Date(track_visibility='onchange')
    x_studio_tipo_de_operacion_descripcion = ields.Char(track_visibility='onchange')
    qty_done = fields.Float(track_visibility='onchange')
    product_uom_id = fields.Many2one(track_visibility='onchange')
    state = fields.Selection(related='move_id.state', store=True, related_sudo=False, readonly=False, track_visibility='onchange')



class StockWarehouse(models.Model):
    _inherit = ['stock.warehouse', 'mail.thread']

    name = fields.Char(track_visibility='onchange')
    code = fields.Char(track_visibility='onchange')
    lot_stock_id = fields.Many2one(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange')
    reception_steps = fields.Selection([
        ('one_step', 'Receive goods directly (1 step)'),
        ('two_steps', 'Receive goods in input and then stock (2 steps)'),
        ('three_steps', 'Receive goods in input, then quality and then stock (3 steps)')],
        'Incoming Shipments', default='one_step', required=True,
        help="Default incoming route to follow", track_visibility='onchange')
    delivery_steps = fields.Selection([
        ('ship_only', 'Deliver goods directly (1 step)'),
        ('pick_ship', 'Send goods in output and then deliver (2 steps)'),
        ('pick_pack_ship', 'Pack goods, send goods in output and then deliver (3 steps)')],
        'Outgoing Shipments', default='ship_only', required=True,
        help="Default outgoing route to follow", track_visibility='onchange')  
    buy_to_resupply = fields.Boolean(track_visibility='onchange')
    manufacture_to_resupply = fields.Boolean(track_visibility='onchange')        
    manufacture_steps = fields.Selection([
        ('mrp_one_step', 'Manufacture (1 step)'),
        ('pbm', 'Pick components and then manufacture (2 steps)'),
        ('pbm_sam', 'Pick components, manufacture and then store products (3 steps)')],
        'Manufacture', default='mrp_one_step', required=True,
        help="Produce : Move the raw materials to the production location\
        directly and start the manufacturing process.\nPick / Produce : Unload\
        the raw materials from the Stock to Input location first, and then\
        transfer it to the Production location.", track_visibility='onchange')
    resupply_wh_ids = fields.Many2many(track_visibility='onchange')    
    wh_input_stock_loc_id = fields.Many2one(track_visibility='onchange')
    wh_qc_stock_loc_id = fields.Many2one(track_visibility='onchange')
    wh_pack_stock_loc_id = fields.Many2one(track_visibility='onchange')        
    wh_output_stock_loc_id = fields.Many2one(track_visibility='onchange')
    sam_loc_id = fields.Many2one(track_visibility='onchange')
    pbm_loc_id = fields.Many2one(track_visibility='onchange')
    in_type_id = fields.Many2one(track_visibility='onchange')
    int_type_id = fields.Many2one(track_visibility='onchange')
    pick_type_id = fields.Many2one(track_visibility='onchange')
    pack_type_id = fields.Many2one(track_visibility='onchange')
    out_type_id = fields.Many2one(track_visibility='onchange')
    sam_type_id = fields.Many2one(track_visibility='onchange')           
    pbm_type_id = fields.Many2one(track_visibility='onchange')           
    manu_type_id = fields.Many2one(track_visibility='onchange')   



class StockLocation(models.Model):
    _inherit = ['stock.location', 'mail.thread']  

    name = fields.Char(track_visibility='onchange')
    location_id = fields.Many2one(track_visibility='onchange') 
    usage = fields.Selection([
        ('supplier', 'Vendor Location'),
        ('view', 'View'),
        ('internal', 'Internal Location'),
        ('customer', 'Customer Location'),
        ('inventory', 'Inventory Loss'),
        ('procurement', 'Procurement'),
        ('production', 'Production'),
        ('transit', 'Transit Location')], string='Location Type',
        default='internal', index=True, required=True,
        help="* Vendor Location: Virtual location representing the source location for products coming from your vendors"
             "\n* View: Virtual location used to create a hierarchical structures for your warehouse, aggregating its child locations ; can't directly contain products"
             "\n* Internal Location: Physical locations inside your own warehouses,"
             "\n* Customer Location: Virtual location representing the destination location for products sent to your customers"
             "\n* Inventory Loss: Virtual location serving as counterpart for inventory operations used to correct stock levels (Physical inventories)"
             "\n* Procurement: Virtual location serving as temporary counterpart for procurement operations when the source (vendor or production) is not known yet. This location should be empty when the procurement scheduler has finished running."
             "\n* Production: Virtual counterpart location for production operations: this location consumes the raw material and produces finished products"
             "\n* Transit Location: Counterpart location that should be used in inter-company or inter-warehouses operations",
        track_visibility='onchange')
    allow_negative_stock = fields.Boolean(track_visibility='onchange')
    partner_id = fields.Many2one(track_visibility='onchange') 
    company_id = fields.Many2one(track_visibility='onchange') 
    scrap_location = fields.Boolean(track_visibility='onchange')
    return_location = fields.Boolean(track_visibility='onchange')
    removal_strategy_id = fields.Many2one(track_visibility='onchange') 
    putaway_strategy_id = fields.Many2one(track_visibility='onchange')
    posx = fields.Integer(track_visibility='onchange')
    posy = fields.Integer(track_visibility='onchange')
    posz = fields.Integer(track_visibility='onchange')
    barcode = fields.Char(track_visibility='onchange')
    comment = fields.Text(track_visibility='onchange')



class StockRule(models.Model):
    _inherit = ['stock.rule', 'mail.thread'] 

    name = fields.Char(track_visibility='onchange')
    action = fields.Selection(
        selection=[('pull', 'Pull From'), 
                   ('push', 'Push To'), 
                   ('pull_push', 'Pull & Push')], string='Action',
        required=True, track_visibility='onchange')
    picking_type_id = fields.Many2one(track_visibility='onchange')
    location_src_id = fields.Many2one(track_visibility='onchange')
    location_id = fields.Many2one(track_visibility='onchange')
    procure_method = fields.Selection([
        ('make_to_stock', 'Take From Stock'),
        ('make_to_order', 'Trigger Another Rule')], string='Move Supply Method',
        default='make_to_stock', required=True,
        help="""Create Procurement: A procurement will be created in the source location and the system will try to find a rule to resolve it. The available stock will be ignored.
             Take from Stock: The products will be taken from the available stock.""",
        track_visibility='onchange')   
    route_id = fields.Many2one(track_visibility='onchange')
    warehouse_id = fields.Many2one(track_visibility='onchange')
    company_id = fields.Many2one(track_visibility='onchange')     
    sequence = fields.Integer(track_visibility='onchange')
    group_propagation_option = fields.Selection([
        ('none', 'Leave Empty'),
        ('propagate', 'Propagate'),
        ('fixed', 'Fixed')], string="Propagation of Procurement Group", default='propagate',
        track_visibility='onchange')      
    propagate = fields.Boolean(track_visibility='onchange')   
    propagate_warehouse_id = fields.Many2one(track_visibility='onchange')
    partner_address_id = fields.Many2one(track_visibility='onchange')
    delay = fields.Integer(track_visibility='onchange')



class StockLocationRoute(models.Model):
    _inherit = ['stock.location.route', 'mail.thread'] 

    name = fields.Char(track_visibility='onchange') 
    sequence = fields.Integer(track_visibility='onchange')   
    company_id = fields.Many2one(track_visibility='onchange')  
    product_categ_selectable = fields.Boolean(track_visibility='onchange')  
    product_selectable = fields.Boolean(track_visibility='onchange')  
    warehouse_selectable = fields.Boolean(track_visibility='onchange') 
    warehouse_ids = fields.Many2many(track_visibility='onchange')
    sale_selectable = fields.Boolean(track_visibility='onchange') 
    rule_ids = fields.One2many(track_visibility='onchange')



class StockPickingType(models.Model):
    _inherit = ['stock.picking.type', 'mail.thread'] 

    name = fields.Char(track_visibility='onchange') 
    sequence_id = fields.Many2one(track_visibility='onchange') 
    warehouse_id = fields.Many2one(track_visibility='onchange') 
    barcode = fields.Char(track_visibility='onchange')
    code = fields.Selection([('incoming', 'Vendors'), 
                             ('outgoing', 'Customers'), 
                             ('internal', 'Internal')], 
                            'Type of Operation', required=True,
                            track_visibility='onchange')
    return_picking_type_id = fields.Many2one(track_visibility='onchange')
    show_operations = fields.Boolean(track_visibility='onchange')
    show_reserved = fields.Boolean(track_visibility='onchange')
    default_location_src_id = fields.Many2one(track_visibility='onchange')
    default_location_dest_id = fields.Many2one(track_visibility='onchange')



class ProductCategory(models.Model):
    _inherit = ['product.category', 'mail.thread']

    #In "ACCOUNTING Module" is already and more completely defined all fields of this view
    allow_negative_stock = fields.Boolean(track_visibility='onchange')



#Values for selection field upc_ean_conv
UPC_EAN_CONVERSIONS = [
    ('none','Never'),
    ('ean2upc','EAN-13 to UPC-A'),
    ('upc2ean','UPC-A to EAN-13'),
    ('always','Always'),
]
class BarcodeNomenclature(models.Model):
    _inherit = ['barcode.nomenclature', 'mail.thread']

    name = fields.Char(track_visibility='onchange') 
    upc_ean_conv =
    upc_ean_conv = fields.Selection(UPC_EAN_CONVERSIONS, string='UPC/EAN Conversion', required=True, default='always',
        help="UPC Codes can be converted to EAN by prefixing them with a zero. This setting determines if a UPC/EAN barcode should be automatically converted in one way or another when trying to match a rule with the other encoding.",
        track_visibility='onchange')
    rule_ids = fields.One2many(track_visibility='onchange')



#class UomCategory(models.Model):
#    _inherit = ['uom.category', 'mail.thread']

    #In "SALES Module" is already and more completely defined all fields of this view    



#class UomUom(models.Model):
#    _inherit = ['uom.uom', 'mail.thread']

    #In "ACCOUNTING Module" is already and more completely defined all fields of this view  
