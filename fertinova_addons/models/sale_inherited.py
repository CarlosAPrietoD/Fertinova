# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 028    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    #########################################################
    # MODEL FIELDS
    #########################################################
    qty_to_deliver = fields.Float(string='Quantity to deliver', 
                                  digits=dp.get_precision('Product Unit of Measure'), 
                                  compute='_get_qty_to_deliver',
                                  store=True,
                                  translate=True)

    #########################################################
    # MODEL METHODS
    #########################################################
    @api.depends('product_uom_qty', 'qty_delivered')
    def _get_qty_to_deliver(self):
        '''This method computes the difference between product on demand and quantity delivered'''
        for rec in self:
            if not rec.product_uom_qty and rec.qty_delivered:
                rec.qty_to_deliver= 0.0
            else:
                rec.qty_to_deliver = rec.product_uom_qty - rec.qty_delivered
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 028    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#

class ReportCustom(models.AbstractModel):
    _name = 'report.fertinova_addons.report_custom_pdf'

    @api.model
    def _get_report_values(self, docids, data=None): 
        docs = self.env['sale.order'].browse(docids)
        print("============", docs)
        algo=[1,2,3,4,5,6]
        algo.append(7)
        return {
            'doc_ids': docids,
            'doc_model': 'sale.order',
            'docs': docs,
            'some': algo,
            #'lines': self.some_func(docs),
            #'data': data,
        }     

class ReportContact(models.AbstractModel):
    _name = 'report.fertinova_addons.report_contact'

    @api.model
    def _get_report_values(self, docids, data=None): 
        partners = self.env['res.partner'].browse(docids)

        docs=[]

        for partner in partners:
            moves=self.env['account.move.line'].search([('partner_id', '=', partner.id)])
            doc={'name':partner.name,
                'moves': moves
            }
            docs.append(doc)
            
        
        return {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'docs': docs
        }           