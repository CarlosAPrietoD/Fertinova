# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api

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
        self.credit_notes_ids = self.env['account.invoice'].search([('id', 'in', self.invoice_lines.ids)]).ids         
