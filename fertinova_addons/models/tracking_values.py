from odoo import models, fields, api

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
    
    
class ProductProduct(models.Model):
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
    image_medium = fields.Binary(track_visibility='onchange')
    
    
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


    '''(track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')
    (track_visibility='onchange')'''
