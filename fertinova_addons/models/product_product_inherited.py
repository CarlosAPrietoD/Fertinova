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
      #Assign date input by user:
      date_ingress = self.date

      #INHERITANCE of original method "open_table()": 
      action = super(StockQuantityHistory, self).open_table()
     
      #Obtain all products from model "product.product":
      all_products = self.env['product.product'].search([('type', '=', 'product')]) 

      for product in all_products.ids:
        #Retrieve INputs summatory from model "stock.move.line" 
        # matching with id->product_id and a given date:         
        sql_query = """SELECT sum(inputs) FROM stock_move_line WHERE product_id = %(prod)s AND date <= %(date)s;"""
        self.env.cr.execute(sql_query, {'prod': product, 'date': date_ingress})
        inputs_aux = self.env.cr.fetchone()  

        #Retrieve OUTputs summatory from model "stock.move.line" 
        # matching with id->product_id and a given date:         
        sql_query = """SELECT sum(outputs) FROM stock_move_line WHERE product_id = %(prod)s AND date <= %(date)s;"""
        self.env.cr.execute(sql_query, {'prod': product, 'date': date_ingress})
        outputs_aux = self.env.cr.fetchone()                    

        #Modify recordset according to iterated product to set inputs and outputs:
        recordset_product = self.env['product.product'].browse(product) 
        recordset_product.inputs  = inputs_aux[0]         
        recordset_product.outputs = outputs_aux[0]

      #Return modified view in method "open_table":
      return action 
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   PRACTICE    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#        