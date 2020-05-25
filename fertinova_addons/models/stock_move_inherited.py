# -*- coding: utf-8 -*-
import math
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 108    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class StockMove(models.Model):
    _inherit = "stock.move"

    #########################################################
    # MODEL FIELDS
    #########################################################
    analytic_account_id = fields.Many2one('account.analytic.account', 
                                          string='Analytic Account',
                                          store=True,
                                          translate=True)  

    analytic_tag_id = fields.Many2many('account.analytic.tag', 
                                       string='Analytic Tag',                                       
                                       store=True,
                                       translate=True)                                       


    #########################################################
    # MODEL METHODS
    #########################################################
    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id):
      """This method intends to expand the business logic in order to create into
         journal entry the new value of analytic accounts"""
      #Sample about what is inside the res in preparation method of journal entry:   
      #[
      # 0, 0, {'name': '[FURN_9999] Office Design Software', 'product_id': 7, 'quantity': -1.0, 'product_uom_id': 1, 'ref': 'WH/OUT/00012', 'partner_id': 9, 'credit': 235.0, 'debit': 0, 'account_id': 4}, 
      # 0, 0, {'name': '[FURN_9999] Office Design Software', 'product_id': 7, 'quantity': -1.0, 'product_uom_id': 1, 'ref': 'WH/OUT/00012', 'partner_id': 9, 'debit': 235.0, 'credit': 0, 'account_id': 6}
      #]     
            
      #Retrieve original list:
      res = super(StockMove, self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id)
        
      #Creation of the list to be returned:
      result = []      
      #Iteration of res:
      for v in res:        
        #Obtain "account_id" from the original tuple from its internal dictionaty (0, 0, dict{}):
        account_id = v[2].get('account_id')  

        #Retrieval of "code" from model 'account.account' matching with account_id:                    
        code = self.env['account.account'].search([('id', '=', account_id)]).code         
                           
        #Assign and create the new value of analytic_account:           
        new_vals = v[2] #get the dictionary from original tuple (0, 0, dict{})
        
        #Validate that accounts belonging to Equity, Assets and Liabilities must not be considered: 
        if int(code[0]) not in [1, 2 , 3]:
          new_vals['analytic_account_id'] = self.analytic_account_id.id                    
          new_vals['analytic_tag_ids'] = [(6, 0, self.analytic_tag_id.ids)]

        #Append new values into original dictionary:
        element = (0, 0, new_vals)
        result.append(element) 
                            
      return result
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 108    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#      



#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 102 KARDEX    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    #########################################################
    # MODEL FIELDS
    #########################################################
    operative_qty = fields.Float(string='Operative Quantity', 
                                 store=True,
                                 digits=dp.get_precision('Product Unit of Measure'),
                                 compute='_get_operative_qty')      

    inputs = fields.Float(string='Inputs', 
                          store=True,
                          digits=dp.get_precision('Product Unit of Measure'),
                          compute='_get_inputs') 

    outputs = fields.Float(string='Outputs', 
                           store=True,
                           digits=dp.get_precision('Product Unit of Measure'),
                           compute='_get_outputs')     

    transfers = fields.Float(string='Transfers', 
                             store=True,                             
                             digits=dp.get_precision('Product Unit of Measure'),
                             compute='_get_transfers') 

    #accumulated_qty = fields.Float(string='Accumulated Quantity', 
    #                               digits=dp.get_precision('Product Unit of Measure'),
    #                               compute='_get_accumulated_qty')                               

    price_unit = fields.Float(string='Price Unit', 
                              digits=dp.get_precision('Product Unit of Measure'), 
                              compute='_get_price_unit') 

    #accumulated_ammount = fields.Float(string='Accumulated Ammount', 
    #                                   digits=dp.get_precision('Product Unit of Measure'),
    #                                   compute='_get_accumulated_ammount')   

    #calculated_average_cost = fields.Float(string='Calculated Average Cost', 
    #                                       digits=dp.get_precision('Product Unit of Measure'),
    #                                       compute='_get_calculated_average_cost')   

    #average_cost_difference = fields.Float(string='Average Cost Difference', 
    #                                       digits=dp.get_precision('Product Unit of Measure'),
    #                                       compute='_get_average_cost_difference')                                             


    #########################################################
    # MODEL METHODS
    #########################################################
    @api.depends('qty_done', 'x_studio_valor')
    def _get_operative_qty(self):
        '''This method computes the value of operative quantity'''
        for record in self:
          if not record.qty_done and not record.x_studio_valor:
            record.operative_qty = 0.0
          else:
            #Get the sign from field "value": 
            sign_function = lambda param: math.copysign(1, param)
            sign = sign_function(record.x_studio_valor)
            #Assign the value into new field "operative_qty":
            record.operative_qty = record.qty_done * sign                        
            #However since I obtain always 1, then when occurs the case 1 * 1 must be equal to 0.0:
            if record.operative_qty == 1:
                  record.operative_qty = 0.0
            

    @api.depends('qty_done', 'x_studio_valor')
    def _get_inputs(self):
      '''This method computes the value of inputs'''
      for record in self:
        if not record.qty_done and not record.x_studio_valor:
          record.inputs = 0.0
        else:
          #If value is equal or lesser than 0 "inputs" must be 0.0    
          if record.x_studio_valor > 0:
            record.inputs = record.qty_done  
          else:
            record.inputs = 0.0


    @api.depends('qty_done', 'x_studio_valor')
    def _get_outputs(self):
      '''This method computes the value of outputs'''
      for record in self:
        #If value is equal or superior than 0 "inputs" must be 0.0    
        if record.x_studio_valor >= 0:
          record.outputs = 0.0  
        else:
          record.outputs = record.qty_done
    

    @api.depends('qty_done', 'x_studio_valor')
    def _get_transfers(self):
      '''This method computes the value of transfers'''
      for record in self:
        #If value is equal to 0 "tranfers" must be qty_done  
        if record.x_studio_valor == 0.0000 or record.x_studio_valor == 0 or not record.x_studio_valor or record.x_studio_valor == None:            
          record.transfers = record.qty_done
        else:
          record.transfers = 0.0


    #@api.depends('product_id', 'operative_qty')
    #def _get_accumulated_qty(self):
    #  '''This method computes the value of accumulated_qty'''
    #  product_id = None #product id necessary for comparing when it is different
    #  accumulated_qty_aux = 0.0

    #  for record in self:
    #    product_id_aux = record.product_id.id #Obtain product id 
    #    if product_id != product_id_aux:
          #Validation for first item belonging to a product given:    
    #      record.accumulated_qty = record.operative_qty 
    #      accumulated_qty_aux = record.accumulated_qty
    #      product_id = product_id_aux #make product ids equal
    #    else:  
          #When product ids are equal just add values to accumulated quantity:
    #      accumulated_qty_aux = accumulated_qty_aux + record.operative_qty
    #      record.accumulated_qty = accumulated_qty_aux                       

    
    @api.depends('qty_done', 'x_studio_valor')
    def _get_price_unit(self):
      '''This method computes the value of price_unit'''
      for record in self:
        #Avoiding zero division:  
        if not record.qty_done:
          record.price_unit = 0.0
        else:
          #price unit = value / quantity done                
          record.price_unit = record.x_studio_valor / record.qty_done      
      
    
    #@api.depends('x_studio_valor')
    #def _get_accumulated_ammount(self):
    #  '''This method computes the value of accumulated_ammount'''
    #  product_id = None #product id necessary for comparing when it is different
    #  accumulated_ammount_aux = 0.0
      
    #  for record in self:
    #    product_id_aux = record.product_id.id #Obtain product id 
    #    if product_id != product_id_aux:
          #Validation for first item belonging to a product given: 
    #      record.accumulated_ammount = record.x_studio_valor 
    #      accumulated_ammount_aux = record.accumulated_ammount
    #      product_id = product_id_aux #make product ids equal
    #    else:  
          #When product ids are equal just add values to accumulated ammount:
    #      accumulated_ammount_aux += record.x_studio_valor
    #      record.accumulated_ammount = accumulated_ammount_aux


    #@api.depends('accumulated_qty', 'accumulated_ammount')
    #def _get_calculated_average_cost(self):
    #  '''This method computes the value of calculated_average_cost'''
    #  for record in self:
        #Avoiding zero division:   
    #    if record.accumulated_qty == 0.0000 or record.accumulated_qty == 0 or not record.accumulated_qty or record.accumulated_qty == None:
    #      record.calculated_average_cost = 0.0
    #    else:
          #calculated average cost = accumulated ammount / accumulated quantity     
    #      record.calculated_average_cost = record.accumulated_ammount / record.accumulated_qty 


    #@api.depends('calculated_average_cost')    
    #def _get_average_cost_difference(self):
    #  '''This method computes the value of average_cost_difference'''      
    #  product_id = None #product id necessary for comparing when it is different
    #  auxiliar_ammount = 0.0

    #  for record in self:
    #    product_id_aux = record.product_id.id #Obtain product id 

    #    if product_id != product_id_aux:
          #Validation for first item belonging to a product given:
    #      record.accumulated_qty = auxiliar_ammount
    #      product_id = product_id_aux
    #    else:  
          #When product ids are equal just add values to accumulated ammount:
    #      auxiliar_ammount -= record.average_cost_difference
    #      record.average_cost_difference = auxiliar_ammount                                                   
