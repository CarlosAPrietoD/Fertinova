# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools.translate import _  


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    #########################################################
    # MODEL FIELDS
    #########################################################
    user_id = fields.Many2one('res.users', 
                              string='Purchase Representative', 
                              index=True, 
                              track_visibility='onchange', 
                              required=True,
                              default=lambda self: None)



#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 028    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    #########################################################
    # MODEL FIELDS
    #########################################################
    qty_to_receive = fields.Float(string='Quantity to receive', 
                                  digits=dp.get_precision('Product Unit of Measure'), 
                                  compute='_get_qty_to_receive',
                                  store=True,
                                  translate=True)

    ##########################################################
    # MODEL METHODS
    ##########################################################
    @api.depends('product_qty', 'qty_received')
    def _get_qty_to_receive(self):
        '''This method computes the difference between product quantity and quantity received'''
        for rec in self:
            if not rec.product_qty and rec.qty_received:
                rec.qty_to_receive = 0.0
            else:
                rec.qty_to_receive = rec.product_qty - rec.qty_received
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 028    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#  

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 035    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
    @api.onchange('price_unit')
    def validation_on_price_unit(self):
        '''This method intends to validate that a product must not be purchased more expensive 
           which is sold by company'''
        msg = ""
        #Initial validation in order to ascertain that checkbox in "product_template" model is ckecked up:        
        if self.product_id.product_tmpl_id.valid_price_unit == True: 
            #Use of "_convert()" method; 
            #parameters ===> ammount, currency to apply conversion, company, date round=True
            purchase_price = self.currency_id._convert(self.price_unit, self.env.user.currency_id, self.env.user.company_id, self.order_id.date_order, round=True)         
            sale_price = self.product_id.product_tmpl_id.list_price
        
            if purchase_price > sale_price:
                msg = _('\nThe purchase price of the product %s $%s is superior than sales price $%s\n') % (self.name, "{0:.4f}".format(purchase_price), sale_price)
                raise UserError(msg)   
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 035    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#
