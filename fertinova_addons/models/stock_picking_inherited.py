# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


#//////////////////////////////////////////////////////////////////////////////////////////////#
# TICKET Error in Fertinova, OV0803 has not assigned its field Partner_id  -- START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class StockPicking(models.Model):
    _inherit = 'stock.picking'

    #Add via inheritance a compute method:
    partner_id = fields.Many2one(
        'res.partner', 'Partner',
        states={'done': [('readonly', True)], 'cancel': [('readonly', True)]},
        compute='_set_partner_ov803', store=True)    


    @api.one
    @api.depends('name')
    def _set_partner_ov803(self):
        #Transfers or Stock Pickings to correct with this data 
        # ID: 2842
        # NAME: OV0803
        # COMPANY_DB: Fertinova

        #Apply this assignation to Sale Order OV0803
        #where its stock pickings are empty and its
        #origin field is indicated with that document
        if self.origin:
            if 'OV0803' in self.origin or self.id == 26195 or self.id == 26023:
                if not self.partner_id:
                    #Retrieve partner_id from field Client of Sale Order OV0803
                    #and assign them to empty pickings:
                    partner_gotten = self.env['sale.order'].search([('id', '=', 2842)]).partner_id.id
                    self.partner_id = partner_gotten

#//////////////////////////////////////////////////////////////////////////////////////////////#
# TICKET Error in Fertinova, OV0803 has not assigned its field Partner_id  -- END
#//////////////////////////////////////////////////////////////////////////////////////////////#