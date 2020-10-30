# -*- coding: utf-8 -*-
import datetime
import pytz
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class RecibaPrestamos(models.Model):
    _name = 'reciba.prestamos'
    _description = 'Préstamos de Reciba'
    _inherit = ['mail.thread', 'mail.activity.mixin']      

    @api.model
    def create(self, vals):                        
        #Change of sequence (if it isn't stored is shown "New" else e.g PRES000001)  
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'self.prestamo') or 'Nuevo'               
        result = super(RecibaPrestamos, self).create(vals)
        return result    


    def _set_hora_mx(self):
        #Get User Timezone e.g. MEXICO/GENERAL:
        user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        #Obtain current system time:
        time_system_current = fields.datetime.now()     
        #Convert system time into mexican time:   
        time_converted = pytz.utc.localize(time_system_current).astimezone(user_timezone)  
        hora_prestamo_aux = time_converted.strftime('%H:%M:%S')
        return hora_prestamo_aux


    name            = fields.Char(string="Préstamo", readonly=True, required=True, copy=False, default='Nuevo') 
    tipo            = fields.Char(string='Tipo', default='Préstamo')
    contacto_id     = fields.Many2one('res.partner', string='Contacto')
    limite_prestamo = fields.Float(string='Límite de Préstamos', digits=dp.get_precision('Product Unit of Measure'))   
    fecha_prestamo  = fields.Date(string='Fecha de Préstamo')
    hora_prestamo   = fields.Char(string='Hora de Préstamo', default=_set_hora_mx)
    fecha_cobro     = fields.Date(string='Fecha de Cobro')
    hora_cobro      = fields.Char(string='Hora de Cobro')    
    cantidad        = fields.Float(string='Cantidad', digits=dp.get_precision('Product Unit of Measure'))   
    observaciones   = fields.Html('Observaciones')
    estado          = fields.Selection(selection=[('open', 'Abierto'),
                                                  ('settled', 'Saldado')], 
                                                string='Status', required=True, readonly=True, copy=False, track_visibility='onchange', default='open')


    def marcar_saldado(self):
        #Set up "settled" state:
        self.estado = 'settled'        
        #Get User Timezone e.g. MEXICO/GENERAL:
        user_timezone = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        #Obtain current system time:
        time_system_current = fields.datetime.now()     
        #Convert system time into mexican time:   
        time_converted = pytz.utc.localize(time_system_current).astimezone(user_timezone)  
        fecha_cobro_aux = time_converted.strftime('%Y-%m-%d')
        self.fecha_cobro = fecha_cobro_aux
        hora_cobro_aux = time_converted.strftime('%H:%M:%S')        
        self.hora_cobro = hora_cobro_aux


    def cancelar(self):
        self.estado = 'open'   
        self.fecha_cobro = ''       
        self.hora_cobro = ''             