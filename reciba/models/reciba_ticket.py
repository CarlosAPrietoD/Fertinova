from odoo import models, fields, api
from datetime import date, datetime

class RecibaTicket(models.Model):
    _name = 'reciba.ticket'
    _description = 'Boletas'

    @api.model
    def _default_currency(self):
        return self.env.ref('base.main_company').currency_id


    
    @api.model
    def _default_number(self):
        tickets = self.env['reciba.ticket'].search([])
        return len(tickets)+1

    @api.one
    @api.depends('humidity')
    def _get_humidity_discount(self):
        if self.humidity:
            if self.humidity > 14.5:
                self.humidity_discount = ((self.humidity-14.5)*1.16)/100*1000

    @api.one
    @api.depends('impurity')
    def _get_impurity_discount(self):
        if self.impurity:
            if self.impurity > 2:
                self.impurity_discount = (self.impurity-2)/100*1000

    @api.one
    @api.depends('humidity', 'net_weight')
    def _get_humidity_total_discount(self):
        if self.humidity:
            if self.humidity > 14.5:
                self.humidity_total_discount = ((self.humidity-14.5)*1.16)/100*self.net_weight

    @api.one
    @api.depends('impurity', 'net_weight')
    def _get_impurity_total_discount(self):
        if self.impurity:
            if self.impurity > 2:
                self.impurity_total_discount = (self.impurity-2)/100*self.net_weight
                
    @api.one
    @api.depends('gross_weight')
    def _default_gross_date(self):
        if self.gross_weight:
            today = datetime.today()
            self.gross_date = today

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
            self.net_weight = self.gross_weight-self.tare_weight

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
    

    state = fields.Selection([('draft', 'Borrador'),
    ('confirmed', 'Por facturar'), 
    ('invoiced','Facturado'),
    ('cancel', 'Cancelado')], default='draft')
    
    name = fields.Char(string="Boleta", default="Boleta Borrador")
    #number = fields.Integer(string="Boleta No.", default=_default_number)
    date = fields.Datetime(string="Fecha y hora de llegada", default=lambda self: fields.datetime.now())
    weigher = fields.Char(string="Nombre del analista")
    partner_id = fields.Many2one('res.partner', string="Proveedor")
    product_id = fields.Many2one('product.product', string="Producto")

    quality_id = fields.Many2one('reciba.quality', string="Norma de calidad", domain="[('product_id', '=', product_id)]")
    humidity = fields.Float(string="Humedad 14.5%")
    humidity_discount = fields.Float(string="Descuento (Kg)", compute='_get_humidity_discount')
    impurity = fields.Float(string="Impurity 2%")
    impurity_discount = fields.Float(string="Descuento (Kg)", compute='_get_impurity_discount')
    params_id = fields.One2many('reciba.ticket.params', 'ticket_id')

    driver = fields.Char(string="Nombre del operador")
    type_vehicle = fields.Selection([('van','Camioneta'),
    ('torton','Torton'),
    ('trailer', 'Trailer sencillo'),
    ('full','Trailer full')], string="Tipo de vehiculo")
    plate_vehicle = fields.Char(string="Placas unidad")
    plate_trailer = fields.Char(string="Placas remolque")
    plate_second_trailer = fields.Char(string="Placas segundo remolque")

    reception = fields.Selection([('price', 'Con precio'),
    ('priceless', 'Sin precio')], string="Tipo de recepción")
    
    location_id = fields.Many2one('stock.location', string="Ubicación de descarga")
    location_date = fields.Datetime(string="Fecha y hora", compute='_default_location_date')
    gross_weight = fields.Float(string="Peso bruto")
    gross_date = fields.Datetime(string="Fecha y hora", compute='_default_gross_date')
    tare_weight = fields.Float(string="Peso tara")
    tare_date = fields.Datetime(string="Fecha y hora", compute='_default_tare_date')
    net_weight = fields.Float(string="Peso Neto", compute='_default_net_weight')
    net_date = fields.Datetime(string="Fecha y hora", compute='_default_net_date')
    
    humidity_total_discount = fields.Float(string="Descuento total de humedad (Kg)", compute='_get_humidity_total_discount')
    impurity_total_discount = fields.Float(string="Descuento total de impureza (Kg)", compute='_get_impurity_total_discount')
    price = fields.Monetary(string="Precio")
    currency_id = fields.Many2one('res.currency', default=_default_currency, string="Moneda")
    
    
    sub = fields.Monetary(string="Subtotal", compute='_calcule_sub')
    discount = fields.Float(string="Descuento total (kg)", compute='_get_discount_total')
    total_weight = fields.Float(string="Peso neto analizado", compute='_get_total_weight')
    total = fields.Monetary(string="Total", compute='_get_total')

    picking_id = fields.Many2one('stock.picking', string="Transferencia")


    @api.onchange('quality_id')
    def get_quality_params(self):
        self.params_id = None
        
        if self.quality_id:
            array_params = []
            
            for param in self.quality_id.params:
                array_params.append((0,0,{'quality_params_id':param.id, 'name': param.name, }))
            
            self.params_id = array_params       

    
    def confirm_reciba(self):
        
        if self.location_id:
            tickets = self.env['reciba.ticket'].search(['&',('location_id','=',self.location_id.id),('state','=','confirmed')], order="id desc",limit=1)
            if tickets:
                name_location = self.location_id.name[:2]
                if tickets.name:
                    number = str(int(tickets.name[2:])+1)
                    self.name=name_location.upper()+number
            else:
                self.name = self.location_id.name[:2].upper()+"1"

        
        if self.reception == 'priceless':
            picking_type = self.env['stock.picking.type'].search([('name','ilike','recepciones')], limit=1)
            values={
            'picking_type_id': picking_type.id,
            'location_id': self.location_id,
            'location_dest_id' : self.location_id,
            'scheduled_date': self.date,
            'move_ids_without_package': [(0,0,{
                'name': self.product_id.name,
                'product_id': self.product_id.id,
                'product_uom_qty': self.net_weight,
                'product_uom': 1
                })]}
            picking = self.env['stock.picking'].create(values)

            self.picking_id = picking.id

        


        self.state='confirmed'

    
    def cancel_reciba(self):
        self.state='cancel'


    @api.multi
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        ticket = super(RecibaTicket, self).copy(default)
        
        ticket.name = "Boleta Borrador"
        ticket.state = 'draft'

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

    name = fields.Char(string="Nombre")
    product_id = fields.Many2one('product.product', string="Producto")
    params = fields.One2many('reciba.quality.params', 'quality_id')


class RecibaQualityParams(models.Model):
    _name = 'reciba.quality.params'
    _description = 'Parametros de calidad de Reciba'

    name = fields.Char(string="Nombre")
    quality_id = fields.Many2one('reciba.quality')
    value = fields.Float(string="Máximo")
    unit = fields.Char(string="Unidad de medida")


class ReportRecibaTicket(models.AbstractModel):
    _name = 'report.reciba.report_ticket'

    @api.model
    def _get_report_values(self, docids, data=None): 
        tickets = self.env['reciba.ticket'].browse(docids)

        docs=[]
        for ticket in tickets:
            doc={'ticket': ticket
            }
            docs.append(doc)
            
        
        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': docs
        }     

'''class RecibaTicketWizard(models.TransientModel):
    _name = 'reciba.ticket.wizard'

    def _get_ticket_id(self):
        return self.env['reciba.ticket'].browse(self.env.context.get('active_id'))

    ticket_id = fields.Many2one('reciba.ticket', default=_get_ticket_id)

    def confirm_ticket(self):
        print("==============", self.ticket_id)
        #self.ticket_id.state = 'confirmed' '''
