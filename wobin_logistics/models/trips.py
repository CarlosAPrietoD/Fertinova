# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)     


class LogisticsTrips(models.Model):
    _name        = 'logistics.trips'
    _description = 'Logistics Trips'
    _inherit     = ['mail.thread', 'mail.activity.mixin']        


    @api.model
    def create(self, vals):                  
        '''This method intends to create a sequence for a given trip and a new analytic tag'''         
        tag = self.env['account.analytic.tag'].search([('analytic_tag_type', '=', 'trip')], order="write_date desc", limit=1).name
        _logger.info("\n\n\ntag: %s\n\n\n", tag)
        if tag:
            #Split to get numeric part of string e.g. "V: 005"
            numeric_part = int(tag[3:])
            _logger.info("\n\n\nnumeric_part: %s\n\n\n", numeric_part)
            #Increase number of trip tag:
            tag_to_create = numeric_part + 1        
            #After retrieve the last tag it's important create a new one:
            name_aux = 'V: ' + str(tag_to_create)   
            _logger.info("\n\n\nname_aux: %s\n\n\n", name_aux)     
            values = {
                    'name': name_aux,
                    'analytic_tag_type': 'trip'
                }
            new_tag = self.env['account.analytic.tag'].create(values)
        
        #Change of sequence (if it isn't stored is shown "New" else e.g VJ000005)  
        #if vals.get('name', 'New') == 'New':
        #   vals['name'] = self.env['ir.sequence'].next_by_code(
        #        'self.trip') or 'New'
        #    vals['trip_number_tag'] = name_aux                
        vals['name'] = name_aux 
        vals['trip_number_tag'] = name_aux 
        result = super(LogisticsTrips, self).create(vals)
        return result



    name              = fields.Char(string="Trip", readonly=True, required=True, copy=False, default='New')
    trip_number_tag   = fields.Char(string='Trip Number (Analytic Tag)', track_visibility='always')
    sales_order_id    = fields.Many2one('sale.order', string='Sales Order', track_visibility='always')
    opportunity_id    = fields.Many2one('crm.lead', string='Lead', track_visibility='always')
    client_id         = fields.Many2one('res.partner', string='Client', track_visibility='always')
    vehicle_id        = fields.Many2one('fleet.vehicle', string='Vehicle')    
    analytic_accnt_id = fields.Many2one('account.analytic.account', string='Analytic Account', track_visibility='always')
    operator_id       = fields.Many2one('res.partner',string='Operator', track_visibility='always')
    route_id          = fields.Many2one('account.analytic.tag',string='Route', track_visibility='always', domain=[('analytic_tag_type', '=', "route")])
    advance           = fields.Char(string='Advance', track_visibility='always')
    start_date        = fields.Date(string='Start Date', track_visibility='always')
    upload_date       = fields.Date(string='Upload Date', track_visibility='always')
    estimated_qty     = fields.Float(string='Estimated Quantity', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always')
    real_upload_qty   = fields.Float(string='Real Upload Quantity', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always')
    download_date     = fields.Date(string='Download Date', track_visibility='always')
    real_download_qty = fields.Float(string='Real Download Quantity', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always')
    conformity        = fields.Binary(string='Conformity and Settlement', track_visibility='always')
    checked           = fields.Boolean(string=" ")
    state             = fields.Selection(selection=[('assigned', 'Assigned'),
                                                    ('route', 'En route'),
                                                    ('discharged', 'Discharged')], 
                                                    string='Status', required=True, readonly=True, copy=False, tracking=True, default='assigned', compute="set_status", track_visibility='always')
    
    
    @api.one
    def set_status(self):
        '''Set up state in base a which fields are filled up'''
        if self.trip_number_tag and self.sales_order_id and self.opportunity_id and self.client_id and self.vehicle_id and self.operator_id and self.route_id and self.advance and self.start_date and self.upload_date and self.estimated_qty and self.real_upload_qty and self.download_date and self.real_download_qty and self.conformity and self.checked:
           self.state = 'discharged'
        elif self.trip_number_tag and self.sales_order_id and self.opportunity_id and self.client_id and self.vehicle_id and self.operator_id and self.route_id and self.advance and self.start_date and self.upload_date and self.estimated_qty and self.real_upload_qty:
            self.state = 'route'
        else:
            self.state = 'assigned'

    
    @api.onchange('sales_order_id')
    def _onchange_sales_order(self):
        '''Authomatic assignation for field "client_id" from sales_order's input'''
        self.client_id = self.env['sale.order'].search([('id', '=', self.sales_order_id.id)]).partner_id.id 
         

    @api.onchange('vehicle_id')
    def _onchange_vehicle(self):
        '''Authomatic assignation for fields "operator_id" & "analytic_accnt_id" 
           from driver_id taken from vehicle_id's input'''
        self.operator_id = self.env['fleet.vehicle'].search([('id', '=', self.vehicle_id.id)]).driver_id.id
        self.analytic_accnt_id = self.env['account.analytic.account'].search([('vehicle_id', '=', self.vehicle_id.id)]).id

 


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Aggregation of a new many2one field of Vehicles in Analytic Accounts 
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::  
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle')    




class AccountAnalyticTag(models.Model):
    _inherit = "account.analytic.tag"

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Aggregation of a new selection field in Analytic Tags to manage types
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::       
    analytic_tag_type = fields.Selection([('trip', 'Trip'),
                                          ('route', 'Route'),
                                          ('operator', 'Operator')],
                                         'Analytic Tag Type')                                




class SaleOrder(models.Model):
    _inherit = "sale.order"

    trips              = fields.Char(string='Trips', compute='_set_trips')
    sale_order_qty     = fields.Float(string='Sale Order Qty', digits=dp.get_precision('Product Unit of Measure'), compute='_set_sale_order_qty')
    trip_delivered_qty = fields.Float(string='Trip Delivered Qty', digits=dp.get_precision('Product Unit of Measure'), compute='_set_trip_delivered_qty')
    difference_qty     = fields.Float(string='Difference Qty', digits=dp.get_precision('Product Unit of Measure'), compute='_set_diff_qty')


    @api.one
    @api.depends('name')
    def _set_trips(self):
        '''This method intends to show in a single row multiple 
           trips assigned to a given sale order'''
        trips_lst = []
            
        sql_query = """SELECT trip_number_tag 
                         FROM logistics_trips 
                        WHERE sales_order_id = %s;"""
        self.env.cr.execute(sql_query, (self.id,))
        result = self.env.cr.fetchall()  

        if result:                    
            for trip in result:
                if trip[0]:
                    trips_lst.append(trip[0])                    
            self.trips = ', '.join(trips_lst)
        else:
            self.trips = ""     


    @api.multi      
    @api.depends('name')
    def _set_sale_order_qty(self):
        '''This method intends to sum the value of qty_delivered in sales order lines'''
        for rec in self:
            rec.trip_delivered_qty = sum(line.qty_delivered for line in rec.order_line)  


    @api.one
    @api.depends('name')
    def _set_trip_delivered_qty(self):
        '''This method intends to sum all discharges of multiple 
           trips assigned to a given sales order'''
        sql_query = """SELECT sum(real_download_qty) 
                         FROM logistics_trips 
                        WHERE sales_order_id = %s"""
        self.env.cr.execute(sql_query, (self.id,))
        result = self.env.cr.fetchone()
        _logger.info("\n\n\n result: %s\n\n\n", result)

        if result:                    
            self.trips = result[0]


    @api.one    
    @api.depends('name')
    def _set_diff_qty(self):
        '''This method intends to show the difference between delivered qty 
           and discharged qty assigned to a given sale order'''
        self.difference_qty = self.sale_order_qty - self.trip_delivered_qty