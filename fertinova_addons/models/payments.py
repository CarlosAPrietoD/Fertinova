# -*- coding: utf-8 -*-
from odoo import models, fields, api

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 164    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    bank_account_id = fields.Many2many('res.partner.bank', string='Cuenta Diario Pago', compute='_compute_bank_account')
    invoices_id     = fields.Many2many('account.invoice', string='Factura', compute='_set_invoices')
    purchases_id    = fields.Many2many('purchase.order', string='Orden de Compra', compute='_set_purchases')
    

    @api.depends('journal_id')
    def _compute_bank_account(self):
        self.bank_account_id = self.env['account.journal'].search([('id', '=', self.journal_id)]).bank_account_id
        
        
    def _set_invoices(self):
        domain=[('partner_id', '=', self.partner_id.ids), 
                ('state', 'not in', ['paid', 'cancel'])]
        self.invoices_id = self.env['account.invoice'].search(domain)
        
        
    def _set_purchases(self):
        domain = [('partner_id', '=', self.partner_id.ids), 
                  ('state', 'not in', ['done', 'cancel'])]
        self.purchases_id = self.env['purchase.order'].search(domain)
