# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api
from openerp.exceptions import ValidationError
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

    #Fields added to Form View of Inventory > Operations > Transfers
    operador = fields.Char(string='Operador')
    placas   = fields.Char(string='Placas')
    folio_peso_tk = fields.Char(string='Folio Peso Ticket')                                                                                             





class StockMove(models.Model):
    _inherit = 'stock.move'
    
    #Fields added to one2many field of Stock Moves in Form View 
    # of Sales > To Incoice > Lineas de Pedido {Odoo Studio}
    operador = fields.Char(string='Operador', compute='_set_operador')
    placas   = fields.Char(string='Placas', compute='_set_placas')    
    importe  = fields.Float(string='Importe', digits=(20, 2), compute='_set_importe')
    #Revisar su correcta asignación dado que se puso en una vista de Odoo Studio |
    #de "Líneas de Pedido de Venta"                                              |
    folio_peso_tk = fields.Char(string='Folio Peso Ticket')#                     |
    #----------------------------------------------------------------------------|

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





class StockQuant(models.Model):
    _inherit = 'stock.quant'

    #Field added to List View of Inventory > Reporting > Inventory Report
    cant_disponible = fields.Float(string='Cantidad Disponible', digits=(20, 2), compute='_set_cant_disponible', store=True)

    @api.one
    def _set_cant_disponible(self):           
        self.cant_disponible = self.quantity - self.reserved_quantity         





class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #Field added to display credit notes in Form View 
    # of Sales > To Incoice > Lineas de Pedido {Odoo Studio}
    credit_notes_ids = fields.Many2many('account.invoice.line', string='Notas de crédito', compute='_set_credit_notes')

    @api.one
    def _set_credit_notes(self):
        #Get invoices to check up
        list_inv_ids = []
        
        for ln in self.invoice_lines:
            list_inv_ids.append(ln.invoice_id.id)

        #Get credit notes
        ids_credit_notes = self.env['account.invoice'].search([('refund_invoice_id', 'in', list_inv_ids)])                    
        ids_lns_credit_notes = self.env['account.invoice.line'].search([('invoice_id', 'in', ids_credit_notes.ids)])
        
        #Assign to field retrieved credit notes
        self.credit_notes_ids = ids_lns_credit_notes.ids





class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    #Field added to one2many field of Credit Notes in Form View 
    # of Sales > To Incoice > Lineas de Pedido {Odoo Studio}
    factura_origen_credito = fields.Char(string='Factura Origen', related='invoice_id.refund_invoice_id.number')





class WobinServiceOrder(models.Model):
    _name = 'wobin.service.order'
    _description = 'Wobin Service Order'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    @api.model
    def create(self, vals):  
        """This method intends to create a sequence for a given Service Order"""            
        #Change of sequence (if it isn't stored is shown "New" else e.g ORD000001) 
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code(
                'self.orden_servicio') or 'New'
            vals['name'] = sequence     
            res = super(WobinServiceOrder, self).create(vals)  

        return res      


    name         = fields.Char(string="Orden de Servicio", readonly=True, required=True, copy=False, default='New')
    partner_id   = fields.Many2one('res.partner', string='Proveedor')
    estado       = fields.Selection([('no_asignada', 'No Asignada'),
                                     ('asignada', 'Asignada'),                                     
                                     ('cancelada', 'Cancelada')
                                    ], string='Estado', default='no_asignada', compute='_set_estado_asignada', store=True)
    check_cancel = fields.Boolean()                                    
                                   
    pickings_ids = fields.One2many('wobin.service.order.line', 'wbn_service_order_id', string='Control de Albaranes')
    purchase_with_order_id = fields.Many2one('purchase.order', string='Orden de Compra')
    

    def cancelar_orden(self):
        self.check_cancel = True
        self.estado = 'cancelada'


    @api.one
    @api.depends('purchase_with_order_id')
    def _set_estado_asignada(self):
        if self.purchase_with_order_id and self.check_cancel != True:
            self.estado = 'asignada'
        elif not self.purchase_with_order_id and self.check_cancel != True:
            self.estado = 'no_asignada'   
        elif self.check_cancel == True:
            self.estado = 'cancelada'                     





class WobinServiceOrderLine(models.Model):
    _name = 'wobin.service.order.line'
    _description = 'Wobin Service Order Line'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 


    _sql_constraints = [('transferencia_origen', 
                         'unique (transferencia_origen_id)',     
                         'Albaranes duplicados no están permitidos por línea'),
                        ('transferencia_destino', 
                         'unique (transferencia_destino_id)',     
                         'Albaranes duplicados no están permitidos por línea')]

    #General Data:
    wbn_service_order_id     = fields.Many2one('wobin.service.order', string='Orden de Servicio')
    estado_wbn_servi_ord     = fields.Selection([('no_asignada', 'No Asignada'),
                                                 ('asignada', 'Asignada'),                                     
                                                 ('cancelada', 'Cancelada')
                                    ],string='Estado', related='wbn_service_order_id.estado')
    wbn_pur_order_related    = fields.Char(string="Orden de Compra", related='wbn_service_order_id.purchase_with_order_id.name')
                                    
    #Upload Origin Data:
    transferencia_origen_id  = fields.Many2one('stock.picking', string='Movimiento Origen')    
    fecha_carga_origen       = fields.Date(string='Fecha Carga')
    producto_id              = fields.Many2one('product.product', string='Producto', compute='_set_producto_id')
    folio_peso_tk_tr_ori     = fields.Char(string='Folio Peso Ticket', compute='_set_folio_tk_origen')
    kilos_origen             = fields.Float(string='Kg Carga', digits=(20, 2), compute='_set_kilos_origen')
    
    #Discharge Destiny Data:
    transferencia_destino_id = fields.Many2one('stock.picking', string='Movimiento Destino')
    fecha_descarga_destino   = fields.Date(string='Fecha Entrega')
    producto_destino_id      = fields.Many2one('product.product', string='Producto', compute='_set_producto_destino_id')
    folio_peso_tk_tr_dest    = fields.Char(string='Folio Peso Ticket', compute='_set_folio_tk_destino')
    kilos_destino            = fields.Float(string='Kg Entrega', digits=(20, 2), compute='_set_kilos_destino')
    placas                   = fields.Char(string='Placas', compute='_set_placas') 
    operador                 = fields.Char(string='Operador', compute='_set_operador') 
    dif_merma_excedente      = fields.Float(string='Diferencia Merma o Excedente', digits=(20, 2), compute='_set_dif_merma_excedente')   
    tolerancia               = fields.Float(string='Tolerancia Sistema', digits=(20, 2), compute='_set_tolerancia')
    tolerancia_ajustada      = fields.Float(string='Tolerancia Ajustada', digits=(20, 2))
    tolerancia_autorizada    = fields.Float(string='Tolerancia Autorizada', digits=(20, 2), compute='_set_tolerancia_autorizada')
    tolerancia_excedida      = fields.Float(string='Tolerancia Excedida', digits=(20, 2), compute='_set_tolerancia_excedida')
    tarifas                  = fields.Float(string='Tarifas', digits=(20, 2))
    subtotal_antes_desc      = fields.Float(string='Subtotal antes Descuento', digits=(20, 2), compute='_set_subtotal_antes_desc')
    currency_id              = fields.Many2one('res.currency', default=lambda self: self.env.user.company_id.currency_id)
    precio_producto          = fields.Monetary('Precio Producto', currency_field='currency_id')
    desc_tolerancia_exced    = fields.Monetary('Descuento por Tolerancia Excedida', currency_field='currency_id', compute='_set_desc_tolerancia_exced')
    importe                  = fields.Monetary('Importe', currency_field='currency_id', compute='_set_importe')
    iva                      = fields.Monetary('IVA', currency_field='currency_id', compute='_set_iva')
    retencion                = fields.Monetary('Retención', currency_field='currency_id', compute='_set_retencion')
    total                    = fields.Monetary('Total', currency_field='currency_id', compute='_set_total')

    
    @api.constrains('transferencia_origen_id', 'transferencia_interna_id', 'transferencia_destino_id')
    def _constrains_transferencias(self):
        if self.transferencia_origen_id == self.transferencia_destino_id:
            raise ValidationError("No se pueden repetir albaranes")  
        elif self.transferencia_destino_id == self.transferencia_origen_id:
            raise ValidationError("No se pueden repetir albaranes")                              


    #/ - / - / - / - / - / - / - / - / - / - / - /
    #Upload Origin Methods
    #/ - / - / - / - / - / - / - / - / - / - / - /    
    @api.one
    @api.depends('transferencia_origen_id')
    def _set_producto_id(self):        
        if self.transferencia_origen_id:
            self.producto_id = self.env['stock.move'].search([('picking_id', '=', self.transferencia_origen_id.id)], limit=1).product_id.id


    @api.one
    @api.depends('transferencia_origen_id')
    def _set_folio_tk_origen(self):        
        if self.transferencia_origen_id:
            self.folio_peso_tk_tr_ori = self.env['stock.picking'].search([('id', '=', self.transferencia_origen_id.id)], limit=1).folio_peso_tk        


    @api.one
    @api.depends('transferencia_origen_id')
    def _set_kilos_origen(self):        
        if self.transferencia_origen_id:
            self.kilos_origen = self.env['stock.move'].search([('picking_id', '=', self.transferencia_origen_id.id)], limit=1).quantity_done    


    #/ - / - / - / - / - / - / - / - / - / - / - /
    #Discharge Destiny Methods
    #/ - / - / - / - / - / - / - / - / - / - / - /
    @api.one
    @api.depends('transferencia_destino_id')
    def _set_producto_destino_id(self):        
        if self.transferencia_destino_id:
            self.producto_destino_id = self.env['stock.move'].search([('picking_id', '=', self.transferencia_destino_id.id)], limit=1).product_id.id


    @api.one
    @api.depends('transferencia_destino_id')
    def _set_folio_tk_destino(self):        
        if self.transferencia_destino_id:
            self.folio_peso_tk_tr_dest = self.env['stock.picking'].search([('id', '=', self.transferencia_destino_id.id)], limit=1).folio_peso_tk        


    @api.one
    @api.depends('kilos_destino', 'transferencia_destino_id')    
    def _set_dif_merma_excedente(self):
        if self.transferencia_destino_id:
            #Get kilos origen from related line:
            kilos_origen = 0.0
            
            if self.wbn_service_order_id:
                kilos_origen = self.env['wobin.service.order.line'].search([('wbn_service_order_id', '=', self.wbn_service_order_id.id),
                                                                            ('producto_id', '=', self.producto_destino_id.id)], limit=1).kilos_origen       

            self.dif_merma_excedente = self.kilos_destino - kilos_origen        

    
    @api.one
    @api.depends('transferencia_destino_id')
    def _set_kilos_destino(self):        
        if self.transferencia_destino_id:
            self.kilos_destino = self.env['stock.move'].search([('picking_id', '=', self.transferencia_destino_id.id)], limit=1).quantity_done    
    

    @api.one
    @api.depends('transferencia_destino_id')
    def _set_placas(self):        
        if self.transferencia_destino_id:
            self.placas = self.env['stock.picking'].search([('id', '=', self.transferencia_destino_id.id)], limit=1).placas        


    @api.one
    @api.depends('transferencia_destino_id')
    def _set_operador(self):        
        if self.transferencia_destino_id:
            self.operador = self.env['stock.picking'].search([('id', '=', self.transferencia_destino_id.id)], limit=1).operador
    

    @api.one
    @api.depends('transferencia_destino_id')     
    def _set_tolerancia(self):
        if self.transferencia_destino_id:        
            kilos_origen = 0.0        
            
            if self.wbn_service_order_id:
                kilos_origen = self.env['wobin.service.order.line'].search([('wbn_service_order_id', '=', self.wbn_service_order_id.id),
                                                                            ('producto_id', '=', self.producto_destino_id.id)], limit=1).kilos_origen       
            
            self.tolerancia = kilos_origen * 0.002


    @api.one
    @api.depends('tolerancia')    
    def _set_tolerancia_autorizada(self):
        if self.transferencia_destino_id:
            self.tolerancia_autorizada = self.tolerancia


    @api.one
    @api.depends('dif_merma_excedente', 'tolerancia_ajustada', 'tolerancia_autorizada') 
    def _set_tolerancia_excedida(self):
        if self.transferencia_destino_id:        
            self.tolerancia_excedida = -(self.dif_merma_excedente) - (self.tolerancia_ajustada + self.tolerancia_autorizada)


    @api.one
    @api.depends('transferencia_destino_id', 'tarifas') 
    def _set_subtotal_antes_desc(self):
        if self.transferencia_destino_id:        
            kilos_origen = 0.0        
            
            if self.wbn_service_order_id:            
                kilos_origen = self.env['wobin.service.order.line'].search([('wbn_service_order_id', '=', self.wbn_service_order_id.id),
                                                                            ('producto_id', '=', self.producto_destino_id.id)], limit=1).kilos_origen       
        
            self.subtotal_antes_desc = kilos_origen * self.tarifas


    @api.one
    @api.depends('tolerancia_excedida') 
    def _set_desc_tolerancia_exced(self):
        if self.transferencia_destino_id:
            if self.tolerancia_excedida <= 0:
                self.desc_tolerancia_exced = 0.0
            elif self.tolerancia_excedida > 0:
                self.desc_tolerancia_exced = self.tolerancia_excedida * self.precio_producto


    @api.one
    @api.depends('subtotal_antes_desc', 'desc_tolerancia_exced') 
    def _set_importe(self):
        if self.transferencia_destino_id:
            self.importe = self.subtotal_antes_desc - self.desc_tolerancia_exced


    @api.one
    @api.depends('importe') 
    def _set_iva(self): 
        if self.transferencia_destino_id:
            self.iva = self.importe * 0.16


    @api.one
    @api.depends('importe') 
    def _set_retencion(self): 
        if self.transferencia_destino_id:
            self.retencion = self.importe * 0.04


    @api.one
    @api.depends('importe', 'iva', 'retencion') 
    def _set_total(self):  
        if self.transferencia_destino_id:               
            self.total = self.importe + self.iva - self.retencion





class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    wbn_service_order_ids = fields.One2many('wobin.service.order', 'purchase_with_order_id', string='Ordenes de Servicio')
