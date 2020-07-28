# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)
 

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   PRACTICE    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class ProductProduct(models.Model):
    _inherit = "product.product"

    #:::::::::::::::::::::::::::::::::::::::
    # MODEL FIELDS
    #::::::::::::::::::::::::::::::::::::::: 
    inputs = fields.Float(string='Inputs', digits=dp.get_precision('Product Unit of Measure')) 
    outputs = fields.Float(string='Outputs', digits=dp.get_precision('Product Unit of Measure'))     


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    def open_table(self):      
      date_ingress = self.date
      _logger.info('\n\n\n date: %s\n\n\n', date_ingress)  
      _logger.info('\n\n\n contexto: %s\n\n\n', self.env.context) 

      #Verify if radiobutton or option "compute_at_date" has been selected:
      if self.compute_at_date:

        #Inheritance of original method "open_table()" 
        action = super(StockQuantityHistory, self).open_table()
      
        #Obtain all products from model "product.product"
        products_all = self.env['product.product'].search([('type', '=', 'product')])
        _logger.info('\n\n\n stk_mv_lns: %s\n\n\n', products_all)  

        for product in products_all.ids:
          #Retrieval of inputs from model 'stock.move.line' matching with id->product_id:         
          sql_query = """SELECT sum(inputs) FROM stock_move_line WHERE product_id = (product,) AND date <= (self.date,);"""
          self.env.cr.execute(sql_query)
          inputs_aux = self.env.cr.fetchone()  
          _logger.info('\n\n\n inputs_aux: %s\n\n\n', inputs_aux)          

          #Modify the recordset for a given product:
          recordset_product = self.env['product.product'].browse(product) 
          recordset_product.inputs = inputs_aux[0]         

      return action   