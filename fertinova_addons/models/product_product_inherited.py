# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   PRACTICE    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class ProductProduct(models.Model):
    _inherit = "product.product"

    #:::::::::::::::::::::::::::::::::::::::
    # MODEL FIELDS
    #::::::::::::::::::::::::::::::::::::::: 
    inputs = fields.Float(string='Inputs', 
                          store=True,
                          digits=dp.get_precision('Product Unit of Measure'),
                          compute='_get_inputs') 

    outputs = fields.Float(string='Outputs', 
                           store=True,
                           digits=dp.get_precision('Product Unit of Measure'),
                           compute='_get_outputs')     

    #::::::::::::::::::::::::::::::::::::
    # MODEL METHODS
    #::::::::::::::::::::::::::::::::::::
    @api.depends('qty_at_date', 'stock_value')
    def _get_inputs(self):
      '''This method computes the value of inputs'''
      for record in self:
        if not record.qty_at_date and not record.stock_value:
          record.inputs = 0.0
        else:
          #If value is equal or lesser than 0 "inputs" must be 0.0:    
          if record.stock_value > 0:
            record.inputs = record.qty_at_date  
          else:
            record.inputs = 0.0


    @api.depends('qty_at_date', 'stock_value')
    def _get_outputs(self):
      '''This method computes the value of outputs'''
      for record in self:
        #If value is equal or superior than 0 "inputs" must be 0.0:    
        if record.stock_value >= 0:
          record.outputs = 0.0  
        else:
          record.outputs = record.qty_at_date