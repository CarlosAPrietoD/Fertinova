# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class LogisticsContracts(models.Model):
    _name = 'logistics.contracts'
    _description = 'Logistics Contracts'
    _inherit     = ['mail.thread', 'mail.activity.mixin']   

    @api.model
    def create(self, vals):                        
        #Change of sequence (if it isn't stored is shown "New" else e.g CONTR000005)  
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'self.contract') or 'New'               
        result = super(LogisticsContracts, self).create(vals)
        return result    

    name           = fields.Char(string="Contract", readonly=True, required=True, copy=False, default='New')
    client_id      = fields.Many2one('res.partner', string='Client')
    sales_order_id = fields.Many2one('sale.order', string='Sales Order')
    product_id     = fields.Many2one('product.template', string="Product")
    covenant_qty   = fields.Float(string='Covenanted Quantity', digits=dp.get_precision('Product Unit of Measure'))
    tariff         = fields.Float(string='Tariff', digits=dp.get_precision('Product Unit of Measure'))
    origin_destiny = fields.Many2many('account.analytic.tag', string='Origin & Destiny', domain=[('analytic_tag_type', '=', 'route')])
    remitter       = fields.Char(string='Remitter')
    recipient      = fields.Char(string='Recipient')
    shipping       = fields.Char(string='Shipping')
    observations   = fields.Html('Observations')


    def create_trip(self):
        """This method intends to display a Form View of Trips"""
        #action_id = self.env['ir.model.data'].xmlid_to_res_id('wobin_logistics.view_logistics_trips_form', 
        return {
            #'name':_("Products to Process"),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'logistics.trips',
            #'res_id': partial_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'domain': '[]',
            'context': {'default_contracts_id': self.id}
        }



class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _action_confirm(self):
        #Normal Logic of method "action_confirm" of Sales Order:
        sale_order = super(SaleOrder, self)._action_confirm()
        #Create a new contract in Wobin Logistics triggered by 
        #a confirmation in Sales Order:  
        sequence = self.env['ir.sequence'].next_by_code('self.contract')
        if not sequence:
            numerical_part = 1
            #After number has increased, fill with zeros to 6 digits
            sequence_aux = str(numerical_part).zfill(6)
        else: 
            #Retrieved  --> CONTR000011
            numerical_part = int(sequence[5:])
            numerical_part += 1
            #After number has increased, fill with zeros to 6 digits
            sequence_aux = str(numerical_part).zfill(6)

        contract = {'name': 'CONTR' + sequence_aux,
                    'client_id': self.partner_id.id,
                    'sales_order_id': self.id}
        self.env['logistics.contracts'].create(contract)        
        return sale_order        