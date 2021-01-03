# -*- coding: utf-8 -*-
import operator    
from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)   

class LogisticsRoutes(models.Model):
    _name = 'logistics.routes'
    _description = 'Logistics Routes'

    name = fields.Char(string="City to add for origins & destinations")



class LogisticsContracts(models.Model):
    _name = 'logistics.contracts'
    _description = 'Logistics Contracts'
    _inherit     = ['mail.thread', 'mail.activity.mixin']   

    @api.model
    def create(self, vals):                        
        #Change of sequence (if it isn't stored is shown "New" else e.g CONTR000005)  
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'self.contract') or 'New'               
        result = super(LogisticsContracts, self).create(vals)
        return result    

    name            = fields.Char(string="Contract", readonly=True, required=True, copy=False, default='New')
    client_id       = fields.Many2one('res.partner', string='Client', required=True)
    product_id      = fields.Char(string="Product", required=True)
    covenant_qty    = fields.Float(string='Covenanted Quantity', required=True, digits=dp.get_precision('Product Unit of Measure'))
    tariff          = fields.Float(string='Tariff', required=True, digits=dp.get_precision('Product Unit of Measure'))
    expected_income = fields.Float(string='Expected Income', readonly=True, digits=dp.get_precision('Product Unit of Measure'), compute='_set_expected_income')
    origin_id       = fields.Many2one('logistics.routes', string='Origin', required=True)
    destination_id  = fields.Many2one('logistics.routes', string='Destination', required=True)
    remitter        = fields.Char(string='Remitter', required=True)
    recipient       = fields.Char(string='Recipient', required=True)
    shipping        = fields.Char(string='Shipping', required=True)
    observations    = fields.Html('Observations', required=True)
    # -- These fields were created for analysis not to be shown in main view of contracts -- #
    trips              = fields.Char(string='Trips', compute='_set_trips')
    trip_delivered_qty = fields.Float(string='Trip Delivered Qty', digits=dp.get_precision('Product Unit of Measure'), compute='_set_trp_del_qty')
    difference_qty     = fields.Float(string='Difference Qty', digits=dp.get_precision('Product Unit of Measure'), compute='_set_dif_qty')
    trip_status        =  fields.Selection([('to_do', 'To Do'),
                                            ('doing', 'Doing'),
                                            ('done', 'Done'),
                                           ], string='Trip Status', index=True, readonly=True, default='to_do', copy=False, compute='_set_trip_status')    

    
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
            'res_model': 'logistics.trips',
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
                         FROM logistics_trips 
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
                         FROM logistics_trips 
                        WHERE contracts_id = %s"""
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


    @api.one
    def _set_trip_status(self):
        pass


"""
class SaleOrder(models.Model):
    _inherit = "sale.order"


    @api.multi
    def _action_confirm(self):
        #Normal Logic of method "action_confirm" of Sales Order:
        sale_order = super(SaleOrder, self)._action_confirm()

        #Before creation of a new contract it's important to validate
        #that the sales order contains in its lines "Servicio Flete":
        flag = False
        for line in self.order_line:
            if operator.contains(line.name, "FLETE"): 
                flag = True

        #Create a new contract in Wobin Logistics triggered by 
        #a confirmation in Sales Order:  
        if flag == True:
            sequence = self.env['ir.sequence'].next_by_code('self.contract')
            if not sequence:
                numerical_part = 1
                #After number has increased, fill with zeros to 6 digits
                sequence_aux = str(numerical_part).zfill(6)
            else: 
                #Retrieved  --> CONTR000011
                numerical_part = int(sequence[5:])
                numerical_part += 1
                #After number has increased, fill with zeros to 6 digits
                sequence_aux = str(numerical_part).zfill(6)

            contract = {'name': 'CONTR' + sequence_aux,
                        'client_id': self.partner_id.id,
                        'sales_order_id': self.id}
            self.env['logistics.contracts'].create(contract)        
        return sale_order 
""" 