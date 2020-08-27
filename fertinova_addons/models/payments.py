# -*- coding: utf-8 -*-
from odoo import models, fields, api

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 035    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    cta_diario_pago = fields.Char(string='Cuenta Diario Pago')
    factura = fields.Many2one('account.invoice', 
                              string = 'Factura',
                              domain = [('partner_id', '=', self.partner_id.id),
                                        ('state', 'not in', ['paid', 'cancel'])])
    compra = fields.Many2one('purchase.order', 
                              string = 'Orden de Compra',
                              domain = [('partner_id', '=', self.partner_id.id),
                                        ('state', 'not in', ['done', 'cancel'])])
