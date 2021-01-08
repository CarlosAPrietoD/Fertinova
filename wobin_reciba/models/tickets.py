from odoo import models, fields, api
from datetime import date, datetime
from odoo.exceptions import UserError

class RecibaTicket(models.Model):
    #Boletas
    _name = 'reciba.ticket'
    _description = 'Boletas'

    state = fields.Selection([('draft', 'Borrador'),
    ('confirmed', 'Confirmado')], default='draft')
    picking_id = fields.Many2one('stock.picking', string="Transferencia")

    #-------------------------------------Datos generales----------------------------------
    name = fields.Char(string="Boleta")
    date = fields.Datetime(string="Fecha y hora")
    operation_type_id = fields.Many2one('stock.picking.type', string="Tipo de operacion")
    transfer_type = fields.Selection([('int', 'Misma sucursal'),
    ('in', 'Entrada'), 
    ('out','Salida')], string="Tipo de transferencia")
    weigher = fields.Char(string="Nombre del analista")
    product_id = fields.Many2one('product.product', string="Producto")
    ticket_id = fields.Many2one('wreciba.ticket', string="Boleta relacionada")
    sale_id = fields.Many2one('sale.order', string="Orden de venta")
    purchase_id = fields.Many2one('purchase.order', string="Pedido de compra")
    partner_id = fields.Many2one('res.partner', string="Contacto")
    list_production_id = fields.Many2one('mrp.bom', string="Lista de materiales")
    qty_produce = fields.Float(string="Cantidad a producir")
    qty_process = fields.Float(string="Cantidad a procesar")
    
    #------------------------------------Datos de calidad---------------------------------
    quality_id = fields.Many2one('reciba.quality', string="Norma de calidad")
    humidity = fields.Float(string="Humedad 14%")
    humidity_discount = fields.Float(string="Descuento (Kg)")
    impurity = fields.Float(string="Impureza 2%")
    impurity_discount = fields.Float(string="Descuento (Kg)")
    density = fields.Float(string="Densidad g/L 720-1000")
    temperature = fields.Float(string="Temperatura °C")
    params_id = fields.One2many('reciba.ticket.params', 'ticket_id')
    sum_damage = fields.Float(string="Suma daños")
    sum_broken = fields.Float(string="Suma quebrados")

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
    provider_location_id = fields.Many2one('stock.location', string="Ubicación origen")
    provider_date = fields.Datetime(string="Fecha y hora")
    location_id = fields.Many2one('stock.location', string="Ubicación destino")
    location_date = fields.Datetime(string="Fecha y hora")

    #-----------------------------------Datos de pesaje----------------------------------
    reception = fields.Selection([('price', 'Con precio'),
    ('priceless', 'Sin precio')], string="Tipo de recepción")
    gross_weight = fields.Float(string="Peso Bruto")
    gross_date = fields.Datetime(string="Fecha y hora")
    tare_weight = fields.Float(string="Peso Tara")
    tare_date = fields.Datetime(string="Fecha y hora")
    net_weight = fields.Float(string="Peso Neto")
    net_date = fields.Datetime(string="Fecha y hora")

    #----------------------------------Datos de descuento-------------------------------
    apply_discount = fields.Boolean(string="Aplicar descuento")
    humidity_total_discount = fields.Float(string="Descuento total de humedad (Kg)")
    impurity_total_discount = fields.Float(string="Descuento total de impureza (Kg)")
    discount = fields.Float(string="Descuento total (kg)")
    total_weight = fields.Float(string="Peso neto analizado")
    price = fields.Float(string="Precio", digits=(15,4))
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env['res.company']._company_default_get('your.module').currency_id, string="Moneda")


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