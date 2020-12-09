# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.translate import _

import logging
_logger = logging.getLogger(__name__)     


class LogisticsTrips(models.Model):
    _name        = 'logistics.trips'
    _description = 'Logistics Trips'
    _inherit     = ['mail.thread', 'mail.activity.mixin']        


    @api.model
    def create(self, vals):  
        #Change of sequence (if it isn't stored is shown "New" else e.g VJ000005)  
        if vals.get('name', 'New') == 'New':
           vals['name'] = self.env['ir.sequence'].next_by_code(
                'self.trip') or 'New'
        result = super(LogisticsTrips, self).create(vals)
        return result


    name              = fields.Char(string="Trip", readonly=True, required=True, copy=False, default='New')
    contracts_id      = fields.Many2one('logistics.contracts', string='Contracts', track_visibility='always')
    sales_order_id    = fields.Many2one('sale.order', string='Sales Order', track_visibility='always')
    client_id         = fields.Many2one('res.partner', string='Client', track_visibility='always')
    vehicle_id        = fields.Many2one('fleet.vehicle', string='Vehicle')    
    analytic_accnt_id = fields.Many2one('account.analytic.account', string='Analytic Account', track_visibility='always')
    operator_id       = fields.Many2one('res.partner',string='Operator', track_visibility='always')
    route             = fields.Char(string='Route', track_visibility='always')
    advance_id        = fields.Many2many('hr.expense.sheet',string='Advance', track_visibility='always')
    start_date        = fields.Date(string='Start Date', track_visibility='always')
    upload_date       = fields.Date(string='Upload Date', track_visibility='always')
    estimated_qty     = fields.Float(string='Estimated Quantity', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always')
    real_upload_qty   = fields.Float(string='Real Upload Quantity', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always')
    attachment_upload = fields.Binary(string='Upload Attachments', track_visibility='always')
    download_date     = fields.Date(string='Download Date', track_visibility='always')
    real_download_qty = fields.Float(string='Real Download Quantity', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always')
    attachment_downld = fields.Binary(string='Download Attachments', track_visibility='always')
    conformity        = fields.Binary(string='Conformity and Settlement', track_visibility='always')
    checked           = fields.Boolean(string=" ")
    state             = fields.Selection(selection=[('assigned', 'Assigned'),
                                                    ('route', 'En route'),
                                                    ('discharged', 'Discharged')], 
                                                    string='Status', required=True, readonly=True, copy=False, tracking=True, default='assigned', compute="set_status", track_visibility='always')
    
    
    @api.one
    def set_status(self):
        '''Set up state in base a which fields are filled up'''
        if self.contracts_id and self.sales_order_id and self.client_id and self.vehicle_id and self.analytic_accnt_id and self.operator_id and self.route and self.advance_id and self.start_date and self.upload_date and self.estimated_qty and self.real_upload_qty and self.download_date and self.real_download_qty and self.conformity and self.checked:
           self.state = 'discharged'
        elif self.contracts_id and self.sales_order_id and self.client_id and self.vehicle_id and self.analytic_accnt_id and self.operator_id and self.route and self.advance_id and self.start_date and self.upload_date and self.estimated_qty and self.real_upload_qty:
            self.state = 'route'
        else:
            self.state = 'assigned'


    @api.onchange('contracts_id')
    def _onchange_contract(self):
        '''Authomatic assignation for field "sales_order_id" from contracts_id's input'''
        self.sales_order_id = self.env['logistics.contracts'].search([('id', '=', self.contracts_id.id)]).sales_order_id.id         
        self.client_id      = self.env['logistics.contracts'].search([('id', '=', self.contracts_id.id)]).client_id.id    
        
        origin          = self.env['logistics.contracts'].search([('id', '=', self.contracts_id.id)]).origin_id.id    
        destination     = self.env['logistics.contracts'].search([('id', '=', self.contracts_id.id)]).destination_id.id
        origin_obj      = self.env['logistics.routes'].browse(origin)    
        destination_obj = self.env['logistics.routes'].browse(destination)
        if origin and destination:
            self.route = origin_obj.name + ', ' + destination_obj.name
            print('\n\n\n\n', )
        else:
            self.route = ""


    @api.onchange('sales_order_id')
    def _onchange_sales_order(self):
        '''Authomatic assignation for field "client_id" from sales_order's input'''
        self.client_id = self.env['sale.order'].search([('id', '=', self.sales_order_id.id)]).partner_id.id 
         

    @api.onchange('vehicle_id')
    def _onchange_vehicle(self):
        '''Authomatic assignation for fields "operator_id" & "analytic_accnt_id" 
           from driver_id taken from vehicle_id's input'''
        self.operator_id = self.env['fleet.vehicle'].search([('id', '=', self.vehicle_id.id)]).driver_id.id
        self.analytic_accnt_id = self.env['account.analytic.account'].search([('vehicle_id', '=', self.vehicle_id.id)], limit=1).id   


    @api.model
    def create_invoice(self, vals):  
        #Create a new invoice according to data in trip's info:
        name_sl_ord = self.env['sale.order'].search([('id', '=', self.sales_order_id.id)]).name
        invoice = {
            'state': 'draft',
            'origin': name_sl_ord
            }
        record = self.env['account.invoice'].create(invoice)      

        #Return a new form view from Trips in order user can interact with it:
        return {
            #'name':_("Products to Process"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'account.invoice',
            'res_id': record.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': '[]',
            #'context': {'default_id': record.id}
        }                

 


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