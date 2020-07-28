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
    inputs = fields.Float(string='Inputs', digits=dp.get_precision('Product Unit of Measure')) 
    outputs = fields.Float(string='Outputs', digits=dp.get_precision('Product Unit of Measure'))     


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    def open_table(self):  
      #INHERITANCE of original method "open_table()": 
      action = super(StockQuantityHistory, self).open_table()

      #Assign date input by user:
      date_ingress = self.date

      #Verify if radiobutton or option "compute_at_date" has been selected:
      if self.compute_at_date:     
        #Obtain all products from model "product.product":
        all_products = self.env['product.product'].search([('type', '=', 'product')]) 

        for product in all_products.ids:
          #Retrieve INputs % OUTputs summatory from model "stock.move.line" 
          # matching with id->product_id and a given date:         
          sql_query = """SELECT sum(inputs), sum(outputs) FROM stock_move_line WHERE product_id = %(prod)s AND date <= %(date)s;"""
          self.env.cr.execute(sql_query, {'prod': product, 'date': date_ingress})
          inputs_outputs = self.env.cr.fetchone()  

          #Modify recordset according to iterated product to set inputs and outputs:
          recordset_product = self.env['product.product'].browse(product) 
          recordset_product.inputs  = inputs_outputs[0]         
          recordset_product.outputs = inputs_outputs[1]

      else:          
        #Obtain all products from model "product.product":
        all_products = self.env['product.product'].search([('type', '=', 'product')]) 

        for product in all_products.ids:
          #Retrieve INputs & OUTputs summatory from model "stock.move.line"          
          sql_query = """SELECT sum(inputs), sum(outputs) FROM stock_move_line WHERE product_id = %s;"""
          self.env.cr.execute(sql_query, (product,))
          inputs_outputs = self.env.cr.fetchone()                     

          #Modify recordset according to iterated product to set inputs and outputs:
          recordset_product = self.env['product.product'].browse(product) 
          recordset_product.inputs  = inputs_outputs[0]         
          recordset_product.outputs = inputs_outputs[1]        

      #Return modified view in method "open_table":
      return action 
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   PRACTICE    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#  