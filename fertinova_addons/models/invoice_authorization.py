# -*- coding: utf-8 -*-
from odoo import models, fields, api

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 164    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    #             MODEL FIELDS
    #state_aux = fields.Selection(selection=[
    #    ('draft', 'Draft'),
    #    ('authorized', 'Authorized'),
    #    ('posted', 'Posted'),
    #    ('sent', 'Sent'),
    #    ('reconciled', 'Reconciled'),
    #    ('cancelled', 'Cancelled')
    #    ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')  
    
    bank_account_id = fields.Many2one('res.partner.bank', string='Cuenta Diario Pago', 
                                      compute='_compute_bank_account', store=True, readonly=False)    
    
    invoices_id     = fields.Many2one('account.invoice', 
                                      string='Factura', readonly=False,
                                      default=lambda self: self.env['account.invoice'].search([('partner_id', '=', self.partner_id.id), 
                                                                                               ('state', 'not in', ['paid', 'cancel'])]))    
    purchases_id    = fields.Many2one('purchase.order', 
                                      string='Orden de Compra', readonly=False,
                                      default=lambda self: self.env['purchase.order'].search([('partner_id', '=', self.partner_id.id), 
                                                                                               ('state', 'not in', ['done', 'cancel'])]))
    #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    #             METHOD FIELDS
    @api.one
    @api.depends('journal_id')
    def _compute_bank_account(self):
        self.ensure_one()
        self.bank_account_id = self.env['account.journal'].search([('id', '=', self.journal_id.id)]).bank_account_id.id
    
    """    
    def change_state_authorized(self):
        #Modify state to Authorized
        values = {'state_aux': 'authorized'}
        self.write(values) 
        
        #Construction of post message's content in Payments:
        uid = self.env.user.id
        name_user = self.env['res.users'].search([('id', '=', uid)]).name

        payment_post =  "<ul style=\"margin:0px 0 9px 0\">"
        payment_post += "<li><p style='margin:0px; font-size:13px; font-family:\"Lucida Grande\", Helvetica, Verdana, Arial, sans-serif'>Usuario que autorizó el pago: <strong>" + name_user + "</strong></p></li>"
        payment_post += "<li><p style='margin:0px; font-size:13px; font-family:\"Lucida Grande\", Helvetica, Verdana, Arial, sans-serif'>Estado: <strong>AUTORIZADO</strong></p></li>"
        payment_post += "</ul>"

        payment_order_recorset = self.env['account.payment'].browse(self.id)
        payment_order_recorset.message_post(body=payment_post)  

    @api.multi
    def post(self):
        payment = super(AccountPayment, self).post()
        for rec in self:   
            rec.state_aux = 'posted'
        return payment   

    @api.multi
    def cancel(self):
        payment = super(AccountPayment, self).cancel()
        for rec in self:
            rec.state_aux = 'cancelled'
        return payment  

    @api.multi
    def action_draft(self):
        payment = super(AccountPayment, self).action_draft()
        self.write({'state_aux': 'draft'})  
        return payment 
    """

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'    

    state = fields.Selection([
            ('draft','Draft'),
            ('authorized', 'Authorized'),
            ('open', 'Open'),
            ('in_payment', 'In Payment'),
            ('paid', 'Paid'),
            ('cancel', 'Cancelled'),
        ], string='Status', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        help=" * The 'Draft' status is used when a user is encoding a new and unconfirmed Invoice.\n"
             " * The 'Authorized' status is used as a part of customization for authorizing Invoices before continue general process.\n"
             " * The 'Open' status is used when user creates invoice, an invoice number is generated. It stays in the open status till the user pays the invoice.\n"
             " * The 'In Payment' status is used when payments have been registered for the entirety of the invoice in a journal configured to post entries at bank reconciliation only, and some of them haven't been reconciled with a bank statement line yet.\n"
             " * The 'Paid' status is set automatically when the invoice is paid. Its related journal entries may or may not be reconciled.\n"
             " * The 'Cancelled' status is used when user cancel invoice.")

    def change_state_authorized(self):
        #Modify state to Authorized
        values = {'state': 'authorized'}
        self.write(values) 

        self.state = 'authorized'
        
        #Construction of post message's content in Payments:
        uid = self.env.user.id
        name_user = self.env['res.users'].search([('id', '=', uid)]).name

        invoice_post =  "<ul style=\"margin:0px 0 9px 0\">"
        invoice_post += "<li><p style='margin:0px; font-size:13px; font-family:\"Lucida Grande\", Helvetica, Verdana, Arial, sans-serif'>Usuario que autorizó la factura: <strong>" + name_user + "</strong></p></li>"
        invoice_post += "<li><p style='margin:0px; font-size:13px; font-family:\"Lucida Grande\", Helvetica, Verdana, Arial, sans-serif'>Estado: <strong>AUTORIZADO</strong></p></li>"
        invoice_post += "</ul>"

        invoice_order_recorset = self.env['account.invoice'].browse(self.id)
        invoice_order_recorset.message_post(body=invoice_post)    

    @api.multi
    def action_invoice_open(self):
        for rec in self:
            if rec.state == 'authorized':
                rec.state = 'draft' 
        invoice = super(AccountInvoice, self).action_invoice_open()        
        return invoice 