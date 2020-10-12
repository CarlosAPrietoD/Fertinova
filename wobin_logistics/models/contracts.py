# -*- coding: utf-8 -*-

from odoo import models, fields, api

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

    name      = fields.Char(string="Contract", readonly=True, required=True, copy=False, default='New')
    remitter  = fields.Char(string='Remitter')
    recipient = fields.Char(string='Recipient')
    carrier   = fields.Char(string='Carrier')
    shipping  = fields.Char(string='Shipping')