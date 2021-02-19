# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    advance_id      = fields.Many2one('wobin.advances', string='Advance')
    comprobation_id = fields.Many2one('wobin.comprobations', string='Comprobation') 
    settlement_id   = fields.Many2one('wobin.settlements', string='Settlement')



class WobinAdvances(models.Model):
    _name = 'wobin.advances'
    _description = 'Wobin Advances'
    _inherit = ['mail.thread', 'mail.activity.mixin']      


    @api.model
    def create(self, vals):  
        """This method intends to create a sequence for a given advance"""            
        #Change of sequence (if it isn't stored is shown "New" else e.g ANT000005) 
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code(
                'self.advance') or 'New'
            vals['name'] = sequence  
          
            #Update flag to indicate employee for checking up:
            employee_obj = self.env['hr.employee'].browse(vals['operator_id'])
            employee_obj.flag_employee_active = True

            res = super(WobinAdvances, self).create(vals)

        #Create a new record for Wobin Moves Advances Settlements Lines
        values = {
                  'operator_id': res.operator_id.id,
                  'trip_id': res.trip_id.id,
                  'advance_id': res.id
                 }
        mov_lns_obj = self.env['wobin.moves.adv.set.lines'].create(values) 

        #Set value of id for Wobin Moves Advances Settlements Lines in Advances:
        res.mov_lns_ad_set_id = mov_lns_obj.id 

        #Create a new record for Wobin Settlements:
        vals_set = {
                    'name': self.env['ir.sequence'].next_by_code('self.settlement'),  
                    'operator_id': res.operator_id.id,
                    'trip_id': res.trip_id.id,
                    'state': 'pending'
                   }
        self.env['wobin.settlements'].create(vals_set)         

        return res


    name        = fields.Char(string="Advance", readonly=True, required=True, copy=False, default='New')
    operator_id = fields.Many2one('hr.employee',string='Operator', track_visibility='always', ondelete='cascade')
    date        = fields.Date(string='Date', track_visibility='always')
    amount      = fields.Float(string='Amount $', digits=dp.get_precision('Product Unit of Measure'), group_operator=False, track_visibility='always')
    trip_id     = fields.Many2one('wobin.logistica.trips', string='Trip', track_visibility='always', ondelete='cascade')
    expenses_to_check  = fields.Float(string='Pending Expenses to Check', digits=dp.get_precision('Product Unit of Measure'), compute='set_expenses_to_check', track_visibility='always')
    payment_related_id = fields.Many2one('account.payment', string='Related Payment', compute='set_related_payment', ondelete='cascade', track_visibility='always')
    mov_lns_ad_set_id  = fields.Many2one('wobin.moves.adv.set.lines', string='Movs Lns Adv Set Id', ondelete='cascade')
    settlement_id      = fields.Many2one('wobin.settlements', string='Settlement')




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
            'context': {'default_advance_id': self.id}
        }   



    @api.one
    def set_expenses_to_check(self):
        #Sum amounts from the same trip by operator
        sql_query = """SELECT sum(amount) 
                         FROM wobin_advances 
                        WHERE trip_id = %s AND operator_id = %s"""
        self.env.cr.execute(sql_query, (self.trip_id.id, self.operator_id.id,))
        result = self.env.cr.fetchone()

        if result:                    
            self.expenses_to_check = result[0]
    


    @api.one
    def set_related_payment(self):
        #Retrieve related payment to this advance
        payment_related = self.env['account.payment'].search([('advance_id', '=', self.id)], limit=1).id 
        if payment_related:
            self.payment_related_id = payment_related