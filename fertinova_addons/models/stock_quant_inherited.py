# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

import logging
_logger = logging.getLogger(__name__)      

#//////////////////////////////////////////////////////////////////////////////////////////////#
# TICKET 107 DEVELOPED BY SEBASTIAN MENDEZ -- START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class StockQuant(models.Model):
    _inherit = 'stock.quant'

    ############################################################
    #   MODEL FIELDS:
    ############################################################
    inputs = fields.Float(string='Inputs',                           
                          digits=dp.get_precision('Product Unit of Measure'),
                          compute='_get_inputs') 

    outputs = fields.Float(string='Outputs', 
                           digits=dp.get_precision('Product Unit of Measure'),
                           compute='_get_outputs')     

    transfers = fields.Float(string='Transfers',                                                      
                             digits=dp.get_precision('Product Unit of Measure'),
                             compute='_get_transfers')   


    ############################################################
    #   MODEL METHODS:
    ############################################################    
    def _get_inputs(self):
        '''This method computes the value of inputs'''
        self.inputs = 0 #Initialization
        #Construct domain in order to retrieve values from 'stock.move.line':
        domain = [ 
                  '|',
                      ('product_id', '=', self.product_id.id),                   
                      ('location_id', '=', self.location_id.id),
                 ]
        #IDs obtained in which is necessary to make calculations:                 
        stk_mv_lns = self.env['stock.move.line'].search(domain).ids

        for line in stk_mv_lns:
            #Obtain recordeset of given ID:            
            stk_mv_ln_obj = self.env['stock.move.line'].browse(line)

            #If value is equal or lesser than 0 "inputs" must be 0.0:    
            if stk_mv_ln_obj.mapped('x_studio_valor')[0] > 0:
                self.inputs += stk_mv_ln_obj.mapped('qty_done')[0]   



    def _get_outputs(self):
        '''This method computes the value of outputs'''
        self.inputs = 0 #Initialization
        #Construct domain in order to retrieve values from 'stock.move.line':
        domain = [ 
                  '|',
                      ('product_id', '=', self.product_id.id),                   
                      ('location_id', '=', self.location_id.id),
                 ]
        #IDs obtained in which is necessary to make calculations:                 
        stk_mv_lns = self.env['stock.move.line'].search(domain).ids  
             
        for line in stk_mv_lns:
            #Obtain recordeset of given ID:            
            stk_mv_ln_obj = self.env['stock.move.line'].browse(line)        

            if not stk_mv_ln_obj.mapped('qty_done')[0] and not stk_mv_ln_obj.mapped('x_studio_valor')[0]:
                #If value is equal or superior than 0 "inputs" must be 0.0:    
                if stk_mv_ln_obj.mapped('x_studio_valor')[0] >= 0:
                    self.outputs += 0.0  
                else:
                    self.outputs += stk_mv_ln_obj.mapped('qty_done')[0]  



    def _get_transfers(self):
        '''This method computes the value of transfers'''
        self.inputs = 0 #Initialization
        #Construct domain in order to retrieve values from 'stock.move.line':
        domain = [ 
                  '|',
                      ('product_id', '=', self.product_id.id),                   
                      ('location_id', '=', self.location_id.id),
                 ]
        #IDs obtained in which is necessary to make calculations:                 
        stk_mv_lns = self.env['stock.move.line'].search(domain).ids        

        for line in stk_mv_lns:
            #Obtain recordeset of given ID:  
            stk_mv_ln_obj = self.env['stock.move.line'].browse(line) 

            #If value is equal to 0 "tranfers" must be qty_done                                     
            #(Although it is important notice the conditional about if location_id 
            # is equal to the current location_id in this model):            
            if stk_mv_ln_obj.mapped('x_studio_valor')[0] >= 0:
                _logger.info('\n\n\n stk_mv_ln_obj.mapped(qty_done)[0]: %s', stk_mv_ln_obj.mapped('qty_done')[0])
                if self.location_id == stk_mv_ln_obj.mapped('location_id')[0]:          
                    self.transfers -= stk_mv_ln_obj.mapped('qty_done')[0]
                    _logger.info('\n\n\n tranfers sumandose: %s', self.transfers)
                else:
                    self.transfers += stk_mv_ln_obj.mapped('qty_done')[0] 
                    _logger.info('\n\n\n ¿si entra aquí? tranfers sumandose: %s', self.transfers)                 
       


    def action_view_stock_moves(self):
        """This method intends to extend the original method "action_view_stock_moves()" in order to pass the location_id selected in "stock.quant" by the context.
        This is made by entering into STOCK > MAIN DATA {Menu} > PRODUCTS {Menuitem} > a given product > Smart Button {action_open_quants}"""
        
        #Call in order to extend method 'action_view_stock_moves' 
        action = super(StockQuant, self).action_view_stock_moves()

        #Pass the location_id by context:
        ctx = eval(action['context'])
        ctx.update({'location_id': self.location_id.id})
        action['context'] = str(ctx)          

        return action         
#//////////////////////////////////////////////////////////////////////////////////////////////#
# TICKET 107 DEVELOPED BY SEBASTIAN MENDEZ -- END
#//////////////////////////////////////////////////////////////////////////////////////////////#