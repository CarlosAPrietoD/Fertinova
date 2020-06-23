# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


#//////////////////////////////////////////////////////////////////////////////////////////////#
# TICKET 107 DEVELOPED BY SEBASTIAN MENDEZ -- START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class StockQuant(models.Model):
    _inherit = 'stock.quant'

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