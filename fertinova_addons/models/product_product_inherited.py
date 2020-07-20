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
    @api.depends('id')
    def _get_inputs(self):
      """This method computes the value of inputs"""
      for record in self:
        #Retrieval of inputs from model 'stock.move.line' matching with id->product_id:         
        sql_query = """SELECT sum(inputs) FROM stock_move_line WHERE product_id = %s;"""
        self.env.cr.execute(sql_query, (record.id,))
        inputs_aux = self.env.cr.fetchone()
        record.inputs = inputs_aux[0]


    @api.depends('id')
    def _get_outputs(self):
      """This method computes the value of inputs"""
      for record in self:
        #Retrieval of outputs from model 'stock.move.line' matching with id->product_id:         
        sql_query = """SELECT sum(outputs) FROM stock_move_line WHERE product_id = %s;"""
        self.env.cr.execute(sql_query, (record.id,))
        outputs_aux = self.env.cr.fetchone()
        record.outputs = outputs_aux[0]