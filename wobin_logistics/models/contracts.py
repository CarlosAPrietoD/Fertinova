# -*- coding: utf-8 -*-
import operator    
from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp

import logging
import warnings
_logger = logging.getLogger(__name__)   

class WobinLogisticaRoutes(models.Model):
    _name = 'wobin.logistica.routes'
    _description = 'Logistics Routes'

    name = fields.Char(string="City to add for origins & destinations")
    company_id = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('your.module'))



class WobinLogisticaContracts(models.Model):
    _name = 'wobin.logistica.contracts'
    _description = 'Logistics Contracts'
    _inherit     = ['mail.thread', 'mail.activity.mixin']   

    @api.model
    def create(self, vals):                        
        #Change of sequence (if it isn't stored is shown "New" else e.g CONTR000005)  
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'self.contract') or 'New'               
        result = super(WobinLogisticaContracts, self).create(vals)
        return result    

    name            = fields.Char(string="Contract", readonly=True, required=True, copy=False, default='New')
    client_id       = fields.Many2one('res.partner', string='Client')
    product_id      = fields.Char(string="Product")
    covenant_qty    = fields.Float(string='Covenanted Quantity (kg)', digits=dp.get_precision('Product Unit of Measure'))
    tariff          = fields.Float(string='Tariff $', digits=dp.get_precision('Product Unit of Measure'))
    expected_income = fields.Float(string='Expected Income $', readonly=True, digits=dp.get_precision('Product Unit of Measure'), compute='_set_expected_income')
    origin_id       = fields.Many2one('wobin.logistica.routes', string='Origin')
    destination_id  = fields.Many2one('wobin.logistica.routes', string='Destination')
    remitter        = fields.Char(string='Remitter')
    recipient       = fields.Char(string='Recipient')
    shipping        = fields.Char(string='Shipping')
    observations    = fields.Html('Observations')
    status          = fields.Selection(selection=[('active', 'Active'),
                                                  ('close', 'Closed'),
                                                 ], string='State', required=True, readonly=True, copy=False, tracking=True, default='active', track_visibility='always')    
    # -- These fields were created for analysis not to be shown in main view of contracts -- #
    company_id         = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('your.module'))
    trips              = fields.Char(string='Trips', compute='_set_trips')
    trip_delivered_qty = fields.Float(string='Trip Delivered Qty', digits=dp.get_precision('Product Unit of Measure'), compute='_set_trp_del_qty')
    difference_qty     = fields.Float(string='Difference Qty', digits=dp.get_precision('Product Unit of Measure'), compute='_set_dif_qty')
    trip_status        =  fields.Selection([('to_do', 'To Do'),
                                            ('doing', 'Doing'),
                                            ('done', 'Done'),
                                           ], string='Supply Contract Status', index=True, readonly=True, default='to_do', copy=False, compute='_set_trip_status')    

    
    @api.one
    @api.depends('covenant_qty', 'tariff')
    def _set_expected_income(self):
        self.expected_income = self.covenant_qty * self.tariff


    def create_trip(self):
        """This method intends to display a Form View of Trips"""
        #action_id = self.env['ir.model.data'].xmlid_to_res_id('wobin_logistics.view_logistics_trips_form', 
        return {
            #'name':_("Products to Process"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'wobin.logistica.trips',
            #'res_id': partial_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': '[]',
            'context': {'default_contracts_id': self.id}
        }


    @api.one
    @api.depends('name')
    def _set_trips(self):
        '''This method intends to show in a single row multiple 
           trips assigned to a given contract'''
        trips_lst = []
            
        sql_query = """SELECT name 
                         FROM wobin_logistica_trips 
                        WHERE contracts_id = %s;"""
        self.env.cr.execute(sql_query, (self.id,))
        result = self.env.cr.fetchall()  

        if result:                    
            for trip in result:
                if trip[0]:
                    trips_lst.append(trip[0])                    
            self.trips = ', '.join(trips_lst)
        else:
            self.trips = ""     


    @api.one
    @api.depends('name')
    def _set_trp_del_qty(self):
        '''This method intends to sum all discharges of multiple 
           trips assigned to a given contract'''
        sql_query = """SELECT sum(real_upload_qty) 
                         FROM wobin_logistica_trips 
                        WHERE contracts_id = %s"""
        self.env.cr.execute(sql_query, (self.id,))
        result = self.env.cr.fetchone()

        if result:                    
            self.trip_delivered_qty = result[0]



    @api.one    
    @api.depends('name')
    def _set_dif_qty(self):
        '''This method intends to show the difference between delivered qty 
           and discharged qty assigned to a given sale order'''
        self.difference_qty = self.covenant_qty - self.trip_delivered_qty



    @api.one
    def _set_trip_status(self):
        trips_related_lst = []
        covenant_qty = 0.0

        trips_related_lst = self.env['wobin.logistica.trips'].search([('contracts_id', '=', self.id)]).ids

        if not trips_related_lst:
            self.trip_status = 'to_do'
        else: 
            for trip in trips_related_lst:
                covenant_qty += self.env['wobin.logistica.trips'].search([('id', '=', trip)]).real_download_qty

            if covenant_qty == self.covenant_qty:
                self.trip_status = 'done'
            else:
                self.trip_status = 'doing'


    def close_contract(self):
        self.status = 'close'