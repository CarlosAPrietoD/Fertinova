# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WobinVehicles(models.Model):
    _name = 'wobin.logistica.vehicles'
    _description = 'Logistics Vehicles'
    _inherit     = ['mail.thread', 'mail.activity.mixin']  



    @api.one
    def _set_history(self):
        list_history = self.env['wobin_logistica_trips'].search([('vehicle_id', '=', self.id)]).ids
        
        if list_history:
            self.trip_history = list_history



    name  = fields.Char(track_visibility='always')
    mark  = fields.Char(string='Mark', track_visibility='always')
    model = fields.Char(string='Model', track_visibility='always')
    year  = fields.Char(string='Year', track_visibility='always')
    description = fields.Char(string='Description', track_visibility='always')
    series      = fields.Char(string='Series', track_visibility='always')
    license_plate     = fields.Char(string='License Plate', track_visibility='always') 
    current_trip      = fields.Many2one('wobin.logistica.trips', string='Current Trip', compute="_set_current_trip", track_visibility='always')
    analytic_accnt_id = fields.Many2one('account.analytic.account', string='Analytic Account', track_visibility='always')
    trip_history      = fields.One2many('wobin.logistica.trips', 'vehicle_id', string='Trips History', default=_set_history)
    state             = fields.Selection(selection=[('in_use', 'In Use'),
                                                    ('without_charge', 'Whitout Charge')], 
                                                    string='State', required=True, readonly=True, copy=False, tracking=True, default='without_charge', compute="_set_state", track_visibility='always')
    company_id = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('your.module'))                                                    


    @api.one
    def _set_state(self):
        if self.current_trip:
            self.state = 'in_use'
        else:
            self.state = 'without_charge'

        

    @api.one
    def _set_current_trip(self):        
        sql_query = """SELECT wl.id, wl.state_aux
                         FROM wobin_logistica_trips AS wl
                        WHERE vehicle_id = %s
                        ORDER BY create_date DESC
                        LIMIT 1;"""
        self.env.cr.execute(sql_query, (self.id,))
        result = self.env.cr.fetchone()

        if result:   
            if result[1] != 'discharged': 
                self.current_trip = result[0]
            else:                
                self.current_trip = None