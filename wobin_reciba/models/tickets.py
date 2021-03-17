from odoo import models, fields, api
from datetime import date, datetime
from odoo.exceptions import UserError

class RecibaTicket(models.Model):
    #Boletas
    _name = 'reciba.ticket'
    _inherit = ['mail.thread']
    _description = 'Boletas'


    @api.one
    @api.depends('humidity','apply_discount')
    def _get_humidity_discount(self):
        #Metodo para calcular el descuento de humedad por cada mil kilos
        if self.apply_discount == True:
            if self.humidity:
                if self.humidity > 14:
                    self.humidity_discount = ((self.humidity-14)*1.16)/100*1000
        else:
            self.humidity_discount = 0

    @api.one
    @api.depends('impurity','apply_discount')
    def _get_impurity_discount(self):
        #Metodo para calcular el descuento de impureza por cada mil kilos
        if self.apply_discount == True:
            if self.impurity:
                if self.impurity > 2:
                    self.impurity_discount = (self.impurity-2)/100*1000
        else:
            self.impurity_discount=0

    @api.one
    @api.depends('humidity', 'net_weight','apply_discount')
    def _get_humidity_total_discount(self):
        #Metodo para calcular el descuento total por humedad del peso neto 
        if self.apply_discount == True:
            if self.humidity:
                if self.humidity > 14:
                    self.humidity_total_discount = ((self.humidity-14)*1.16)/100*self.net_weight
        else: self.humidity_total_discount = 0

    @api.one
    @api.depends('impurity', 'net_weight','apply_discount')
    def _get_impurity_total_discount(self):
        #Metodo para calcular el descuento total por impureza del peso neto
        if self.apply_discount == True:
            if self.impurity:
                if self.impurity > 2:
                    self.impurity_total_discount = (self.impurity-2)/100*self.net_weight
        else:
            self.impurity_total_discount = 0

    @api.one
    @api.depends('humidity_total_discount', 'impurity_total_discount')
    def _get_discount_total(self):
        #Metodo para calcular el descuento total
        self.discount = self.humidity_total_discount+self.impurity_total_discount

    @api.one
    @api.depends('net_weight', 'discount')
    def _get_total_weight(self):
        #Metodo para calcular el peso neto analizado
        self.total_weight = self.net_weight-self.discount

    @api.one
    @api.depends('params_id')
    def _get_total_damage(self):
        #Metodo para calcular la suma de daños
        total = 0
        for data in self.params_id:
            if data.quality_params_id.damage:
                total += data.value
        self.sum_damage = total

    
    @api.one
    @api.depends('params_id')
    def _get_total_broken(self):
        #Metodo para calcular la suma de quebrados
        total = 0
        for data in self.params_id:
            if data.quality_params_id.broken:
                total += data.value
        self.sum_broken = total

    @api.one
    @api.depends('origin_id')
    def _default_origin_date(self):
        #Metodo para obtener fecha de asignacion de origen
        if self.origin_id:
            today = datetime.today()
            self.origin_date = today

    @api.one
    @api.depends('destination_id')
    def _default_destination_date(self):
        #Metodo para obtener fecha de asignacion de destino
        if self.destination_id:
            today = datetime.today()
            self.destination_date = today

    @api.one
    @api.depends('gross_weight', 'tare_weight')
    def _get_net_weight(self):
        #metodo para calcular peso neto
        if self.gross_weight and self.tare_weight:
            self.net_weight = self.gross_weight-self.tare_weight
        else:
            self.net_weight = 0

    @api.one
    @api.depends('gross_weight')
    def _default_gross_date(self):
        #Metodo para obtener fecha de peso bruto
        if self.gross_weight:
            today = datetime.today()
            self.gross_date = today

    @api.one
    @api.depends('tare_weight')
    def _default_tare_date(self):
        #Metodo para obtener fecha de peso tara
        if self.tare_weight:
            today = datetime.today()
            self.tare_date = today


    @api.one
    @api.depends('net_weight')
    def _default_net_date(self):
        #Metodo para obtener fecha de peso neto
        if self.net_weight:
            today = datetime.today()
            self.net_date = today

    @api.one
    @api.depends('net_weight', 'sum_broken', 'apply_bonus')
    def _get_broken_bonus(self):
        #Metodo para obtener el bono por grano quebrado
        if self.apply_bonus:
            if self.sum_broken <= 2:
                self.broken_bonus = 35 * self.net_weight/1000
            else:
                self.broken_bonus = 0
        else:
            self.broken_bonus = 0

    @api.one
    @api.depends('net_weight', 'impurity', 'apply_bonus')
    def _get_impurity_bonus(self):
        #Metodo para obtener el bono por impureza
        if self.apply_bonus:
            if self.impurity <= 1.5:
                self.impurity_bonus = 35 * self.net_weight/1000
            else:
                self.impurity_bonus = 0
        else:
            self.impurity_bonus = 0

    @api.one
    @api.depends('net_weight', 'sum_damage', 'apply_bonus')
    def _get_damage_bonus(self):
        #Metodo para obtener el bono por grano dañado
        if self.apply_bonus:
            if self.sum_damage <= 1.5:
                self.damage_bonus = 35 * self.net_weight/1000
            else:
                self.damage_bonus = 0
        else:
            self.damage_bonus = 0

    @api.one
    @api.depends('net_weight', 'humidity', 'apply_bonus')
    def _get_humidity_bonus(self):
        #Metodo para obtener el bono por humedad
        if self.apply_bonus:
            if self.humidity >= 14 and self.humidity <= 15:
                self.humidity_bonus = 35 * self.net_weight/1000
            else:
                self.humidity_bonus = 0
        else:
            self.humidity_bonus = 0

    @api.one
    @api.depends('broken_bonus', 'impurity_bonus', 'damage_bonus','humidity_bonus')
    def _get_total_bonus(self):
        #Metodo para obtener el bono total
        self.total_bonus = self.broken_bonus + self.impurity_bonus + self.damage_bonus + self.humidity_bonus


    @api.model
    def _get_name_weigher(self):
        #Obtener analista
        return self.env.user.name
    
    #------------------------------------Datos---------------------------------------------
    company_id = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('your.module'))
    state = fields.Selection([('draft', 'Borrador'),
    ('priceless', 'Confirmado sin precio'),
    ('confirmed', 'Confirmado'),
    ('reverse','Reversa'),
    ('cancel', 'Cancelado')], default='draft', track_visibility='onchange')
    transfer_id = fields.Many2one('stock.picking', string="Transferencia")
    transfer_count = fields.Integer("Transferencias", default=0)
    transfer_reverse_id = fields.Many2one('stock.picking', string="Reversa")
    transfer_reverse_count = fields.Integer("Reversa", default=0)
    credit_id = fields.Many2one('account.invoice', "Nota de crédito por descuento")
    credit_count = fields.Integer("Nota de crédito por descuento", default=0)
    manu_id = fields.Many2one('mrp.production', string="Fabricación")
    manu_count = fields.Integer(string="Fabricación", default=0)
    unbuild_id = fields.Many2one('mrp.unbuild', string="Desconstrucción")
    unbuild_count = fields.Integer(string="Desconstrucción", default=0)
    invoice_id = fields.Many2one('account.invoice')
    invoice_count = fields.Integer(string="Facturas", default=0)

    #-------------------------------------Datos generales----------------------------------
    name = fields.Char(string="Boleta", default="Boleta borrador", track_visibility='onchange', required=True)
    date = fields.Datetime(string="Fecha y hora", default=lambda self: fields.datetime.now())
    operation_type = fields.Selection([('in','Recepción'),
    ('out','Entrega'),
    ('dev_sale','Devolucion sobre venta'),
    ('dev_purchase','Devolucion sobre compra'),
    ('manufacturing','Fabricaciones'),
    ('transfer','Transferencias internas')], string="Tipo de operacion")
    operation_type_id = fields.Many2one('stock.picking.type', string="Tipo de operacion", track_visibility='onchange', required=True)
    reception = fields.Selection([('price', 'Con precio'),
    ('priceless', 'Sin precio')], string="Tipo de recepción", default='price', required=True, track_visibility='onchange')
    transfer_type = fields.Selection([('int', 'Misma sucursal'),
    ('in', 'Entrada'), 
    ('out','Salida')], string="Tipo de transferencia", default='int', track_visibility='onchange')
    weigher = fields.Char(string="Nombre del analista", track_visibility='onchange', default=_get_name_weigher, readonly=True, required=True)
    product_id = fields.Many2one('product.product', string="Producto", track_visibility='onchange', required=True)
    ticket_id = fields.Many2one('reciba.ticket', string="Boleta relacionada")
    ticket_count = fields.Integer("Boletas", default=0)
    sale_id = fields.Many2one('sale.order', string="Orden de venta", track_visibility='onchange')
    sale_invoice_status = fields.Selection(related='sale_id.invoice_status', string="Estatus de facturación", store=True)
    purchase_id = fields.Many2one('purchase.order', string="Pedido de compra", domain="[('company_id','=',company_id)]", track_visibility='onchange')
    purchase_invoice_status = fields.Selection(related='purchase_id.invoice_status', string="Estatus de facturación", store=True)
    partner_id = fields.Many2one('res.partner', string="Contacto", track_visibility='onchange', required=True)
    list_production_id = fields.Many2one('mrp.bom', string="Lista de materiales")
    origin = fields.Char(string="Documento origen", track_visibility='onchange')
    
    #------------------------------------Datos de calidad---------------------------------
    quality_id = fields.Many2one('reciba.quality', string="Norma de calidad", track_visibility='onchange', required=True)
    humidity = fields.Float(string="Humedad 14%", track_visibility='onchange', required=True)
    humidity_discount = fields.Float(string="Descuento (Kg)", compute='_get_humidity_discount', store=True)
    impurity = fields.Float(string="Impureza 2%", track_visibility='onchange', required=True)
    impurity_discount = fields.Float(string="Descuento (Kg)", compute='_get_impurity_discount', store=True)
    density = fields.Float(string="Densidad g/L 720-1000", track_visibility='onchange', required=True)
    temperature = fields.Float(string="Temperatura °C", track_visibility='onchange', required=True)
    params_id = fields.One2many('reciba.ticket.params', 'ticket_id', track_visibility='onchange')
    sum_damage = fields.Float(string="Suma daños", compute='_get_total_damage', store=True, track_visibility='onchange')
    sum_broken = fields.Float(string="Suma quebrados", compute='_get_total_broken', store=True, track_visibility='onchange')

    #-----------------------------------Datos de transportacion---------------------------
    driver = fields.Char(string="Nombre del operador", track_visibility='onchange')
    type_vehicle = fields.Selection([('van','Camioneta'),
    ('torton','Torton'),
    ('trailer', 'Trailer sencillo'),
    ('full','Trailer full')], string="Tipo de vehiculo", default='van', track_visibility='onchange')
    plate_vehicle = fields.Char(string="Placas unidad", track_visibility='onchange')
    plate_trailer = fields.Char(string="Placas remolque", track_visibility='onchange')
    plate_second_trailer = fields.Char(string="Placas segundo remolque", track_visibility='onchange')

    #-----------------------------------Datos de ubicaciones-----------------------------
    origin_id = fields.Many2one('stock.location', string="Ubicación origen", track_visibility='onchange', required=True)
    origin_date = fields.Datetime(string="Fecha y hora", compute='_default_origin_date', store=True)
    destination_id = fields.Many2one('stock.location', string="Ubicación destino", track_visibility='onchange', required=True)
    destination_date = fields.Datetime(string="Fecha y hora", compute='_default_destination_date', store=True)

    #-----------------------------------Datos de pesaje----------------------------------
    gross_weight = fields.Float(string="Peso Bruto", track_visibility='onchange')
    gross_date = fields.Datetime(string="Fecha y hora", compute='_default_gross_date', store=True)
    tare_weight = fields.Float(string="Peso Tara", track_visibility='onchange')
    tare_date = fields.Datetime(string="Fecha y hora", compute='_default_tare_date', store=True)
    net_weight = fields.Float(string="Peso Neto", compute='_get_net_weight', store=True)
    net_date = fields.Datetime(string="Fecha y hora", compute='_default_net_date', store=True)
    net_expected = fields.Float(string="Pendiente por surtir")
    qty_manufacturing = fields.Float(string="Cantidad a producir", track_visibility='onchange')
    bom_id = fields.Many2one('mrp.bom', string="Lista de materiales", domain="[('product_id', '=', product_id)]", track_visibility='onchange')

    #----------------------------------Datos de descuento-------------------------------
    apply_discount = fields.Boolean(string="Aplicar descuento", track_visibility='onchange')
    humidity_total_discount = fields.Float(string="Descuento total de humedad (Kg)", compute='_get_humidity_total_discount', store=True)
    impurity_total_discount = fields.Float(string="Descuento total de impureza (Kg)", compute='_get_impurity_total_discount', store=True)
    discount = fields.Float(string="Descuento total (kg)", compute='_get_discount_total', store=True)
    total_weight = fields.Float(string="Peso neto analizado", compute='_get_total_weight', store=True)
    price_po = fields.Float(related='purchase_id.order_line.price_unit', string="Precio", digits=(15,4), track_visibility='onchange')
    price_so = fields.Float(related='sale_id.order_line.price_unit', string="Precio", digits=(15,4), track_visibility='onchange')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env['res.company']._company_default_get('your.module').currency_id, string="Moneda", track_visibility='onchange')

    #----------------------------------Datos de bonificación----------------------------
    apply_bonus = fields.Boolean(string="Aplicar bonos", track_visibility='onchange')
    broken_bonus = fields.Float(string="Bono quebrado", compute='_get_broken_bonus', store=True)
    impurity_bonus = fields.Float(string="Bono impureza", compute='_get_impurity_bonus', store=True)
    damage_bonus = fields.Float(string="Bono dañado", compute='_get_damage_bonus', store=True)
    humidity_bonus = fields.Float(string="Bono humedad", compute='_get_humidity_bonus', store=True)
    total_bonus = fields.Float(string="Bono total", compute='_get_total_bonus', store=True)


    @api.onchange('operation_type')
    def _default_operation_type(self):
        #metodo para obtener el tipo de operacion
        operation_id = 0
        if self.operation_type=='in':
            operation_id = self.env['stock.picking.type'].search(['|',('name','=','Recepciones'),('name','=','Receipts')], limit=1).id
        elif self.operation_type=='out':
            operation_id = self.env['stock.picking.type'].search(['|',('name','=','Órdenes de entrega'),('name','=','Delivery Orders')], limit=1).id
        elif self.operation_type=='dev_sale':
            operation_id = self.env['stock.picking.type'].search([('name','=','Devolucion de Órdenes de entrega')], limit=1).id
        elif self.operation_type=='dev_purchase':
            operation_id = self.env['stock.picking.type'].search([('name','=','Devolucion de Recepciones')], limit=1).id
        elif self.operation_type=='transfer':
            operation_id = self.env['stock.picking.type'].search([('name','=','Transferencias internas')], limit=1).id
        elif self.operation_type=='manufacturing':
            operation_id = self.env['stock.picking.type'].search(['|',('name','=','Fabricación'),('name','=','Manufacturing')], limit=1).id
        self.operation_type_id = operation_id

    @api.onchange('quality_id')
    def _get_quality_params(self):
        #Metodo para agregar los parametros de calidad a la boleta
        self.params_id = None
        if self.quality_id:
            array_params = []
            for param in self.quality_id.params:
                array_params.append((0,0,{'quality_params_id':param.id, 'name': param.name, }))
            self.params_id = array_params

    @api.onchange('reception')
    def _get_reception_type(self):
        #metodo para detectar cambios de tipo de recepcion
        if self.reception == 'priceless':
            self.purchase_id = 0

    @api.onchange('type_vehicle')
    def _get_vehicle_type(self):
        #metodo para detectar cambios de tipo de vehiculo
        self.plate_trailer = ''
        self.plate_second_trailer = ''

    @api.onchange('sale_id')
    def _get_sale_order(self):
        #metodo para detectar cambios orden de venta
        if self.sale_id:
            self.partner_id = self.sale_id.partner_id
            self.net_expected = self.sale_id.order_line[0].product_uom_qty - self.sale_id.order_line[0].qty_delivered

    @api.onchange('product_id')
    def _get_product_manufacturing(self):
        #metodo para detectar cambiar la lista de materiales
        if self.product_id:
            if self.operation_type == 'manufacturing':
                if self.product_id.bom_ids:
                    self.bom_id = self.product_id.bom_ids[0]
                else:
                    msg = 'Este producto no cuenta con lista de materiales'
                    raise UserError(msg)

    def confirm_receipt_ticket(self):
        #Metodo para confirmar la boleta de entrada
        #Condicionales para confirmar la boleta
        if self.net_weight == 0:
            msg = 'El peso neto ingresado no es valido'
            raise UserError(msg)
        if self.humidity <= 0 or self.impurity <= 0 or self.temperature <= 0 or self.density <= 0:
            msg = 'Los valores de humedad, impureza, densidad y temperatura deben ser mayores a 0'
            raise UserError(msg)
        if self.purchase_id:
            if (self.purchase_id.order_line[0].product_qty-self.purchase_id.order_line[0].qty_received) < self.net_weight:
                msg = 'El peso neto es mayor a la cantidad faltante en la orden de compra'
                raise UserError(msg)
        if self.state == 'draft':
            #Asignacion del nombre de acuerdo al destino si esta en modo borrador
            if self.destination_id:
                tickets = self.env['reciba.ticket'].search(['&',('destination_id','=',self.destination_id.id),('state','!=','draft')])
                if tickets:
                    name_location = self.destination_id.display_name
                    number = str(len(tickets)+1).zfill(4)
                    self.name=name_location + '/' + number
                else:
                    self.name = self.destination_id.display_name + '/' + '0001'
            #Si hay bonos por calidad se elimina la orden de compra seleccionada y se pone en estado sin precio
            if self.total_bonus > 0:
                self.purchase_id = 0
                self.reception = 'priceless'
        
        if self.reception == 'price':
            #Creacion y asignación de la transferencia, si ya se tiene un precio asignado
            values={
            'picking_type_id': self.operation_type_id.id,
            'location_id': self.origin_id.id,
            'location_dest_id' : self.destination_id.id,
            'scheduled_date': datetime.today(),
            'reciba_id': self.id,
            'purchase_id': self.purchase_id.id,
            'partner_id': self.partner_id.id,
            'origin': self.purchase_id.name,
            'move_ids_without_package': [(0,0,{
                'name': self.product_id.name,
                'product_id': self.product_id.id,
                'product_uom_qty': self.net_weight,
                'quantity_done': self.net_weight,
                'product_uom': self.product_id.uom_po_id.id,
                'purchase_line_id': self.purchase_id.order_line[0].id,
                'location_dest_id': self.destination_id.id,
            })]}
            picking = self.env['stock.picking'].create(values)
            picking.button_validate()
            self.transfer_id = picking.id
            self.transfer_count = 1
            #Se crea una nota de credito en caso de haber descuento
            if self.apply_discount:
                if self.discount > 0:
                    account = self.env['account.account'].search([('name','=','PROVEEDORES NACIONALES')], limit=1).id
                    values={
                        'type': 'in_refund',
                        'partner_id': self.partner_id.id,
                        'date_invoice': date.today(),
                        'invoice_line_ids': [(0,0,{
                            'product_id': self.product_id.id,
                            'name': self.product_id.display_name,
                            'quantity': self.discount,
                            'uom_id': self.product_id.uom_id.id,
                            'price_unit': self.price_po,
                            'account_id': account
                        })]
                        }
                    credit = self.env['account.invoice'].create(values)
                    self.credit_id = credit.id
                    self.credit_count = 1
            self.state = 'confirmed'
        if self.reception == 'priceless':
            #Estado confirmado sin precio si no se tiene asignado
            self.state = 'priceless'

    def reverse_receipt_ticket(self):
        #Metodo para dar reversa a la boleta de entrada
        operation = self.env['stock.picking.type'].search([('name','=','Devolucion de Recepciones'),('warehouse_id','=',self.transfer_id.picking_type_id.warehouse_id.id)]).id
        values={
        'picking_type_id': operation,
        'location_id': self.destination_id.id,
        'location_dest_id' : self.origin_id.id,
        'scheduled_date': datetime.today(),
        'reciba_id': self.id,
        'purchase_id': self.purchase_id.id,
        'partner_id': self.partner_id.id,
        'move_ids_without_package': [(0,0,{
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'product_uom_qty': self.net_weight,
            'quantity_done': self.net_weight,
            'product_uom': self.product_id.uom_po_id.id,
            'purchase_line_id': self.purchase_id.order_line[0].id,
            'location_dest_id' : self.origin_id.id,
            'to_refund': True,
            })]
        }
        picking = self.env['stock.picking'].create(values)
        picking.button_validate()
        self.transfer_reverse_id = picking.id
        self.transfer_reverse_count = 1
        #Creacion de nueva boleta borrador
        values={
            'state': 'draft',
            'operation_type': self.operation_type,
            'operation_type_id': self.operation_type_id.id,
            'weigher': self.weigher,
            'product_id': self.product_id.id,
            'purchase_id': self.purchase_id.id,
            'partner_id': self.partner_id.id,
            'apply_discount': self.apply_discount,
            'quality_id': self.quality_id.id,
            'humidity': self.humidity,
            'impurity': self.impurity,
            'density': self.density,
            'temperature': self.temperature,
            'reception': self.reception,
            'driver': self.driver,
            'type_vehicle': self.type_vehicle,
            'plate_vehicle': self.plate_vehicle,
            'plate_trailer': self.plate_trailer,
            'plate_second_trailer': self.plate_second_trailer,
            'origin_id': self.origin_id.id,
            'destination_id': self.destination_id.id,
            'gross_weight': self.gross_weight,
            'tare_weight': self.tare_weight,
            'origin': self.name
        }
        ticket = self.env['reciba.ticket'].create(values)
        params = []
        for i,param in enumerate(self.params_id):
            params.append([0,0,{'ticket_id': ticket.id, 
                                    'quality_params_id': param.quality_params_id.id,
                                    'value': param.value}])
        ticket.params_id = params
        self.ticket_id = ticket.id
        self.ticket_count = 1
        self.state='reverse'

    def cancel_receipt_ticket(self):
        #Metodo para cancelar boletas sin precio
        self.state = 'cancel'
        
    def confirm_delivery_ticket(self):
        #Metodo para confirmar la boleta de salida
        #Condicionales para confirmar la boleta
        if self.net_weight == 0:
            msg = 'El peso neto ingresado no es valido'
            raise UserError(msg)
        if self.humidity <= 0 or self.impurity <= 0 or self.temperature <= 0 or self.density <= 0:
            msg = 'Los valores de humedad, impureza, densidad y temperatura deben ser mayores a 0'
            raise UserError(msg)
        if self.net_expected < self.net_weight:
            msg = 'El peso neto es mayor a la cantidad pendiente por surtir'
            raise UserError(msg)
        if self.state == 'draft':
            #Asignacion del nombre de acuerdo al destino si esta en modo borrador
            if self.origin_id:
                tickets = self.env['reciba.ticket'].search(['&',('origin_id','=',self.origin_id.id),('state','!=','draft')])
                if tickets:
                    name_location = self.origin_id.display_name
                    number = str(len(tickets)+1).zfill(4)
                    self.name=name_location + '/' + number
                else:
                    self.name = self.origin_id.display_name + '/' + '0001'
        
        #Creacion y asignación de la transferencia, si ya se tiene un precio asignado
        values={
        'picking_type_id': self.operation_type_id.id,
        'location_id': self.origin_id.id,
        'location_dest_id' : self.destination_id.id,
        'scheduled_date': datetime.today(),
        'reciba_id': self.id,
        'sale_id': self.sale_id.id,
        'partner_id': self.partner_id.id,
        'move_ids_without_package': [(0,0,{
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'product_uom_qty': self.net_weight,
            'quantity_done': self.net_weight,
            'product_uom': self.product_id.uom_po_id.id,
            'location_dest_id' : self.destination_id.id,
            'sale_line_id': self.sale_id.order_line[0].id,
        })]}
        picking = self.env['stock.picking'].create(values)
        picking.button_validate()
        self.transfer_id = picking.id
        self.transfer_count = 1
        self.state = 'confirmed'

    def reverse_delivery_ticket(self):
        #Metodo para dar reversa a la boleta de salida
        operation = self.env['stock.picking.type'].search([('name','=','Devolucion de Órdenes de entrega'),('warehouse_id','=',self.transfer_id.picking_type_id.warehouse_id.id)]).id
        values={
        'picking_type_id': operation,
        'location_id': self.destination_id.id,
        'location_dest_id' : self.origin_id.id,
        'scheduled_date': datetime.today(),
        'reciba_id': self.id,
        'sale_id': self.sale_id.id,
        'partner_id': self.partner_id.id,
        'move_ids_without_package': [(0,0,{
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'product_uom_qty': self.net_weight,
            'quantity_done': self.net_weight,
            'product_uom': self.product_id.uom_po_id.id,
            'location_dest_id' : self.origin_id.id,
            'sale_line_id': self.sale_id.order_line[0].id,
            'to_refund': True,
            })]
        }
        picking = self.env['stock.picking'].create(values)
        picking.button_validate()
        self.transfer_reverse_id = picking.id
        self.transfer_reverse_count = 1
        #Creacion de nueva boleta borrador
        values={
            'state': 'draft',
            'operation_type': self.operation_type,
            'operation_type_id': self.operation_type_id.id,
            'weigher': self.weigher,
            'product_id': self.product_id.id,
            'sale_id': self.sale_id.id,
            'partner_id': self.partner_id.id,
            'apply_discount': self.apply_discount,
            'quality_id': self.quality_id.id,
            'humidity': self.humidity,
            'impurity': self.impurity,
            'density': self.density,
            'temperature': self.temperature,
            'reception': self.reception,
            'driver': self.driver,
            'type_vehicle': self.type_vehicle,
            'plate_vehicle': self.plate_vehicle,
            'plate_trailer': self.plate_trailer,
            'plate_second_trailer': self.plate_second_trailer,
            'origin_id': self.origin_id.id,
            'destination_id': self.destination_id.id,
            'gross_weight': self.gross_weight,
            'tare_weight': self.tare_weight,
            'origin': self.name
        }
        ticket = self.env['reciba.ticket'].create(values)
        params = []
        for i,param in enumerate(self.params_id):
            params.append([0,0,{'ticket_id': ticket.id, 
                                    'quality_params_id': param.quality_params_id.id,
                                    'value': param.value}])
        ticket.params_id = params
        self.ticket_id = ticket.id
        self.ticket_count = 1
        self.state='reverse'

    def confirm_dev_sale_ticket(self):
        #Metodo para confirmar la boleta de devolucion sobre venta
        #Condicionales para confirmar la boleta
        if self.net_weight == 0:
            msg = 'El peso neto ingresado no es valido'
            raise UserError(msg)
        if self.humidity <= 0 or self.impurity <= 0 or self.temperature <= 0 or self.density <= 0:
            msg = 'Los valores de humedad, impureza, densidad y temperatura deben ser mayores a 0'
            raise UserError(msg)
        if self.sale_id.order_line[0].qty_delivered < self.net_weight:
            msg = 'El peso neto es mayor a la cantidad entregada en la orden de venta'
            raise UserError(msg)
        if self.state == 'draft':
            #Asignacion del nombre de acuerdo al destino si esta en modo borrador
            if self.destination_id:
                tickets = self.env['reciba.ticket'].search(['&',('destination_id','=',self.destination_id.id),('state','!=','draft')])
                if tickets:
                    name_location = self.destination_id.display_name
                    number = str(len(tickets)+1).zfill(4)
                    self.name=name_location + '/' + number
                else:
                    self.name = self.destination_id.display_name + '/' + '0001'
        
        #Creacion y asignación de la transferencia
        values={
        'picking_type_id': self.operation_type_id.id,
        'location_id': self.origin_id.id,
        'location_dest_id' : self.destination_id.id,
        'scheduled_date': datetime.today(),
        'reciba_id': self.id,
        'sale_id': self.sale_id.id,
        'partner_id': self.partner_id.id,
        'move_ids_without_package': [(0,0,{
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'product_uom_qty': self.net_weight,
            'quantity_done': self.net_weight,
            'product_uom': self.product_id.uom_po_id.id,
            'location_dest_id' : self.destination_id.id,
            'sale_line_id': self.sale_id.order_line[0].id,
            'to_refund': True,
        })]}
        picking = self.env['stock.picking'].create(values)
        picking.button_validate()
        self.transfer_id = picking.id
        self.transfer_count = 1
        self.state = 'confirmed'

    def confirm_dev_purchase_ticket(self):
        #Metodo para confirmar la boleta de devolucion sobre compra
        #Condicionales para confirmar la boleta
        if self.net_weight == 0:
            msg = 'El peso neto ingresado no es valido'
            raise UserError(msg)
        if self.humidity <= 0 or self.impurity <= 0 or self.temperature <= 0 or self.density <= 0:
            msg = 'Los valores de humedad, impureza, densidad y temperatura deben ser mayores a 0'
            raise UserError(msg)
        if self.purchase_id.order_line[0].qty_received < self.net_weight:
            msg = 'El peso neto es mayor a la cantidad entregada de la orden de compra'
            raise UserError(msg)
        if self.state == 'draft':
            #Asignacion del nombre de acuerdo al destino si esta en modo borrador
            if self.origin_id:
                tickets = self.env['reciba.ticket'].search(['&',('origin_id','=',self.origin_id.id),('state','!=','draft')])
                if tickets:
                    name_location = self.origin_id.display_name
                    number = str(len(tickets)+1).zfill(4)
                    self.name=name_location + '/' + number
                else:
                    self.name = self.origin_id.display_name + '/' + '0001'
        
        #Creacion y asignación de la transferencia
        values={
        'picking_type_id': self.operation_type_id.id,
        'location_id': self.origin_id.id,
        'location_dest_id' : self.destination_id.id,
        'scheduled_date': datetime.today(),
        'reciba_id': self.id,
        'purchase_id': self.purchase_id.id,
        'partner_id': self.partner_id.id,
        'move_ids_without_package': [(0,0,{
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'product_uom_qty': self.net_weight,
            'quantity_done': self.net_weight,
            'product_uom': self.product_id.uom_po_id.id,
            'purchase_line_id': self.purchase_id.order_line[0].id,
            'location_dest_id' : self.destination_id.id,
            'to_refund': True,
        })]}
        picking = self.env['stock.picking'].create(values)
        picking.button_validate()
        self.transfer_id = picking.id
        self.transfer_count = 1
        self.state = 'confirmed'

    def confirm_transfer_ticket(self):
        #Metodo para confirmar la boleta de transferencia interna
        #Condicionales para confirmar la boleta
        if self.net_weight == 0:
            msg = 'El peso neto ingresado no es valido'
            raise UserError(msg)
        if self.humidity == 0 or self.impurity == 0 or self.temperature == 0 or self.density == 0:
            msg = 'Los valores de humedad, impureza, densidad y temperatura deben ser mayores a 0'
            raise UserError(msg)
        if self.state == 'draft':
            #Asignacion del nombre de acuerdo al tipo de transferencia
            if self.transfer_type == 'int' or self.transfer_type == 'in':
                if self.destination_id:
                    tickets = self.env['reciba.ticket'].search(['&',('destination_id','=',self.destination_id.id),('state','!=','draft')])
                    if tickets:
                        name_location = self.destination_id.display_name
                        number = str(len(tickets)+1).zfill(4)
                        self.name=name_location + '/' + number
                    else:
                        self.name = self.destination_id.display_name + '/' + '0001'
            elif self.transfer_type == 'out':
                if self.origin_id:
                    tickets = self.env['reciba.ticket'].search([('origin_id','=',self.origin_id.id),('state','!=','draft'),('transfer_type','=','out')])
                    if tickets:
                        name_location = self.origin_id.display_name
                        number = str(len(tickets)+1).zfill(4)
                        self.name=name_location + '/' + number
                    else:
                        self.name = self.origin_id.display_name + '/' + '0001'

        #Creacion y asignación de la transferencia
        values={
        'picking_type_id': self.operation_type_id.id,
        'location_id': self.origin_id.id,
        'location_dest_id' : self.destination_id.id,
        'scheduled_date': datetime.today(),
        'reciba_id': self.id,
        'partner_id': self.partner_id.id,
        'move_ids_without_package': [(0,0,{
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'product_uom_qty': self.net_weight,
            'quantity_done': self.net_weight,
            'product_uom': self.product_id.uom_po_id.id,
            'location_dest_id' : self.destination_id.id,
        })]}
        picking = self.env['stock.picking'].create(values)
        picking.button_validate()
        self.transfer_id = picking.id
        self.transfer_count = 1
        if self.transfer_type == 'out':
            #Creacion de nueva boleta borrador si la transferencia es de salida
            values={
                'state': 'draft',
                'operation_type': self.operation_type,
                'operation_type_id': self.operation_type_id.id,
                'product_id': self.product_id.id,
                'driver': self.driver,
                'type_vehicle': self.type_vehicle,
                'plate_vehicle': self.plate_vehicle,
                'plate_trailer': self.plate_trailer,
                'plate_second_trailer': self.plate_second_trailer,
                'origin_id': self.destination_id.id,
                'gross_weight': self.gross_weight,
                'tare_weight': self.tare_weight,
                'ticket_id': self.id,
                'transfer_type': 'in'
            }
            ticket = self.env['reciba.ticket'].create(values)
            self.ticket_id = ticket.id
            self.ticket_count = 1
        elif self.transfer_type == 'in':
            #Si es de entrada se revisa la relacion de las boletas de salida y entrada
            if self.ticket_id.ticket_id == 0:
                self.ticket_id.ticket_id = self.id
                self.ticket_id.ticket_count = 1
                self.ticket_count = 1
            elif self.ticket_id.ticket_id and self.ticket_id.ticket_id.id != self.id:
                msg = 'La boleta de salida ya está relacionada con otra boleta de entrada'
                raise UserError(msg)
            else:
                self.ticket_count = 1

        self.state = 'confirmed'

    def confirm_manufacturing_ticket(self):
        #Metodo para confirmar la boleta de fabricación
        #Condicionales para confirmar la boleta
        if self.qty_manufacturing <= 0:
            msg = 'La cantidad a producir no es valida'
            raise UserError(msg)
        if self.humidity == 0 or self.impurity == 0 or self.temperature == 0 or self.density == 0:
            msg = 'Los valores de humedad, impureza, densidad y temperatura deben ser mayores a 0'
            raise UserError(msg)
        if self.state == 'draft':
            #Asignacion del nombre de acuerdo al destino si esta en modo borrador
            if self.origin_id:
                tickets = self.env['reciba.ticket'].search(['&',('origin_id','=',self.origin_id.id),('state','!=','draft')])
                if tickets:
                    name_location = self.origin_id.display_name
                    number = str(len(tickets)+1).zfill(4)
                    self.name=name_location + '/' + number
                else:
                    self.name = self.origin_id.display_name + '/' + '0001'
        #Creacion de la fabricación
        values={
            'product_id': self.product_id.id,
            'product_qty': self.qty_manufacturing,
            'product_uom_id' : self.product_id.uom_id.id,
            'bom_id': self.bom_id.id,
            'picking_type_id': self.operation_type_id.id,
            'location_src_id': self.origin_id.id,
            'location_dest_id': self.destination_id.id,
        }
        production = self.env['mrp.production'].create(values)
        production.action_assign()
        #creación del registro para validar la fabricacion
        values={
            'product_id': self.product_id.id,
            'product_qty': self.qty_manufacturing,
            'product_uom_id' : self.product_id.uom_id.id,
            'production_id' : production.id
        }
        produce = self.env['mrp.product.produce'].create(values)
        lines = []
        for move in production.move_raw_ids:
            lines.append((0,0,{'product_id': move.product_id.id,
            'product_qty': move.product_qty,
            'product_uom_id': move.product_uom.id,
            'qty_to_consume': move.product_uom_qty,
            'qty_reserved': move.reserved_availability,
            'qty_done': move.product_uom_qty}))
        produce.produce_line_ids = lines
        #Cambiar a en proceso
        produce.do_produce()
        #Marcar como hecho
        production.button_mark_done()
        self.manu_id = production.id
        self.manu_count = 1
        self.state = 'confirmed'

    def unbuild_manufacturing_ticket(self):
        #Metodo para hacer desconstruccion
        values={
            'product_id': self.product_id.id,
            'product_qty': self.qty_manufacturing,
            'product_uom_id': self.product_id.uom_id.id,
            'bom_id': self.bom_id.id,
            'location_id': self.destination_id.id,
            'location_dest_id': self.origin_id.id,
            'mo_id': self.manu_id.id,
        }
        unbuild = self.env['mrp.unbuild'].create(values)
        unbuild.action_validate()
        self.unbuild_id = unbuild.id
        self.unbuild_count = 1
        self.state = 'reverse'
        

    @api.multi
    def action_view_transfer(self):
        #Metodo para ver transferencias relacionadas
        action = self.env.ref('wobin_reciba.reciba_transfer')
        result = action.read()[0]
        result['domain'] = [('id','=', self.transfer_id.id)]
        return result
    
    @api.multi
    def action_view_reverse(self):
        #Metodo para ver transferencias de reversa
        action = self.env.ref('wobin_reciba.reciba_transfer')
        result = action.read()[0]
        result['domain'] = [('id','=', self.transfer_reverse_id.id)]
        return result

    @api.multi
    def action_view_ticket(self):
        #Metodo para ver boletas relacionadas
        action = None
        if self.operation_type == 'in':
            action = self.env.ref('wobin_reciba.tickets_reception')
        elif self.operation_type == 'out':
            action = self.env.ref('wobin_reciba.tickets_delivery')
        elif self.operation_type == 'dev_sale':
            action = self.env.ref('wobin_reciba.tickets_delivery')
        elif self.operation_type == 'dev_purchase':
            action = self.env.ref('wobin_reciba.tickets_reception')
        elif self.operation_type == 'transfer':
            action = self.env.ref('wobin_reciba.internal_transfer')
        result = action.read()[0]
        result['domain'] = [('id','=', self.ticket_id.id)]
        return result

    @api.multi
    def action_view_credit(self):
        #Metodo para ver notas de credito relacionadas
        action = self.env.ref('wobin_reciba.reciba_credit')
        result = action.read()[0]
        result['domain'] = [('id','=', self.credit_id.id)]
        return result

    @api.multi
    def action_view_manufacturing(self):
        #Metodo para ver fabricaciones relacionadas
        action = self.env.ref('wobin_reciba.reciba_manufacturing')
        result = action.read()[0]
        result['domain'] = [('id','=', self.manu_id.id)]
        return result

    @api.multi
    def action_view_unbuild(self):
        #Metodo para ver desconstrucciones relacionadas
        action = self.env.ref('wobin_reciba.reciba_unbuild')
        result = action.read()[0]
        result['domain'] = [('id','=', self.unbuild_id.id)]
        return result

    @api.multi
    def action_view_invoice(self):
        #Metodo para ver facturas relacionadas
        action = self.env.ref('wobin_reciba.reciba_invoice')
        result = action.read()[0]
        result['domain'] = [('id','=', self.invoice_id.id)]
        return result

    @api.multi
    def unlink(self):
        #Validacion para eliminar la boleta
        if self.state != 'draft':
            msg = 'La boleta debe estar en estado borrador para ser eliminada'
            raise UserError(msg)
        #Eliminar la relacion de boletas cuando una es eliminada
        ticket = self.env['reciba.ticket'].search([('ticket_id','=',self.id)])
        if ticket:
            ticket.ticket_id = 0
            ticket.ticket_count = 0
        return super(RecibaTicket, self).unlink()

class RecibaTicketParams(models.Model):
    #Parametros de calidad de boleta
    _name = 'reciba.ticket.params'
    _description = 'Boletas'

    ticket_id = fields.Many2one('reciba.ticket')
    quality_params_id = fields.Many2one('reciba.quality.params', 'Parametro de calidad')
    max_value = fields.Float(related='quality_params_id.value', string="Máximo")
    unit = fields.Char(related='quality_params_id.unit', string="Unidad de medida")
    value = fields.Float(string="Valor")

class RecibaQuality(models.Model):
    #Normas de calidad
    _name = 'reciba.quality'
    _description = 'Parametros de calidad'

    name = fields.Char(string="Norma")
    product_id = fields.Many2one('product.product', string="Producto")
    params = fields.One2many('reciba.quality.params', 'quality_id')


class RecibaQualityParams(models.Model):
    #Parametros de calidad
    _name = 'reciba.quality.params'
    _description = 'Parametros de calidad de Reciba'

    name = fields.Char(string="Nombre")
    quality_id = fields.Many2one('reciba.quality')
    value = fields.Float(string="Máximo")
    unit = fields.Char(string="Unidad de medida")
    damage = fields.Boolean(string="Sumar daño")
    broken = fields.Boolean(string="Sumar quebrado")

class StockPicking(models.Model):
    _inherit='stock.picking'
    
    x_studio_aplica_flete= fields.Boolean()
    reciba_id = fields.Many2one('reciba.ticket', string="Reciba")

class AccountInvoice(models.Model):
    _inherit='account.invoice'
    
    @api.multi
    def unlink(self):
        #Metodo para eliminar la relacion de notas de crédito cuando una es eliminada
        ticket = self.env['reciba.ticket'].search([('credit_id','=',self.id)])
        if ticket:
            ticket.credit_id = 0
            ticket.credit_count = 0
        return super(AccountInvoice, self).unlink()

class ReportRecibaTicket(models.AbstractModel):
    #Reporte recepción con precio
    _name = 'report.wobin_reciba.report_ticket'

    @api.model
    def _get_report_values(self, docids, data=None): 
        tickets = self.env['reciba.ticket'].browse(docids)
        docs=[]
        for ticket in tickets:
            
            doc={'ticket': ticket,
                'total_format': f'{ticket.total_weight:,.2f}'
            }
            docs.append(doc)
            
        
        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': docs
        }

class ReportRecibaTicketPriceless(models.AbstractModel):
    #Reporte recepción sin precio
    _name = 'report.wobin_reciba.report_ticket_priceless'

    @api.model
    def _get_report_values(self, docids, data=None): 
        tickets = self.env['reciba.ticket'].browse(docids)
        docs=[]
        for ticket in tickets:
            
            doc={'ticket': ticket,
                'total_format': f'{ticket.total_weight:,.2f}'
            }
            docs.append(doc)
            
        
        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': docs
        }

class RecibaInvoice(models.Model):
    #Campo que relaciona factura con boletas
    _name = 'reciba.invoice'

    @api.model
    def create(self, values):
        #agregamos la relacion de reciba con factura
        invoice = super(RecibaInvoice, self).create(values)
        
        invoice.reciba_id.write({
            'invoice_id' : invoice.invoice_id.id,
            'invoice_count' : 1
        })
        return invoice

    @api.multi
    def unlink(self):
        #Borramos la relacion de la boleta con la factura
        self.reciba_id.write({
            'invoice_id' : 0,
            'invoice_count' : 0
        })
        return super(RecibaInvoice, self).unlink()

    invoice_id = fields.Many2one('account.invoice')
    reciba_id = fields.Many2one('reciba.ticket', domain="[('operation_type','=','in'),('state','=','confirmed'),('invoice_id','=',None)]")

class AccountInvoice(models.Model):
    #Campo que relaciona factura con boletas
    _inherit = 'account.invoice'

    reciba_id = fields.One2many('reciba.invoice', 'invoice_id', string="Boleta reciba")
