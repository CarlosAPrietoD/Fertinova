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

    #Fields added to Form View of Inventory > Operations > Transfers
    operador = fields.Char(string='Operador')
    placas   = fields.Char(string='Placas')





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
    cant_disponible = fields.Float(string='Cantidad Disponible', digits=(20, 2), compute='_set_cant_disponible')

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
                                    ], string='Estado', default='no_asignada')
    pickings_ids = fields.One2many('wobin.service.order.line', 'wbn_service_order_id', string='Control de Albaranes')
    purchase_with_order_id = fields.Many2one('purchase.order', string='Orden de Compra')

    
    def cancelar_orden(self):
        self.estado = 'cancelada'





class WobinServiceOrderLine(models.Model):
    _name = 'wobin.service.order.line'
    _description = 'Wobin Service Order Line'


    _sql_constraints = [('transferencias_unique', 'unique (transferencia_origen_id,transferencia_interna_id)',     
                 'Albaranes duplicados no están permitidos por línea')]


    wbn_service_order_id     = fields.Many2one('wobin.service.order', string='Orden de Servicio')
    estado_wbn_servie_ord    = fields.Selection([('no_asignada', 'No Asignada'),
                                                 ('asignada', 'Asignada'),                                     
                                                 ('cancelada', 'Cancelada')
                                    ],string='Estado', related='wbn_service_order_id.estado')
                                    
    fecha_carga_origen       = fields.Date(string='Fecha Carga Origen')
    producto_id              = fields.Many2one('product.product', string='Producto', compute='_set_producto_id')
    folio_peso_tk_tr_ori     = fields.Char(string='Folio Peso Ticket')
    kilos_origen             = fields.Float(string='Kg Origen', digits=(20, 2), compute='_set_kilos_origen')
    transferencia_origen_id  = fields.Many2one('stock.picking', string='Transferencia Origen', domain=[('estado_wbn_servie_ord', '!=', 'cancelada')])
    fecha_descarga_destino   = fields.Date(string='Fecha Descarga Destino')
    dif_merma_excedente      = fields.Float(string='Diferencia Merma o Excedente', digits=(20, 2), compute='_set_dif_merma_excedente')
    transferencia_interna_id = fields.Many2one('stock.picking', string='Transferencia Interna')
    folio_peso_tk_tr_dest    = fields.Char(string='Folio Peso Ticket')
    kilos_destino            = fields.Float(string='Kg Destino', digits=(20, 2), compute='_set_kilos_destino')
    transferencia_destino_id = fields.Many2one('stock.picking', string='Transferencia Destino')
    placas                   = fields.Char(string='Placas', compute='_set_placas') 
    operador                 = fields.Char(string='Operador', compute='_set_operador')    
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

    
    @api.one
    @api.depends('transferencia_origen_id')
    def _set_producto_id(self):        
        if self.transferencia_origen_id:
            self.producto_id = self.env['stock.move'].search([('picking_id', '=', self.transferencia_origen_id.id)], limit=1).product_id.id


    @api.one
    @api.depends('transferencia_origen_id')
    def _set_kilos_origen(self):        
        if self.transferencia_origen_id:
            self.kilos_origen = self.env['stock.move'].search([('picking_id', '=', self.transferencia_origen_id.id)], limit=1).quantity_done    

    
    @api.one
    @api.depends('kilos_destino', 'kilos_origen')    
    def _set_dif_merma_excedente(self):
        self.dif_merma_excedente = self.kilos_destino - self.kilos_origen        

    
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
    @api.depends('kilos_origen')     
    def _set_tolerancia(self):
        self.tolerancia = self.kilos_origen * 0.002


    @api.one
    @api.depends('tolerancia')    
    def _set_tolerancia_autorizada(self):
        self.tolerancia_autorizada = self.tolerancia


    @api.one
    @api.depends('dif_merma_excedente', 'tolerancia_ajustada', 'tolerancia_autorizada') 
    def _set_tolerancia_excedida(self):
        self.tolerancia_excedida = -(self.dif_merma_excedente) - (self.tolerancia_ajustada + self.tolerancia_autorizada)


    @api.one
    @api.depends('kilos_origen', 'tarifas') 
    def _set_subtotal_antes_desc(self):
        self.subtotal_antes_desc = self.kilos_origen * self.tarifas


    @api.one
    @api.depends('tolerancia_excedida') 
    def _set_desc_tolerancia_exced(self):
        if self.tolerancia_excedida <= 0:
            self.desc_tolerancia_exced = 0.0
        elif self.tolerancia_excedida > 0:
            self.desc_tolerancia_exced = self.tolerancia_excedida * self.precio_producto


    @api.one
    @api.depends('subtotal_antes_desc', 'desc_tolerancia_exced') 
    def _set_importe(self):
        self.importe = self.subtotal_antes_desc - self.desc_tolerancia_exced


    @api.one
    @api.depends('importe') 
    def _set_iva(self): 
        self.iva = self.importe * 0.16


    @api.one
    @api.depends('importe') 
    def _set_retencion(self): 
        self.retencion = self.importe * 0.04


    @api.one
    @api.depends('importe', 'iva', 'retencion') 
    def _set_total(self):         
        self.total = self.importe + self.iva - self.retencion





class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    wbn_service_order_ids = fields.One2many('wobin.service.order', 'purchase_with_order_id', string='Ordenes de Servicio')


    """
    DESARROLLO CANCELADO en modelo stock.picking

    origin_transfer_id = fields.Many2one('stock.picking', string='Transferencia Origen', track_visibility='always')

    #is_waste   = fields.Boolean(string='¿Es merma?')
    is_surplus = fields.Boolean(string='¿Es excedente?')

    waste_ids     = fields.Many2many('stock.scrap', string='Folio Desecho', compute='_set_waste_ids')
    surplus_id    = fields.Many2one('stock.picking', string='Folio Excedente', compute='_set_surplus_id')
    surplus_count = fields.Integer(compute='get_surplus_count')

    delivery_amount  = fields.Float(string='Peso Origen', digits=(20, 2), compute='_set_delivery_amount')
    waste_amount     = fields.Float(string='Desecho', digits=(20, 2), compute='_set_waste_amount')
    surplus_amount   = fields.Float(string='Excedente', digits=(20, 2), compute='_set_surplus_amount')
    eff_qty_amount   = fields.Float(string='Cantidad Efectivamente Recibida', digits=(20, 2), compute='_set_eff_qty_amount')
    d_eff_qty_amount = fields.Float(string='Cantidad Efectivamente Entregada', digits=(20, 2), compute='_set_d_eff_qty_amount')

    custom_partner_id  = fields.Many2one('res.partner', string='Cliente', compute='_set_partner')
    custom_date_order  = fields.Datetime(string='Fecha', compute='_set_date_order')
    custom_incoterm_id = fields.Many2one('account.incoterms', string='Incoterm', compute='_set_incoterm')

    # Odoo Studio Fields - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    x_studio_aplica_flete = fields.Boolean(string='Aplica Flete', default=True)
    x_studio_pedido_de_compra_flete = fields.Many2one('purchase.order', string='Pedido de compra flete', domain="[('order_line.product_id.name', 'ilike', 'FLETE')]")
    # Odoo Studio Fields - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -



    @api.one 
    def _set_waste_ids(self):
        self.waste_ids = self.env['stock.scrap'].search([('picking_id', '=', self.id)]).ids         



    @api.one 
    def _set_surplus_id(self):
        self.surplus_id = self.env['stock.picking'].search([('is_surplus', '=', True),
                                                            ('origin_transfer_id', '=', self.id)], limit=1).id 



    @api.one
    @api.depends('name')
    def _set_delivery_amount(self):        
        self.delivery_amount = sum(line.quantity_done for line in self.move_ids_without_package if "Desecho" not in line.location_dest_id.name) 



    def get_surplus(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Excedentes',
            'view_mode': 'tree',
            'res_model': 'stock.picking',
            'domain': [('is_surplus', '=', True), ('origin_transfer_id', '=', self.id)],
            'context': "{'create': False}"
        }



    def get_surplus_count(self):
        for record in self:
            record.vehicle_count = self.env['stock.picking'].search_count(
                [('is_surplus', '=', True), ('origin_transfer_id', '=', self.id)])


    @api.one
    @api.depends('waste_ids')
    def _set_waste_amount(self):
        waste_objs = self.env['stock.scrap'].search([('picking_id', '=', self.id)])
        self.waste_amount = sum(rec.scrap_qty for rec in waste_objs)



    @api.one
    @api.depends('surplus_id')
    def _set_surplus_amount(self):
        self.surplus_amount = sum(line.quantity_done for line in self.surplus_id.move_ids_without_package)



    @api.one
    @api.depends('waste_amount', 'surplus_amount')
    def _set_eff_qty_amount(self):          
        self.eff_qty_amount = self.delivery_amount - self.waste_amount + self.surplus_amount 



    @api.one
    @api.depends('waste_amount', 'surplus_amount')
    def _set_d_eff_qty_amount(self):          
        self.d_eff_qty_amount = self.delivery_amount - self.waste_amount + self.surplus_amount 


    @api.one
    @api.depends('sale_id', 'purchase_id')
    def _set_partner(self):   
        if self.sale_id:
            self.custom_partner_id = self.env['res.partner'].search([('id', '=', self.sale_id.partner_id.id)]).id
        elif self.purchase_id:       
            self.custom_partner_id = self.env['res.partner'].search([('id', '=', self.purchase_id.partner_id.id)]).id



    @api.one
    @api.depends('sale_id', 'purchase_id')
    def _set_date_order(self):   
        if self.sale_id:
            self.custom_date_order = self.env['sale.order'].search([('id', '=', self.sale_id.id)]).date_order
        elif self.purchase_id:       
            self.custom_date_order = self.env['purchase.order'].search([('id', '=', self.purchase_id.id)]).date_order           



    @api.one
    @api.depends('sale_id', 'purchase_id')
    def _set_incoterm(self):   
        if self.sale_id:
            self.custom_incoterm_id = self.env['sale.order'].search([('id', '=', self.sale_id.id)]).incoterm.id
        elif self.purchase_id:       
            self.custom_incoterm_id = self.env['purchase.order'].search([('id', '=', self.purchase_id.id)]).incoterm_id.id




    #|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
    #Open a new window for surplus
    @api.multi
    def open_stock_picking_surplus(self):
        #Get current company_id from user where this process will apply just to GRANERO:
        company_aux_id = self.env['res.company'].browse(self.env['res.company']._company_default_get('your.module')).id
        company_id = company_aux_id.id

        #GRANERO is ID '2' in Companies:
        if company_id == 2:        
            line_ids_list    = list()
            item             = tuple()
            dictionary_vals  = dict()

            #Iterate over items in lines of stock picking
            #in order to construct data pre-filled for new
            #window of surplus transfer:
            for line in self.move_ids_without_package:  
                #Construct tuple item for each line (0, 0, dictionary_vals)
                dictionary_vals = {
                    'name': line.name,
                    'state': 'draft',
                    'product_id': line.product_id.id,
                    'date_expected': fields.datetime.now(),
                    'product_uom': line.product_uom.id,
                    'is_locked': False,
                    'show_operations': False
                }
                item = (0, 0, dictionary_vals)
                #Append into list which it will be used later in context:
                line_ids_list.append(item)       

            #Fill with this fixed data 
            sequence         = self.env['ir.sequence'].next_by_code('self.surplustock') or 'New'
            name_seq         = sequence             
            picking_type     = self.env['stock.picking.type'].search([('id', '=', 170)]).id 
            location_id      = self.env['stock.location'].search([('name', '=', self.location_id.name)]).id                                                                    

            #Context to pre-fill with data new window:
            ctxt = {
                'default_name': name_seq,
                'default_picking_type_id': picking_type,
                'default_location_id': self.location_id.id,
                'default_origin_transfer_id': self.id,
                'default_is_surplus': True,
                'default_surplus_id': self.id,
                'default_move_ids_without_package': line_ids_list
            }

            #Return new window of surplus transfer:
            return {
                #'name':_("Excedentes"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'stock.picking',
                #'res_id': partial_id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'domain': '[]',
                'context': ctxt            
            }   
    """        