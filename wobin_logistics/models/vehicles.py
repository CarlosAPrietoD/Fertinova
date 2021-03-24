# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WobinVehicles(models.Model):
    _name = 'wobin.logistica.vehicles'
    _description = 'Logistics Vehicles'
    _inherit     = ['mail.thread', 'mail.activity.mixin']  
        

    name  = fields.Char(track_visibility='always')
    model = fields.Char(string='Model', track_visibility='always')
    year  = fields.Integer(string='Year')
    current_trip      = fields.Many2one('wobin.logistica.trips', string='Trip', track_visibility='always')
    analytic_accnt_id = fields.Many2one('account.analytic.account', string='Analytic Account', track_visibility='always')
    trip_history      = fields.One2many('wobin.logistica.trips', 'vehicle_id', string='Trips History')
    state             = fields.Selection(selection=[('in_use', 'In Use'),
                                                    ('without_charge', 'Whitout Charge')], 
                                                    string='State', required=True, readonly=True, copy=False, tracking=True, default='without_charge', compute="set_state", track_visibility='always')