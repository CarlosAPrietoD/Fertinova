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

    name         = fields.Char(string="Contract", readonly=True, required=True, copy=False, default='New')
    client_id    = fields.Many2one('res.partner', string='Client')
    product_id   = fields.Many2one('product.template', string="Product")
    covenant_qty = fields.Float(string='Covenanted Quantity', digits=dp.get_precision('Product Unit of Measure'))
    tariff       = fields.Float(string='Tariff', digits=dp.get_precision('Product Unit of Measure'))
    origin       = fields.Char(string='Origin')
    destiny      = fields.Char(string='Destiny')
    remitter     = fields.Char(string='Remitter')
    recipient    = fields.Char(string='Recipient')
    carrier      = fields.Char(string='Carrier')
    shipping     = fields.Char(string='Shipping')
    observations = fields.Html('Observations')

    #@api.multi
    def get_client(self):
        record_collection = self.env['res.partner'].search([('id', '=', self.client_id.id)]).name
        print('////////////////////////// ,   ', record_collection)
        return record_collection  
        
          
    def get_product(self):
        record_collection = self.env['product.template'].search([('id', '=', self.product_id.id)]).name
        print('////////////////////////// ,   ', record_collection)
        return record_collection  
        

'''
class ReportLogisticsContracts(models.AbstractModel):
    _name = 'report.wobin_logistics.report_contract_view'
    _description = 'Abstract Model for contract report'

    @api.model
    def _get_report_values(self, docids, data=None):
        cont = self.env['logistics.contracts'].browse(docids)
        
        #docs = []
        clients_name = self.env['res.partner'].search([('id', '=', cont.client_id.id)]).name
        product_name = self.env['product.template'].search([('id', '=', cont.product_id.id)]).name
        doc = {
               'clients_name': clients_name,
               'product_name': product_name
              }
        #docs.append(doc)


        return {
            'doc_ids': docids,
            'doc_model': 'logistics.contracts',
            'docs': doc
        }    

    '''