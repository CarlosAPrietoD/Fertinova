# -*- coding: utf-8 -*-
from odoo import models, fields, api

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 164    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    #             MODEL FIELDS
    #state = fields.Selection(selection_add=[('authorized', 'Autorizado'), ('draft',)])
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('authorized', 'Autorizado'),
        ('posted', 'Posted'),
        ('sent', 'Sent'),
        ('reconciled', 'Reconciled'),
        ('cancelled', 'Cancelled')
        ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')    
    
    bank_account_id = fields.Many2one('res.partner.bank', string='Cuenta Diario Pago', 
                                      compute='_compute_bank_account', readonly=False)
    
    invoices_id     = fields.Many2one('account.invoice', 
                                      string='Factura', readonly=False,
                                      default=lambda self: self.env['account.invoice'].search([('partner_id', '=', self.partner_id.id), 
                                                                                               ('state', 'not in', ['paid', 'cancel'])]))
    
    purchases_id    = fields.Many2one('purchase.order', 
                                      string='Orden de Compra', readonly=False,
                                      default=lambda self: self.env['account.invoice'].search([('partner_id', '=', self.partner_id.id), 
                                                                                               ('state', 'not in', ['done', 'cancel'])]))

    #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    #             METHOD FIELDS
    @api.depends('journal_id')
    def _compute_bank_account(self):
        self.bank_account_id = self.env['account.journal'].search([('id', '=', self.journal_id.id)]).bank_account_id.id
    
    #def change_state_authorized(self):
    #    self.state = 'authorized'
        
    def change_state_authorized(self, cr, uid, ids, context=None):
        res = self.write(cr, uid, ids, {'state': 'authorized'}, context=context)    
        return res        
