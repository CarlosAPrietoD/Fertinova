# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp
 
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   PRACTICE    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class Quotations(models.Model):
    _name = "crm.quotations"
    _description = "Quotations"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']    

    quotation_id       = fields.Integer(string='ID')
    name               = fields.Char(string='No. Cotización')
    client             = fields.Char(string='Cliente')
    unique_quotation   = fields.Boolean(string='Tipo de Cotización')
    contract_quotation = fields.Boolean(string='Tipo de Cotización')
    volume             = fields.Float(string='Volumen', digits=dp.get_precision('Product Unit of Measure'))
    quotation_lines    = fields.One2many('crm.quotations.lines', 'quotation_line_id', string="Líneas")



class QuotationsLines(models.Model):
    _name = "crm.quotations.lines"
    _description = "Quotations Lines"

    quotation_line_id     = fields.Many2one('purchase.order.line', string='ID')
    trip_number           = fields.Integer(string='Número de viaje')
    origin                = fields.Char(string='Origen')
    destiny               = fields.Char(string='Destino')
    kilometers            = fields.Char(string='Kms')
    cycle                 = fields.Char(string='Ciclo')
    tariff                = fields.Char(string='Tarifa')
    tnl                   = fields.Char(string='TNL.')
    importe               = fields.Char(string='Importe')	
    liters                = fields.Char(string='Litros') 
    fuel                  = fields.Char(string='Combustible') 
    estimated             = fields.Char(string='Estimado')	
    performance_average   = fields.Char(string='Promedio de desempeño')
    circuit_days          = fields.Char(string='Días de Circuito')	
    sueldo_op             = fields.Char(string='Sueldo op.')	 
    diesel_price          = fields.Char(string='Precio Diesel') 	 
    fuel_km               = fields.Char(string='Combustible ($/KMs)')
    highways_fee          = fields.Char(string='Cuotas de autopista') 	
    estimated_urea_liters = fields.Char(string='Estimado de litros de UREA') 
    performance_average2  = fields.Char(string='Promedio de desempeño')
    urea                  = fields.Char(string='UREA') 	 
    rentability           = fields.Char(string='Rentabilidad')  	
    daily_rentability     = fields.Char(string='Rentabilidad Diaria')
    state                 = fields.Char(string='Estado')
    delivery_percentage   = fields.Float(string='Porcentaje de Entrega', digits=dp.get_precision('Product Unit of Measure'))    

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   PRACTICE    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
