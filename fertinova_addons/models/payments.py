# -*- coding: utf-8 -*-
from odoo import models, fields, api

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 164    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    #             MODEL FIELDS
    state_aux = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('authorized', 'Authorized'),
        ('posted', 'Posted'),
        ('sent', 'Sent'),
        ('reconciled', 'Reconciled'),
        ('cancelled', 'Cancelled')
        ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')  
    
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