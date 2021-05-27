# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    origin_transfer_id = fields.Many2one('stock.picking', string='Transferencia Origen', track_visibility='always')



    @api.multi
    def open_stock_picking_waste(self):
        #Get current company_id from user where this process will apply just to GRANERO:
        company_aux_id = self.env['res.company'].browse(self.env['res.company']._company_default_get('your.module')).id
        _logger.info('\n\n\n company_aux_id: %s\n\n\n', company_aux_id)
        company_id = company_aux_id.id
        _logger.info('\n\n\n company_id: %s\n\n\n', company_id)

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
                    'product_id': line.product_id.id,
                    'is_locked': False
                }
                item = (0, 0, dictionary_vals)
                #Append into list which it will be used later in context:
                line_ids_list.append(item)    

            #Fill with this fixed data 
            picking_type     = self.env['stock.picking.type'].search([('id', '=', 173)]).id 
            _logger.info('\n\n\n picking_type: %s\n\n\n', picking_type)
            location_id      = self.env['stock.location'].search([('id', '=', 9)]).id    
            _logger.info('\n\n\n ocation_id: %s\n\n\n', location_id)
            location_dest_id = self.env['stock.location'].search([('id', '=', 1257)]).id 
            _logger.info('\n\n\n location_id_des: %s\n\n\n', location_dest_id)

            #Context to pre-fill with data new window:
            ctxt = {
                'default_name': 'MER/' + self.name,
                'default_picking_type_id': picking_type,
                'default_location_id': location_id,
                'default_location_dest_id': location_dest_id,
                'default_origin_transfer_id': self.id,
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
                    'product_id': line.product_id.id,
                    'is_locked': False
                }
                item = (0, 0, dictionary_vals)
                #Append into list which it will be used later in context:
                line_ids_list.append(item)       

            #Fill with this fixed data 
            picking_type     = self.env['stock.picking.type'].search([('id', '=', 170)]).id 
            _logger.info('\n\n\n picking_type : %s\n\n\n', picking_type)
            location_id      = self.env['stock.location'].search([('name', '=', self.location_id.name)]).id    
            _logger.info('\n\n\n location_id: %s\n\n\n', location_id)

            #Context to pre-fill with data new window:
            ctxt = {
                'default_name': 'EXC/' + self.name,
                'default_picking_type_id': picking_type,
                'default_location_id': self.location_id.id,
                'default_origin_transfer_id': self.id,
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
