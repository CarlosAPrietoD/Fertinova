# -*- coding: utf-8 -*-
from collections import defaultdict
from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    origin_transfer_id = fields.Many2one('stock.picking', string='Transferencia Origen', track_visibility='always')

    @api.multi
    def open_stock_picking_waste(self):
        line_ids_list    = list()
        item             = tuple()
        dictionary_vals  = dict()

        #Iterate over items in lines of stock picking
        #in order to construct data pre-filled for new
        #window of waste transfer:
        for line in self.move_ids_without_package:  
            #Construct tuple item for each line (0, 0, dictionary_vals)
            dictionary_vals = {
                'product_id': line.product_id.id
            }
            item = (0, 0, dictionary_vals)
            #Append into list which it will be used later in context:
            line_ids_list.append(item)                         


        #Context to pre-fill with data new window:
        ctxt = {
            'default_picking_type_id': self.picking_type_id.id,
            'default_location_id': self.location_id.id,
            'default_location_dest_id': self.location_dest_id.id,
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
        line_ids_list    = list()
        item             = tuple()
        dictionary_vals  = dict()

        #Iterate over items in lines of stock picking
        #in order to construct data pre-filled for new
        #window of surplus transfer:
        for line in self.move_ids_without_package:  
            #Construct tuple item for each line (0, 0, dictionary_vals)
            dictionary_vals = {
                'product_id': line.product_id.id
            }
            item = (0, 0, dictionary_vals)
            #Append into list which it will be used later in context:
            line_ids_list.append(item)                         


        #Context to pre-fill with data new window:
        ctxt = {
            'default_picking_type_id': self.picking_type_id.id,
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