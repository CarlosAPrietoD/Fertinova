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
    operator_id       = fields.Many2one('hr.employee',string='Operator', track_visibility='always')
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
    trip_taxes        = fields.Many2many('account.tax', string='Taxes', compute="_set_trip_taxes")
    income_provisions = fields.Float(string='Income Provisions', digits=dp.get_precision('Product Unit of Measure'), compute='_set_income_prov')                                                    
    invoice_status    =  fields.Selection([('draft','Draft'),
                                           ('open', 'Open'),
                                           ('in_payment', 'In Payment'),
                                           ('paid', 'Paid'),
                                           ('cancel', 'Cancelled'),
                                          ], string='Status', index=True, readonly=True, default='draft', copy=False, compute='_set_inv_status')
    
    
    @api.one
    def set_status(self):
        '''Set up state in base a which fields are filled up'''
        if self.contracts_id and self.sales_order_id and self.client_id and self.vehicle_id and self.analytic_accnt_id and self.operator_id and self.route and self.advance_id and self.start_date and self.upload_date and self.estimated_qty and self.real_upload_qty and self.download_date and self.real_download_qty and self.checked:
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
         

    """    
    @api.onchange('vehicle_id')
    def _onchange_vehicle(self):
        '''Authomatic assignation for fields "operator_id" & "analytic_accnt_id" 
           from driver_id taken from vehicle_id's input'''
        #self.operator_id = self.env['fleet.vehicle'].search([('id', '=', self.vehicle_id.id)]).driver_id.id
        self.analytic_accnt_id = self.env['account.analytic.account'].search([('vehicle_id', '=', self.vehicle_id.id)], limit=1).id   
    """


    @api.one
    def _set_trip_taxes(self):
        self.trip_taxes = self.env['account.invoice.line'].search([('trips_id', '=', self.id)]).invoice_line_tax_ids.ids


    @api.one
    def _set_income_prov(self):
        self.income_provisions = self.env['account.invoice.line'].search([('trips_id', '=', self.id)]).price_subtotal

    
    @api.one
    def _set_inv_status(self):
        invoice_id = self.env['account.invoice.line'].search([('trips_id', '=', self.id)]).invoice_id.id
        self.invoice_status = self.env['account.invoice'].search([('id', '=', invoice_id)]).state


    @api.model
    def create_invoice(self, vals):  
        #Create a new invoice according to data in trip's info:
        name_sl_ord = self.env['sale.order'].search([('id', '=', self.sales_order_id.id)]).name
        invoice = {
            'type': 'out_invoice',
            'state': 'draft',
            'origin': name_sl_ord
            }
        self.env['account.invoice'].create(invoice) 
        '''
        return {
            #'name':_("Products to Process"),
            'view_mode': 'form',
            'view_id': account.invoice_form,  #action_invoice_tree1,
            'views': [(account.invoice_form, "form")],
            'view_type': 'form',
            'res_model': 'account.invoice',
            'res_id': record.id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': [('type','=','out_invoice')],
            'context': {'default_type':'out_invoice', 'type':'out_invoice', 'journal_type': 'sale'}
        }        
        '''       

 


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




class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Aggregation of a new many2one field of Trips in Customer Invoices
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::  
    trips_id = fields.Many2one('logistics.trips', string='Trip')    




class SaleOrder(models.Model):
    _inherit = "sale.order"

    trips              = fields.Char(string='Trips', compute='_set_trips')
    covenant_qty       = fields.Float(string='Covenant Qty', digits=dp.get_precision('Product Unit of Measure'), compute='_set_covenant_qty')
    trip_delivered_qty = fields.Float(string='Trip Delivered Qty', digits=dp.get_precision('Product Unit of Measure'), compute='_set_trp_del_qty')
    difference_qty     = fields.Float(string='Difference Qty', digits=dp.get_precision('Product Unit of Measure'), compute='_set_dif_qty')


    @api.one
    @api.depends('name')
    def _set_trips(self):
        '''This method intends to show in a single row multiple 
           trips assigned to a given sale order'''
        trips_lst = []
            
        sql_query = """SELECT name 
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


    @api.one   
    @api.depends('name')
    def _set_covenant_qty(self):
        '''This method intends to sum the value of covenant_qty in trips assigned to order lines'''
        sum_covenant_qty = 0          
        sql_query = """SELECT contracts_id 
                         FROM logistics_trips 
                        WHERE sales_order_id = %s;"""
        self.env.cr.execute(sql_query, (self.id,))
        result = self.env.cr.fetchall()

        print('\n\n\n\n\n result', result)  

        if result:                    
            for contract in result:
                if contract[0]:
                    #Retrieve covenant_qty of contract which belongs to a given trip:
                    sum_covenant_qty += self.env['logistics.contracts'].search([('id', '=', contract)]).covenant_qty
        
        self.covenant_qty = sum_covenant_qty
        print('\n\n\n\n {2} self.covenant_qty',self.covenant_qty) 


    @api.one
    @api.depends('name')
    def _set_trp_del_qty(self):
        '''This method intends to sum all discharges of multiple 
           trips assigned to a given sales order'''
        sql_query = """SELECT sum(real_upload_qty) 
                         FROM logistics_trips 
                        WHERE sales_order_id = %s"""
        self.env.cr.execute(sql_query, (self.id,))
        result = self.env.cr.fetchone()
        _logger.info("\n\n\n\n\n result: %s\n\n\n", result)
        print('\n\n\n ¿si estra?  \n\n')
        if result:                    
            self.trip_delivered_qty = result[0]
            print('\n\n\n\n {3} ,self.trip_delivered_qty', self.trip_delivered_qty)


    @api.one    
    @api.depends('name')
    def _set_dif_qty(self):
        '''This method intends to show the difference between delivered qty 
           and discharged qty assigned to a given sale order'''
        self.difference_qty = self.covenant_qty - self.trip_delivered_qty
        print('\n\n\n\n {4} , self.difference_qty', self.difference_qty)