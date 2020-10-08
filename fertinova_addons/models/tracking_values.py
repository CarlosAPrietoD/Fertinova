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
    (track_visibility='onchange')'''
