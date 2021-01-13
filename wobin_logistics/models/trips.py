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
        """This method intends to create a sequence for a given trip and a new analytic tag"""
        #init vars:
        #name_aux = ''

        #Retrieve the latest tag:
        #tag = self.env['account.analytic.tag'].search([('analytic_tag_type', '=', 'trip')], order="write_date desc", limit=1).name
        #_logger.info("\n\n\ntag: %s\n\n\n", tag)

        #if tag:
            #Split to get numeric part of string e.g. take 005 from "V: 005"
            #numeric_part = int(tag[3:])
            #_logger.info("\n\n\nnumeric_part: %s\n\n\n", numeric_part)
            #Increase number of trip tag 005 + 1 = 006:
            #tag_to_create = numeric_part + 1        
            #After retrieve the lastest tag, it's important to create a new one (e.g. V: 006)
            #name_aux = 'V: ' + str(tag_to_create)   
            #_logger.info("\n\n\nname_aux: %s\n\n\n", name_aux)     
            #values = {
            #        'name': name_aux,
            #        'analytic_tag_type': 'trip'
            #    }
            #self.env['account.analytic.tag'].create(values)

        #Change of sequence (if it isn't stored is shown "New" else e.g VJ000005)  
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code(
                'self.trip') or 'New'

            vals['name'] = sequence
            vals['trip_number_tag'] = sequence

            values = {
                    'name': sequence,
                    'analytic_tag_type': 'trip'
                }
            self.env['account.analytic.tag'].create(values)  
                      
        result = super(LogisticsTrips, self).create(vals)
        return result


    # General Data / - / - / - / - / - / - / - / - / - /
    name              = fields.Char(string="Trip", readonly=True, required=True, copy=False, default='New')
    trip_number_tag   = fields.Char(string='Trip Number (Analytic Tag)', track_visibility='always')
    contracts_id      = fields.Many2one('logistics.contracts', string='Contracts', track_visibility='always', ondelete='set null')
    client_id         = fields.Many2one('res.partner', string='Client', track_visibility='always')
    vehicle_id        = fields.Many2one('fleet.vehicle', string='Vehicle')    
    analytic_accnt_id = fields.Many2one('account.analytic.account', string='Analytic Account', track_visibility='always')
    operator_id       = fields.Many2one('hr.employee',string='Operator', track_visibility='always')
    route             = fields.Char(string='Route', track_visibility='always')
    advance_ids       = fields.Many2many('purchase.order',string='Related Expenses', track_visibility='always', compute='_set_purchase_orders')
   
    # Upload data / - / - / - / - / - / - / - / - / - / - /
    start_date        = fields.Date(string='Start Date', track_visibility='always')
    upload_date       = fields.Date(string='Upload Date', track_visibility='always')
    estimated_qty     = fields.Float(string='Estimated Quantity', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always')
    real_upload_qty   = fields.Float(string='Real Upload Quantity', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always')
    attachment_upload = fields.Binary(string='Upload Attachments', track_visibility='always')
   
    # Download Data / - / - / - / - / - / - / - / - / - / - /
    download_date     = fields.Date(string='Download Date', track_visibility='always')
    real_download_qty = fields.Float(string='Real Download Quantity', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always')
    attachment_downld = fields.Binary(string='Download Attachments', track_visibility='always')
    qty_to_bill       = fields.Float(string='Quantiy to bill', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always', compute='_set_qty_to_bill') 
    conformity        = fields.Binary(string='Conformity and Settlement', track_visibility='always')
    checked           = fields.Boolean(string=" ")
    sales_order_id    = fields.Many2one('sale.order', string='Sales Order Generated', track_visibility='always', compute='_set_sale_order', ondelete='set null')    
    state             = fields.Selection(selection=[('assigned', 'Assigned'),
                                                    ('route', 'En route'),
                                                    ('discharged', 'Discharged')], 
                                                    string='State', required=True, readonly=True, copy=False, tracking=True, default='assigned', compute="set_status", track_visibility='always')

    # Analysis Fields / - / - / - / - / - / - / - / - / - / - /
    trip_taxes        = fields.Many2many('account.tax', string='Taxes', compute="_set_trip_taxes", track_visibility='always')
    income_provisions = fields.Float(string='Income Provisions', digits=dp.get_precision('Product Unit of Measure'), compute='_set_income_prov', track_visibility='always')                                                    
    billed_income     = fields.Float(string='Billed Income', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always', compute='_set_billed_income')                                      
    expenses          = fields.Float(string='Expenses', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always', compute='_set_expenses')                                      
    profitability     = fields.Float(string='Profitability', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always', compute='_set_profitability') 
    advance_payment   = fields.Float(string='Advance Payment', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always', compute='_set_advance_payment') 
    settlement        = fields.Float(string='Settlement', digits=dp.get_precision('Product Unit of Measure'), track_visibility='always', compute='_set_settlement')     
    invoice_status    =  fields.Selection([('draft','Draft'),
                                           ('open', 'Open'),
                                           ('in_payment', 'In Payment'),
                                           ('paid', 'Paid'),
                                           ('cancel', 'Cancelled'),
                                          ], string='Status', index=True, readonly=True, default='draft', copy=False, compute='_set_inv_status', track_visibility='always')                                         
    
   
        
    @api.one
    def set_status(self):
        '''Set up state in base a which fields are filled up'''
        if self.contracts_id and self.client_id and self.vehicle_id and self.analytic_accnt_id and self.operator_id and self.route and self.start_date and self.upload_date and self.estimated_qty and self.real_upload_qty and self.download_date and self.real_download_qty and self.checked:
            self.state = 'discharged'          
        elif self.contracts_id and self.client_id and self.vehicle_id and self.analytic_accnt_id and self.operator_id and self.route and self.start_date and self.upload_date and self.estimated_qty and self.real_upload_qty:
            self.state = 'route'
        else:
            self.state = 'assigned'
    


    @api.one
    @api.depends('name')    
    def _set_sale_order(self):
        self.sales_order_id = self.env['sale.order'].search([('trips_id', '=', self.id)]).id
    """
    def create_sale_order(self):
        if self.sales_order_id:
            #Raise an error because it's not possible to have more than one sale order per trip:
            msg = _('You can just create one Sale Order per Trip')
            raise UserError(msg)
        else:
            #Retrieve id of "SERVICIOS DE FLETE" and create a New Sale Order, 
            #including some data in its order_lines:
            flete_id = self.env['product.template'].search([('name', 'ilike', 'SERVICIO DE FLETE')], limit=1)
            
            vals = {
                   'name': self.env['ir.sequence'].next_by_code('sale.order') or 'New', 
                   'partner_id': self.client_id.id,
                   'order_line': [(0, 0, {'product_id': flete_id.id, 'description': 'SERVICIO DE FLETE', 'price_unit': self.qty_to_bill, 'name': 'SERVICIO DE FLETE'}),
                                  (0, 0, {'display_type': 'line_note', 'description': self.name, 'name': self.name})] 
            }
            record = self.env['sale.order'].create(vals) 

            #Assignment of all new created sale order into field "sales_order_id" in Trips:
            self.sales_order_id = record.id 
            
            #Assignment in Sale Order to indicate which is its corresponding trip:
            sale_order_obj = self.env['sale.order'].browse(record.id)
            sale_order_obj.update({'trips_id': self.id, 'flag_trip': True})
    """



    @api.onchange('contracts_id')
    def _onchange_contract(self):
        '''Authomatic assignation for fields in Trips from contracts_id's input'''
        self.client_id      = self.env['logistics.contracts'].search([('id', '=', self.contracts_id.id)]).client_id.id    
        
        origin          = self.env['logistics.contracts'].search([('id', '=', self.contracts_id.id)]).origin_id.id    
        destination     = self.env['logistics.contracts'].search([('id', '=', self.contracts_id.id)]).destination_id.id
        origin_obj      = self.env['logistics.routes'].browse(origin)    
        destination_obj = self.env['logistics.routes'].browse(destination)
        if origin and destination:
            self.route = origin_obj.name + ', ' + destination_obj.name
        else:
            self.route = ""
         
        
    """    
    @api.onchange('vehicle_id')
    def _onchange_vehicle(self):
        '''Authomatic assignation for fields "operator_id" & "analytic_accnt_id" 
           from driver_id taken from vehicle_id's input'''
        #self.operator_id = self.env['fleet.vehicle'].search([('id', '=', self.vehicle_id.id)]).driver_id.id
        self.analytic_accnt_id = self.env['account.analytic.account'].search([('vehicle_id', '=', self.vehicle_id.id)], limit=1).id   
    """


    @api.one
    @api.depends('name')
    def _set_purchase_orders(self):            
        #ID of trip tag:
        trip_tag_id = self.env['account.analytic.tag'].search([('name', '=', self.trip_number_tag)]).id
        
        #Process valid in case of having an ID of Trip Tag:
        if trip_tag_id:
            #IDs corresponding to Purchase Lines with the present Trip Tag ID: 
            po_lnes_ids = self.env['purchase.order.line'].search([('analytic_tag_ids','=', trip_tag_id)]).ids

            pur_ord_set = set()  #Set in order to avoid duplicate values

            for line in po_lnes_ids:
                #Iterate Purchase Lines and get their Header Purchase Order ID
                #and add them into a set (averting duplicate ones):
                pur_ord_lin_obj = self.env['purchase.order.line'].browse(line)
                pur_ord_set.add(pur_ord_lin_obj.order_id.id)

            #Conversion from set to list in order to permit injection of multiple values:
            pur_ords_lst = list(pur_ord_set)
            print('\n\n\n\n list conversion pur_ords_lst: ', pur_ords_lst)
            #Now many2many field Advance_ids has various values:
            self.advance_ids = [(6, 0, pur_ords_lst)]
                 


    @api.one
    def _set_trip_taxes(self):
        self.trip_taxes = self.env['account.invoice.line'].search([('trips_id', '=', self.id)]).invoice_line_tax_ids.ids



    @api.one
    def _set_income_prov(self):
        self.income_provisions = self.env['account.invoice.line'].search([('trips_id', '=', self.id)]).price_subtotal



    @api.one
    def _set_qty_to_bill(self):
        #Get Tariff from Contract data belonging to this Trip:
        tariff = self.env['logistics.contracts'].search([('id', '=', self.contracts_id.id)]).tariff
        self.qty_to_bill = self.real_upload_qty * tariff



    @api.one
    def _set_inv_status(self):
        invoice_id = self.env['account.invoice.line'].search([('trips_id', '=', self.id)]).invoice_id.id
        self.invoice_status = self.env['account.invoice'].search([('id', '=', invoice_id)]).state



    @api.one
    @api.depends('name')
    def _set_billed_income(self):
        self.billed_income = self.env['account.invoice'].search([('origin', '=', self.sales_order_id.id)], limit=1).amount_total



    @api.one
    @api.depends('name')
    def _set_expenses(self):
        billed_amount_po = 0.0

        for pur_ord in self.advance_ids:
            amount = self.env['account.invoice'].search([('origin', '=', pur_ord.id)]).amount_total
            billed_amount_po += amount

        self.expenses = billed_amount_po            




    @api.one
    @api.depends('name')
    def _set_profitability(self):
        self.profitability = self.billed_income - self.expenses



    @api.one
    @api.depends('name')
    def _set_advance_payment(self):
        pass



    @api.one
    @api.depends('name')
    def _set_settlement(self):
        self.settlement = (self.income_provisions + self.expenses) - self.advance_payment

    """
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
    """            

 


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




class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Aggregation of new relational fields
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::  
    contracts_ids     = fields.One2many('logistics.contracts', 'id', string='Contracts Information')
    trips_related_ids = fields.Many2many('logistics.trips', compute='_set_trips', string='Related Trips')

    @api.one
    @api.depends('number')
    def _set_trips(self):
        #Get trips assigned from invoice lines:        
        trip_list = [ inv.trips_id.id for inv in self.invoice_line_ids ]
        if trip_list:
            trip_retrieved     = trip_list[0]
            print('\n\n\n trip_retrieved: ', trip_retrieved)
            contract_retrieved = self.env['logistics.trips'].search([('id', '=', trip_retrieved)]).contracts_id.id
            print('\n\n\n contract_retrieved: ', contract_retrieved)
            if contract_retrieved:            
                self.contracts_ids = [(4, 0, contract_retrieved)]

        self.trips_related_ids = [(6, 0, trip_list)] 




class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Aggregation of a new many2one field of Trips in Customer Invoices
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::  
    trips_id = fields.Many2one('logistics.trips', string='Trip')        




class SaleOrder(models.Model):
    _inherit = "sale.order"

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    # Aggregation of a new many2one field of Trips in Customer Invoices
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::  
    trips_id = fields.Many2one('logistics.trips', string='Trip')     
    flag_trip = fields.Boolean(string='Flag to indicate this sale order has trip', compute='_set_flag_trip', store=True)
    

    @api.one
    @api.depends('trips_id')
    def _set_flag_trip(self):
        if self.trips_id:
            self.flag_trip = True            
        else:
            self.flag_trip = False