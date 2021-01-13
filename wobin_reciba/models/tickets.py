from odoo import models, fields, api
from datetime import date, datetime
from odoo.exceptions import UserError

class RecibaTicket(models.Model):
    #Boletas
    _name = 'reciba.ticket'
    _description = 'Boletas'


    @api.one
    @api.depends('humidity')
    def _get_humidity_discount(self):
        #Metodo para calcular el descuento de humedad por cada mil kilos
        if self.apply_discount == True:
            if self.humidity:
                if self.humidity > 14:
                    self.humidity_discount = ((self.humidity-14)*1.16)/100*1000
        else:
            self.humidity_discount = 0

    @api.one
    @api.depends('impurity')
    def _get_impurity_discount(self):
        #Metodo para calcular el descuento de impureza por cada mil kilos
        if self.apply_discount == True:
            if self.impurity:
                if self.impurity > 2:
                    self.impurity_discount = (self.impurity-2)/100*1000
        else:
            self.impurity_discount=0

    @api.one
    @api.depends('humidity', 'net_weight')
    def _get_humidity_total_discount(self):
        #Metodo para calcular el descuento total por humedad del peso neto 
        if self.apply_discount == True:
            if self.humidity:
                if self.humidity > 14:
                    self.humidity_total_discount = ((self.humidity-14)*1.16)/100*self.net_weight
        else: self.humidity_total_discount = 0

    @api.one
    @api.depends('impurity', 'net_weight')
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
    
    #------------------------------------Datos---------------------------------------------
    company_id = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('your.module'))
    state = fields.Selection([('draft', 'Borrador'),
    ('confirmed', 'Confirmado'),
    ('reverse','Reversa'),
    ('cancel', 'Cancelado')], default='draft')
    transfer_id = fields.Many2one('stock.picking', string="Transferencia")
    transfer_count = fields.Integer("Transferencias", default=0)
    transfer_reverse_id = fields.Many2one('stock.picking', string="Reversa")
    transfer_reverse_count = fields.Integer("Transferencias", default=0)

    #-------------------------------------Datos generales----------------------------------
    name = fields.Char(string="Boleta", default="Boleta borrador")
    date = fields.Datetime(string="Fecha y hora", default=lambda self: fields.datetime.now())
    operation_type = fields.Selection([('in','Recepción'),
    ('out','Entrega'),
    ('dev_sale','Devolucion sobre venta'),
    ('dev_purchase','Devolucion sobre compra'),
    ('manufacturing','Fabricaciones'),
    ('transfer','Transferencias internas'),
    ('order','Ordenes de desconstruccion')], string="Tipo de operacion")
    operation_type_id = fields.Many2one('stock.picking.type', string="Tipo de operacion")
    transfer_type = fields.Selection([('int', 'Misma sucursal'),
    ('in', 'Entrada'), 
    ('out','Salida')], string="Tipo de transferencia")
    weigher = fields.Char(string="Nombre del analista")
    product_id = fields.Many2one('product.product', string="Producto")
    ticket_id = fields.Many2one('wreciba.ticket', string="Boleta relacionada")
    ticket_count = fields.Integer("Boletas", default=0)
    sale_id = fields.Many2one('sale.order', string="Orden de venta")
    purchase_id = fields.Many2one('purchase.order', string="Pedido de compra", domain="[('company_id','=',company_id)]")
    purchase_invoice_status = fields.Selection(related='purchase_id.invoice_status')
    partner_id = fields.Many2one('res.partner', string="Contacto")
    list_production_id = fields.Many2one('mrp.bom', string="Lista de materiales")
    qty_produce = fields.Float(string="Cantidad a producir")
    qty_process = fields.Float(string="Cantidad a procesar")
    
    #------------------------------------Datos de calidad---------------------------------
    quality_id = fields.Many2one('reciba.quality', string="Norma de calidad")
    humidity = fields.Float(string="Humedad 14%")
    humidity_discount = fields.Float(string="Descuento (Kg)", compute='_get_humidity_discount', store=True)
    impurity = fields.Float(string="Impureza 2%")
    impurity_discount = fields.Float(string="Descuento (Kg)", compute='_get_impurity_discount', store=True)
    density = fields.Float(string="Densidad g/L 720-1000")
    temperature = fields.Float(string="Temperatura °C")
    params_id = fields.One2many('reciba.ticket.params', 'ticket_id')
    sum_damage = fields.Float(string="Suma daños", compute='_get_total_damage', store=True)
    sum_broken = fields.Float(string="Suma quebrados", compute='_get_total_broken', store=True)

    #-----------------------------------Datos de transportacion---------------------------
    driver = fields.Char(string="Nombre del operador")
    type_vehicle = fields.Selection([('van','Camioneta'),
    ('torton','Torton'),
    ('trailer', 'Trailer sencillo'),
    ('full','Trailer full')], string="Tipo de vehiculo")
    plate_vehicle = fields.Char(string="Placas unidad")
    plate_trailer = fields.Char(string="Placas remolque")
    plate_second_trailer = fields.Char(string="Placas segundo remolque")

    #-----------------------------------Datos de ubicaciones-----------------------------
    origin_id = fields.Many2one('stock.location', string="Ubicación origen")
    origin_date = fields.Datetime(string="Fecha y hora", compute='_default_origin_date', store=True)
    destination_id = fields.Many2one('stock.location', string="Ubicación destino")
    destination_date = fields.Datetime(string="Fecha y hora", compute='_default_destination_date', store=True)

    #-----------------------------------Datos de pesaje----------------------------------
    reception = fields.Selection([('price', 'Con precio'),
    ('priceless', 'Sin precio')], string="Tipo de recepción")
    gross_weight = fields.Float(string="Peso Bruto")
    gross_date = fields.Datetime(string="Fecha y hora", compute='_default_gross_date', store=True)
    tare_weight = fields.Float(string="Peso Tara")
    tare_date = fields.Datetime(string="Fecha y hora", compute='_default_tare_date', store=True)
    net_weight = fields.Float(string="Peso Neto", compute='_get_net_weight', store=True)
    net_date = fields.Datetime(string="Fecha y hora", compute='_default_net_date', store=True)

    #----------------------------------Datos de descuento-------------------------------
    apply_discount = fields.Boolean(string="Aplicar descuento")
    humidity_total_discount = fields.Float(string="Descuento total de humedad (Kg)", compute='_get_humidity_total_discount', store=True)
    impurity_total_discount = fields.Float(string="Descuento total de impureza (Kg)", compute='_get_impurity_total_discount', store=True)
    discount = fields.Float(string="Descuento total (kg)", compute='_get_discount_total', store=True)
    total_weight = fields.Float(string="Peso neto analizado", compute='_get_total_weight', store=True)
    price_po = fields.Float(related='purchase_id.order_line.price_unit', string="Precio", digits=(15,4))
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env['res.company']._company_default_get('your.module').currency_id, string="Moneda")


    @api.onchange('operation_type')
    def _default_operation_type(self):
        #metodo para obtener el tipo de operacion
        operation_id = 0
        if self.operation_type=='in':
            operation_id = self.env['stock.picking.type'].search(['|',('name','=','Recepciones'),('name','=','Receipts')], limit=1).id
        elif self.operation_type=='out':
            operation_id = self.env['stock.picking.type'].search(['|',('name','=','Órdenes de entrega'),('name','=','Delivery Orders')], limit=1).id
        self.operation_type_id = operation_id

    @api.onchange('quality_id')
    def get_quality_params(self):
        #Metodo para agregar los parametros de calidad a la boleta
        self.params_id = None
        if self.quality_id:
            array_params = []
            for param in self.quality_id.params:
                array_params.append((0,0,{'quality_params_id':param.id, 'name': param.name, }))
            self.params_id = array_params

    def confirm_receipt_ticket(self):
        #Metodo para confirmar la boleta de entrada
        if self.net_weight == 0:
            msg = 'El peso neto ingresado no es valido'
            raise UserError(msg)
        if self.humidity == 0 or self.impurity == 0 or self.temperature == 0:
            msg = 'Los valores de humedad, impureza y temperatura deben ser mayores a 0'
            raise UserError(msg)
        #Asignacion del nombre de acuerdo 
        if self.destination_id:
            tickets = self.env['reciba.ticket'].search(['&',('destination_id','=',self.destination_id.id),('state','=','confirmed')])
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
        'move_ids_without_package': [(0,0,{
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'product_uom_qty': self.net_weight,
            'quantity_done': self.net_weight,
            'product_uom': self.product_id.uom_po_id.id,
            'purchase_line_id': self.purchase_id.order_line[0].id,
        })]}
        picking = self.env['stock.picking'].create(values)
        picking.state = 'done'
        self.purchase_id.order_line[0].qty_received = self.purchase_id.order_line[0].qty_received+self.net_weight
        self.transfer_id = picking.id
        self.transfer_count = 1
        self.state='confirmed'

    def reverse_receipt_ticket(self):
        #Metodo para dar reversa a la boleta de entrada
        operation = self.env['stock.picking.type'].search([('name','=','Devolucion de Recepciones'),('warehouse_id','=',self.transfer_id.picking_type_id.warehouse_id.id)]).id
        values={
        'picking_type_id': operation,
        'location_id': self.destination_id.id,
        'location_dest_id' : self.origin_id.id,
        'scheduled_date': datetime.today(),
        'reciba_id': self.id,
        'move_ids_without_package': [(0,0,{
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'product_uom_qty': self.net_weight,
            'quantity_done': self.net_weight,
            'product_uom': self.product_id.uom_po_id.id,
            'purchase_line_id': self.purchase_id.order_line[0].id,
            'to_refund': True})]
        }
        picking = self.env['stock.picking'].create(values)
        picking.state = 'done'
        self.purchase_id.order_line[0].qty_received = self.purchase_id.order_line[0].qty_received-self.net_weight
        self.transfer_reverse_id = picking.id
        self.transfer_reverse_count += 1
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
            'tare_weight': self.tare_weight
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
        action = self.env.ref('wobin_reciba.tickets_reception')
        result = action.read()[0]
        result['domain'] = [('id','=', self.ticket_id.id)]
        return result

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
