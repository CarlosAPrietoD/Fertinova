# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    #///////////////////////////////
    #  Fields to add
    #///////////////////////////////
    origin_transfer_id = fields.Many2one('stock.picking', string='Transferencia Origen', track_visibility='always')
    
    is_waste   = fields.Boolean(string='¿Es merma?')
    is_surplus = fields.Boolean(string='¿Es excedente?')

    waste_id   = fields.Many2one('stock.picking', string='Folio Merma', compute='_set_waste_id')
    surplus_id = fields.Many2one('stock.picking', string='Folio Excedente', compute='_set_surplus_id')

    delivery_amount = fields.Float(string='     Entrega', digits=(20, 2), compute='_set_delivery_amount')
    waste_amount    = fields.Float(string='     Merma', digits=(20, 2), compute='_set_waste_amount')
    surplus_amount  = fields.Float(string='     Excedente', digits=(20, 2), compute='_set_surplus_amount')
    eff_qty_amount  = fields.Float(string='Cantidad Efectivamente Recibida', digits=(20, 2), compute='_set_eff_qty_amount')



    @api.one 
    def _set_waste_id(self):
        self.waste_id = self.env['stock.picking'].search([('is_waste', '=', True),
                                                          ('origin_transfer_id', '=', self.id)]).id         



    @api.one 
    def _set_surplus_id(self):
        self.surplus_id = self.env['stock.picking'].search([('is_surplus', '=', True),
                                                            ('origin_transfer_id', '=', self.id)]).id 



    @api.one
    @api.depends('name')
    def _set_delivery_amount(self):
        self.delivery_amount = sum(line.quantity_done for line in self.move_ids_without_package)                                                                    



    @api.one
    @api.depends('waste_id')
    def _set_waste_amount(self):
        self.waste_amount = sum(line.quantity_done for line in self.waste_id.move_ids_without_package)



    @api.one
    @api.depends('surplus_id')
    def _set_surplus_amount(self):
        self.surplus_amount = sum(line.quantity_done for line in self.surplus_id.move_ids_without_package)



    @api.one
    @api.depends('waste_id', 'surplus_id')
    def _set_eff_qty_amount(self):          
        self.eff_qty_amount = self.delivery_amount - self.waste_amount + self.surplus_amount

    


    #|-|-|-|-|-|-|-|-|-|-|-|-|-|
    #Open a new window for waste
    @api.multi
    def open_stock_picking_waste(self):
        #Get current company_id from user where this process will apply just to GRANERO:
        company_aux_id = self.env['res.company'].browse(self.env['res.company']._company_default_get('your.module')).id
        company_id = company_aux_id.id

        #GRANERO is ID '2' in Companies:
        if company_id == 2:

            line_ids_list    = list()
            item             = tuple()
            dictionary_vals  = dict()

            #Iterate over items in lines of stock picking
            #in order to construct data pre-filled for new
            #window of waste transfer:
            for line in self.move_ids_without_package:  
                #Construct tuple item for each line (0, 0, dictionary_vals)
                dictionary_vals = {
                    'name': line.name,
                    'state': 'draft',
                    'product_id': line.product_id.id,
                    'date_expected': fields.datetime.now(),
                    'product_uom': line.product_uom.id,
                    'is_locked': False,
                    'show_operations': False
                }
                item = (0, 0, dictionary_vals)
                #Append into list which it will be used later in context:
                line_ids_list.append(item)    

            #Fill with this fixed data 
            sequence         = self.env['ir.sequence'].next_by_code('self.wastestock') or 'New'
            name_seq         = sequence 
            picking_type     = self.env['stock.picking.type'].search([('id', '=', 173)]).id 
            location_id      = self.env['stock.location'].search([('id', '=', 9)]).id                                   
            location_dest_id = self.env['stock.location'].search([('id', '=', 1257)]).id 

            #Context to pre-fill with data new window:
            ctxt = {
                'default_name': name_seq,
                'default_picking_type_id': picking_type,
                'default_location_id': location_id,
                'default_location_dest_id': location_dest_id,
                'default_origin_transfer_id': self.id,
                'default_is_waste': True,
                'default_waste_id': self.id,
                'default_move_ids_without_package': line_ids_list
            }

            #Return new window of waste transfer:
            return {
                #'name':_("Mermas"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'stock.picking',
                #'res_id': partial_id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'domain': '[]',
                'context': ctxt            
            }  


        

    #|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
    #Open a new window for surplus
    @api.multi
    def open_stock_picking_surplus(self):
        #Get current company_id from user where this process will apply just to GRANERO:
        company_aux_id = self.env['res.company'].browse(self.env['res.company']._company_default_get('your.module')).id
        company_id = company_aux_id.id

        #GRANERO is ID '2' in Companies:
        if company_id == 2:        
            line_ids_list    = list()
            item             = tuple()
            dictionary_vals  = dict()

            #Iterate over items in lines of stock picking
            #in order to construct data pre-filled for new
            #window of surplus transfer:
            for line in self.move_ids_without_package:  
                #Construct tuple item for each line (0, 0, dictionary_vals)
                dictionary_vals = {
                    'name': line.name,
                    'state': 'draft',
                    'product_id': line.product_id.id,
                    'date_expected': fields.datetime.now(),
                    'product_uom': line.product_uom.id,
                    'is_locked': False,
                    'show_operations': False
                }
                item = (0, 0, dictionary_vals)
                #Append into list which it will be used later in context:
                line_ids_list.append(item)       

            #Fill with this fixed data 
            sequence         = self.env['ir.sequence'].next_by_code('self.surplustock') or 'New'
            name_seq         = sequence             
            picking_type     = self.env['stock.picking.type'].search([('id', '=', 170)]).id 
            location_id      = self.env['stock.location'].search([('name', '=', self.location_id.name)]).id                                                                    

            #Context to pre-fill with data new window:
            ctxt = {
                'default_name': name_seq,
                'default_picking_type_id': picking_type,
                'default_location_id': self.location_id.id,
                'default_origin_transfer_id': self.id,
                'default_is_surplus': True,
                'default_surplus_id': self.id,
                'default_move_ids_without_package': line_ids_list
            }

            #Return new window of surplus transfer:
            return {
                #'name':_("Excedentes"),
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'stock.picking',
                #'res_id': partial_id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'domain': '[]',
                'context': ctxt            
            }
