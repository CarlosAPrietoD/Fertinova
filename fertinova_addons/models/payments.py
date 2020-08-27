# -*- coding: utf-8 -*-
from odoo import models, fields, api

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 164    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    bank_account_id = fields.Many2one('res.partner.bank', string='Cuenta Diario Pago', compute='_compute_bank_account')
    invoices_id     = fields.Many2one('account.invoice', string='Factura', domain=_set_invoices)
    purchases_id    = fields.Many2one('purchase.order', string='Orden de Compra', domain=_set_purchases)
    

    @api.depends('journal_id')
    def _compute_bank_account(self):
        self.bank_account_id = self.env['account.journal'].search([('id', '=', self.journal_id.id)]).bank_account_id.id
        
        
    def _set_invoices(self):
        domain=[('partner_id', '=', self.partner_id.id), 
                ('state', 'not in', ['paid', 'cancel'])]
        return domain
        
        
    def _set_purchases(self):
        domain = [('partner_id', '=', self.partner_id.id), 
                  ('state', 'not in', ['done', 'cancel'])]
        return domain
