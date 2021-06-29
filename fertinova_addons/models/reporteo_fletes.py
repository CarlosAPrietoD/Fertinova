# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

# /////////////////////////////////////////////////////////////////////////////
#
#   Development to create a new PDF report from Odoo Studio View 
#   "Líneas de Pedido de Ventas" where also it was necessary add
#   new custom fields.
#
#   Also it was created a new Report {List View} and PDF for Management
#   of Fleets (with new custom fields too)
#
# /////////////////////////////////////////////////////////////////////////////

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    operador = fields.Char(string='Operador')
    placas   = fields.Char(string='Placas')




class StockMove(models.Model):
    _inherit = 'stock.move'
    
    operador = fields.Char(string='Operador', compute='_set_operador')
    placas   = fields.Char(string='Placas', compute='_set_placas')    
    importe  = fields.Float(string='Importe', digits=(20, 2), compute='_set_importe')


    @api.one
    def _set_operador(self):
        self.operador = self.env['stock.picking'].search([('id', '=', self.picking_id.id)]).operador        


    @api.one
    def _set_placas(self):
        self.placas = self.env['stock.picking'].search([('id', '=', self.picking_id.id)]).placas


    @api.one
    def _set_importe(self):
        precio_unitario = self.env['sale.order.line'].search([('id', '=', self.sale_line_id.id)]).price_unit         
        self.importe = self.quantity_done * precio_unitario




class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    credit_notes_ids = fields.Many2many('account.invoice.line', string='Notas de crédito', compute='_set_credit_notes')

    @api.one
    def _set_credit_notes(self):
        #Get invoices to check up
        list_inv_ids = []
        _logger.info('\n\n\n invoice_lines: %s\n\n\n', self.invoice_lines)
        
        for ln in self.invoices_lines:
            _logger.info('\n\n\n ln - invoice_id: %s\n\n\n', ln.invoice_id)
            list_inv_ids.append(ln.invoice_id)
        _logger.info('\n\n\n list_inv_ids: %s\n\n\n', list_inv_ids)

        #Get credit notes
        ids_credit_notes = self.env['account.invoice'].search([('refund_invoice_id', 'in', list_inv_ids)])                    
        _logger.info('\n\n\n ids_credit_notes: %s\n\n\n', ids_credit_notes)

        ids_lns_credit_notes = self.env['account.invoice.line'].search([('invoice_id', 'in', ids_credit_notes)])
        
        self.credit_notes_ids = ids_lns_credit_notes.ids




class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    ids_factura_origen_credito = fields.Integer(string='Factura Origen IDs', related='invoice_id.refund_invoice_id.id')
    factura_origen_credito     = fields.Char(string='Factura Origen', related='invoice_id.refund_invoice_id.number')
