# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class WobinComprobations(models.Model):
    _name = 'wobin.comprobations'
    _description = 'Wobin Comprobations'
    _inherit = ['mail.thread', 'mail.activity.mixin']     


    @api.model
    def create(self, vals):  
        """This method intends to create a sequence for a given comprobation"""
        #Change of sequence (if it isn't stored is shown "New" else e.g ANT000005)  
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code(
                'self.comprobation') or 'New'
            vals['name'] = sequence                      
        return super(WobinComprobations, self).create(vals)


    name        = fields.Char(string="Advance", readonly=True, required=True, copy=False, default='New')
    operator_id = fields.Many2one('hr.employee',string='Operator', track_visibility='always')
    date        = fields.Date(string='Date', track_visibility='always')
    amount      = fields.Float(string='Amount', digits=dp.get_precision('Product Unit of Measure'), group_operator=False, track_visibility='always')
    circuit_id  = fields.Many2one('wobin.circuits', string='Circuit', track_visibility='always')
    trip_id     = fields.Many2one('wobin.logistica.trips', string='Trip', track_visibility='always')
    expenses_to_refund = fields.Float(string='Pending Expenses to Refund', digits=dp.get_precision('Product Unit of Measure'), compute='set_expenses_to_refund', track_visibility='always')
    payment_related_id = fields.Many2one('account.payment', string='Related Payment', compute='set_related_payment', track_visibility='always')



    def create_payment(self):
        """This method intends to display a Form View of Payments""" 
        return {
            #'name':_(""),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'account.payment',
            #'res_id': p_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {'default_comprobation_id': self.id}
        }   



    @api.one
    def set_expenses_to_refund(self):
        #Sum amounts from the same circuit by operator
        sql_query = """SELECT sum(amount) 
                         FROM wobin_comprobations 
                        WHERE circuit_id = %s AND operator_id = %s"""
        self.env.cr.execute(sql_query, (self.circuit_id.id, self.operator_id.id,))
        result = self.env.cr.fetchone()

        if result:                    
            self.expenses_to_refund = result[0]        



    @api.one
    def set_related_payment(self):
        payment_related = self.env['account.payment'].search([('comprobation_id', '=', self.id)], limit=1).id
        if payment_related:
            self.payment_related_id = payment_related