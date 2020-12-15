from odoo import models, fields, api
from datetime import date, datetime
from odoo.exceptions import UserError

class RecibaTicket(models.Model):
    _name = 'reciba.ticket'
    _description = 'Boletas'
    
    @api.model
    def _default_location(self):
        location = self.env['stock.location'].search([('name','ilike','Proveedores')], limit=1).id
        return location

    @api.one
    @api.depends('humidity')
    def _get_humidity_discount(self):
        if self.apply_discount == True:
            if self.humidity:
                if self.humidity > 14:
                    self.humidity_discount = ((self.humidity-14)*1.16)/100*1000
        else:
            self.humidity_discount = 0

    @api.one
    @api.depends('impurity')
    def _get_impurity_discount(self):
        if self.apply_discount == True:
            if self.impurity:
                if self.impurity > 2:
                    self.impurity_discount = (self.impurity-2)/100*1000
        else:
            self.impurity_discount=0

    @api.one
    @api.depends('humidity', 'net_weight')
    def _get_humidity_total_discount(self):
        if self.apply_discount == True:
            if self.humidity:
                if self.humidity > 14:
                    self.humidity_total_discount = ((self.humidity-14)*1.16)/100*self.net_weight
        else: self.humidity_total_discount = 0

    @api.one
    @api.depends('impurity', 'net_weight')
    def _get_impurity_total_discount(self):
        if self.apply_discount == True:
            if self.impurity:
                if self.impurity > 2:
                    self.impurity_total_discount = (self.impurity-2)/100*self.net_weight
        else:
            self.impurity_total_discount = 0
    
             
    @api.one
    @api.depends('gross_weight')
    def _default_gross_date(self):
        if self.gross_weight:
            today = datetime.today()
            self.gross_date = today

    @api.one
    @api.depends('provider_location_id')
    def _default_provider_date(self):
        if self.provider_location_id:
            today = datetime.today()
            self.provider_date = today

    @api.one
    @api.depends('location_id')
    def _default_location_date(self):
        if self.location_id:
            today = datetime.today()
            self.location_date = today

    @api.one
    @api.depends('tare_weight')
    def _default_tare_date(self):
        if self.tare_weight:
            today = datetime.today()
            self.tare_date = today


    @api.one
    @api.depends('net_weight')
    def _default_net_date(self):
        if self.net_weight:
            today = datetime.today()
            self.net_date = today

    @api.one
    @api.depends('gross_weight', 'tare_weight')
    def _default_net_weight(self):
        if self.gross_weight and self.tare_weight:
            if self.operation_type == 'in':
                self.net_weight = self.gross_weight-self.tare_weight
            else:
                self.net_weight = (self.gross_weight-self.tare_weight)*-1

    @api.one
    @api.depends('price', 'net_weight')
    def _calcule_sub(self):
        if self.price and self.net_weight:
            self.sub = self.price*self.net_weight

    @api.one
    @api.depends('humidity_total_discount', 'impurity_total_discount')
    def _get_discount_total(self):
        self.discount = self.humidity_total_discount+self.impurity_total_discount

    @api.one
    @api.depends('net_weight', 'discount')
    def _get_total_weight(self):
        self.total_weight = self.net_weight-self.discount

    @api.one
    @api.depends('total_weight', 'price')
    def _get_total(self):
        self.total = self.total_weight*self.price

    
    @api.one
    @api.depends('params_id')
    def _get_total_damage(self):
        total = 0

        for data in self.params_id:
            if data.quality_params_id.damage:
                total += data.value

        self.sum_damage = total

    
    @api.one
    @api.depends('params_id')
    def _get_total_broken(self):
        total = 0

        for data in self.params_id:
            if data.quality_params_id.broken:
                total += data.value

        self.sum_broken = total

    

    state = fields.Selection([('draft', 'Borrador'),
    ('confirmed', 'Relacionado a un pedido'), 
    ('invoiced','Facturado'),
    ('cancel', 'Cancelado')], default='draft')
    
    operation_type = fields.Selection([('in','Recepción'),
    ('out','Entrega')], string="Tipo de operacion", default="in", required=True)
    name = fields.Char(string="Boleta", default="Boleta Borrador")
    date = fields.Datetime(string="Fecha y hora", default=lambda self: fields.datetime.now())
    weigher = fields.Char(string="Nombre del analista")
    company_id = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('your.module'))
    partner_id = fields.Many2one('res.partner', domain="[('company_id','=',company_id)]", string="Contacto")
    product_id = fields.Many2one('product.product', string="Producto")

    quality_id = fields.Many2one('reciba.quality', string="Norma de calidad", domain="[('product_id', '=', product_id)]")
    humidity = fields.Float(string="Humedad 14%")
    humidity_discount = fields.Float(string="Descuento (Kg)", compute='_get_humidity_discount', store=True)
    impurity = fields.Float(string="Impureza 2%")
    impurity_discount = fields.Float(string="Descuento (Kg)", compute='_get_impurity_discount', store=True)
    density = fields.Float(string="Densidad g/L 720-1000")
    temperature = fields.Float(string="Temperatura °C")
    params_id = fields.One2many('reciba.ticket.params', 'ticket_id')
    sum_damage = fields.Float(string="Suma daños", compute='_get_total_damage', store=True)
    sum_broken = fields.Float(string="Suma quebrados", compute='_get_total_broken', store=True)
    

    driver = fields.Char(string="Nombre del operador")
    type_vehicle = fields.Selection([('van','Camioneta'),
    ('torton','Torton'),
    ('trailer', 'Trailer sencillo'),
    ('full','Trailer full')], string="Tipo de vehiculo")
    plate_vehicle = fields.Char(string="Placas unidad")
    plate_trailer = fields.Char(string="Placas remolque")
    plate_second_trailer = fields.Char(string="Placas segundo remolque")

    delivery = fields.Selection
    reception = fields.Selection([('price', 'Con precio'),
    ('priceless', 'Sin precio')], string="Tipo de recepción", default="priceless")
    
    provider_location_id = fields.Many2one('stock.location', string="Ubicación origen", default=_default_location)
    provider_date = fields.Datetime(string="Fecha y hora", compute='_default_provider_date', store=True)
    location_id = fields.Many2one('stock.location', string="Ubicación destino")
    location_date = fields.Datetime(string="Fecha y hora", compute='_default_location_date', store=True)
    gross_weight = fields.Float(string="Peso Bruto")
    gross_date = fields.Datetime(string="Fecha y hora", compute='_default_gross_date', store=True)
    tare_weight = fields.Float(string="Peso Tara")
    tare_date = fields.Datetime(string="Fecha y hora", compute='_default_tare_date', store=True)
    net_weight = fields.Float(string="Peso Neto", compute='_default_net_weight', store=True)
    net_date = fields.Datetime(string="Fecha y hora", compute='_default_net_date', store=True)
    net_expected = fields.Float(string="Peso neto esperado") 
    
    apply_discount = fields.Boolean(string="Aplicar descuento", default=True)
    humidity_total_discount = fields.Float(string="Descuento total de humedad (Kg)", compute='_get_humidity_total_discount', store=True)
    impurity_total_discount = fields.Float(string="Descuento total de impureza (Kg)", compute='_get_impurity_total_discount', store=True)
    price = fields.Float(string="Precio", digits=(15,4))
    price_flag = fields.Boolean(default=False)
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env['res.company']._company_default_get('your.module').currency_id, string="Moneda")
    
    
    sub = fields.Monetary(string="Importe PN", compute='_calcule_sub', store=True)
    discount = fields.Float(string="Descuento total (kg)", compute='_get_discount_total', store=True)
    total_weight = fields.Float(string="Peso neto analizado", compute='_get_total_weight', store=True)
    total = fields.Monetary(string="Importe PNA", compute='_get_total', store=True)

    picking_id = fields.Many2one('stock.picking', string="Transferencia")
    po_id = fields.Many2one('purchase.order', string="Orden de Compra")
    so_id = fields.Many2one('sale.order', string="Orden de Venta")


    @api.onchange('product_id')
    def product_onchange(self):
        if self.product_id.name == 'MAIZ GRANEL':
            quality = self.env['reciba.quality'].search([('name','=','PROY-NMX-FF-034-SCFI-2019 (Grado II)')], limit=1).id
            self.quality_id = quality


    @api.onchange('so_id')
    def so_onchange(self):
        if self.so_id:
            self.product_id = self.so_id.order_line[0].product_id.id
            self.net_expected = self.so_id.order_line[0].product_uom_qty - self.so_id.order_line[0].qty_delivered

    @api.onchange('quality_id')
    def get_quality_params(self):
        self.params_id = None
        
        if self.quality_id:
            array_params = []
            
            for param in self.quality_id.params:
                array_params.append((0,0,{'quality_params_id':param.id, 'name': param.name, }))
            
            self.params_id = array_params  

    @api.onchange('apply_discount')
    def onchange_apply_discount(self):
        self.humidity = self.humidity
        self.impurity = self.impurity


    @api.onchange('operation_type')
    def onchange_operation_type(self):
        if self.operation_type == 'in':
            location = self.env['stock.location'].search([('name','ilike','Proveedores')], limit=1).id
            self.provider_location_id=location
            self.location_id = False
        else:
            location = self.env['stock.location'].search([('name','ilike','Clientes')], limit=1).id
            self.provider_location_id=False
            self.location_id = location

    
    def confirm_reciba(self):

        if self.net_weight == 0:
            msg = 'El peso neto ingresado no es valido'
            raise UserError(msg)

        if self.humidity == 0 or self.impurity == 0 or self.temperature == 0:
            msg = 'Los valores de humedad, impureza y temperatura deben ser mayores a 0'
            raise UserError(msg)

        if self.operation_type == 'in':
            if self.location_id:
                tickets = self.env['reciba.ticket'].search(['&',('name','ilike',self.location_id.display_name),('state','=','confirmed')], order="id desc",limit=1)
                if tickets:
                    name_location = self.location_id.display_name
                    if tickets.name:
                        number = str(int(tickets.name[-4:])+1).zfill(4)
                        self.name=name_location + '/' + number
                else:
                    self.name = self.location_id.display_name + '/' + '0001'
        
        elif self.operation_type == 'out':
            if self.provider_location_id:
                tickets = self.env['reciba.ticket'].search(['&',('name','ilike',self.provider_location_id.display_name),('state','=','confirmed')], order="id desc",limit=1)
                if tickets:
                    name_location = self.provider_location_id.display_name
                    if tickets.name:
                        number = str(int(tickets.name[-4:])+1).zfill(4)
                        self.name=name_location + '/' + number
                else:
                    self.name = self.provider_location_id.display_name + '/' + '0001'

        
        if self.reception == 'priceless' and self.operation_type == 'in':
            picking_type = self.env['stock.picking.type'].search(['|',('name','=','Recepciones'),('name','=','Receipts'),('default_location_dest_id.name','=',self.location_id.location_id.name)], limit=1)
            
            values={
            'picking_type_id': picking_type.id,
            'location_id': self.provider_location_id.id,
            'location_dest_id' : self.location_id.id,
            'scheduled_date': datetime.today(),
            'reciba_id': self.id,
            'move_ids_without_package': [(0,0,{
                'name': self.product_id.name,
                'product_id': self.product_id.id,
                'product_uom_qty': self.net_weight,
                'product_uom': self.product_id.uom_po_id.id,
                'reciba_id': self.id
            })]}
            picking = self.env['stock.picking'].create(values)
            picking.state = 'confirmed'
            self.picking_id = picking.id

        self.state='confirmed'

    
    def create_transfer(self):
        picking_type = self.env['stock.picking.type'].search(['|',('name','=','Órdenes de entrega'),('name','=','Delivery Orders'),('default_location_dest_id.name','=',self.provider_location_id.location_id.name)], limit=1)  

        values={
        'picking_type_id': picking_type.id,
        'location_id': self.provider_location_id.id,
        'location_dest_id' : self.location_id.id,
        'scheduled_date': datetime.today(),
        'reciba_id': self.id,
        'sale_id': self.so_id.id,
        'origin': self.so_id.name,
        'partner_id': self.partner_id.id,
        'move_ids_without_package': [(0,0,{
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'product_uom_qty': (self.net_weight)*-1,
            'product_uom': self.product_id.uom_po_id.id,
            'sale_line_id': self.so_id.order_line[0].id
        })]}
        picking = self.env['stock.picking'].create(values)
        
        self.picking_id = picking.id

    
    def cancel_reciba(self):
        self.state='cancel'


    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        ticket = super(RecibaTicket, self).copy(default)
        
        ticket.name = "Boleta Borrador"
        ticket.state = 'draft'
        ticket.price_flag = False
        ticket.picking_id = 0
        ticket.po_id = 0

        if ticket.quality_id:
            array_params = []
            
            for n,param in enumerate(self.params_id):
                array_params.append((0,0,{'quality_params_id':param.quality_params_id.id, 'value': param.value }))
            
            ticket.params_id = array_params
        
        return ticket


    @api.onchange('reception')
    def get_reception_change(self):
        if self.reception != 'price':
            self.price = 0

    
    @api.onchange('type_vehicle')
    def get_type_vehicle(self):
        self.plate_trailer = ''
        self.plate_second_trailer = ''


    @api.multi
    def write(self, values):
        ticket = super(RecibaTicket, self).write(values)

        if self.state == 'confirmed' and self.price > 0 and self.picking_id:
                self.picking_id.unlink()

        if self.reception == 'price' and self.price > 0 and self.price_flag == False:
            self.price_flag = True
            
        return ticket

    @api.multi
    def unlink(self):
        if self.state != 'draft':
            msg = 'No se pueden eliminar boletas confirmadas'
            raise UserError(msg)
        ticket = super(RecibaTicket, self).unlink()
        return ticket


    def create_purchase_order(self):
        #picking_type = self.env['stock.picking.type'].search(['|',('name','ilike','Recepciones'),('name','ilike','Receipts')], limit=1)
        payment = self.env['account.payment.term'].search([('name','ilike','PUE')], limit=1)
        analytic_account = self.env['account.analytic.account'].search([('name','ilike','POR ASIGNAR')], limit=1)
        uom = self.env['uom.uom'].search([('name','ilike','kg')], limit=1)
        discount = self.env['product.product'].search([('name','ilike','Descuento sobre compra')], limit=1)
        picking_type = self.env['stock.picking.type'].search(['|',('name','ilike','Recepciones'),('name','ilike','Receipts'),('default_location_dest_id.name','=',self.location_id.location_id.name)], limit=1)

        values={
            'partner_id': self.partner_id.id,
            'picking_type_id': picking_type.id,
            'partner_ref': self.name,
            'payment_term_id': payment.id
        }  
        purchase = self.env['purchase.order'].create(values)

        description = self.product_id.name
        if self.product_id.default_code:
            description = "["+self.product_id.default_code+"] "+self.product_id.name
        
        purchase.order_line=[(0,0,{
                'product_id': self.product_id.id,
                'name': description,
                'date_planned': purchase.date_order,
                'account_analytic_id': analytic_account.id,
                'product_qty': self.net_weight,
                'price_unit': self.price,
                'product_uom': self.product_id.uom_po_id.id
            }),
            (0,0,{
                'product_id': discount.id,
                'name': "Descuento por calidad",
                'date_planned': purchase.date_order,
                'account_analytic_id': analytic_account.id,
                'product_qty': self.discount,
                'price_unit': self.price*-1,
                'product_uom': discount.uom_po_id.id
            })]

        self.po_id = purchase.id



class RecibaTicketParams(models.Model):
    _name = 'reciba.ticket.params'
    _description = 'Boletas'

    ticket_id = fields.Many2one('reciba.ticket')
    quality_params_id = fields.Many2one('reciba.quality.params', 'Parametro de calidad')
    max_value = fields.Float(related='quality_params_id.value', string="Máximo")
    unit = fields.Char(related='quality_params_id.unit', string="Unidad de medida")
    value = fields.Float(string="Valor")


class RecibaQuality(models.Model):
    _name = 'reciba.quality'
    _description = 'Parametros de calidad'

    name = fields.Char(string="Norma")
    product_id = fields.Many2one('product.product', string="Producto")
    params = fields.One2many('reciba.quality.params', 'quality_id')


class RecibaQualityParams(models.Model):
    _name = 'reciba.quality.params'
    _description = 'Parametros de calidad de Reciba'

    name = fields.Char(string="Nombre")
    quality_id = fields.Many2one('reciba.quality')
    value = fields.Float(string="Máximo")
    unit = fields.Char(string="Unidad de medida")
    damage = fields.Boolean(string="Sumar daño")
    broken = fields.Boolean(string="Sumar quebrado")


class ReportRecibaTicket(models.AbstractModel):
    _name = 'report.reciba.report_ticket'

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
    _name = 'report.reciba.report_ticket_priceless'


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




class StockPicking(models.Model):
    _inherit='stock.picking'
    
    x_studio_aplica_flete= fields.Boolean()
    reciba_id = fields.Many2one('reciba.ticket', string="Boleta de análisis")
    
    
    
    def create_reciba(self):
        
        values={
            'state': 'draft',
            'operation_type': 'out',
            'name': 'Boleta Borrador',
            'partner_id': self.partner_id.id,
            'product_id': self.move_ids_without_package[0].product_id.id,
            'provider_location_id': self.location_id.id,
            'location_id' : self.location_dest_id.id,
            'scheduled_date': datetime.today(),
            'so_id': self.sale_id.id,
            'net_expected': self.move_ids_without_package[0].quantity_done,
            'picking_id': self.id,
            'reception': 'priceless'}
        
        ticket = self.env['reciba.ticket'].create(values)

        self.reciba_id = ticket.id
