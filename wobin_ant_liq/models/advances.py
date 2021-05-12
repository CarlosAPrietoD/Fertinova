# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging
_logger = logging.getLogger(__name__)


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

            #After record was created successfully and if considering there is a new trip 
            #with new record for operator then create a new record for Wobin Moves Advances Settlements Lines 
            existing_movs = self.env['wobin.moves.adv.set.lines'].search([('operator_id', '=', res.operator_id.id),
                                                                          ('trip_id', '=', res.trip_id.id)]).ids                                                                       
            if not existing_movs:
                #Create a new record for Wobin Moves Advances Settlements Lines
                values = {
                        'operator_id': res.operator_id.id,
                        'trip_id': res.trip_id.id,
                        'advance_id': res.id,
                        }
                self.env['wobin.moves.adv.set.lines'].create(values) 


            #If a new record was created successfully and settlement related exists
            #update that settlement in order to change its state to 'settled':
            if res.settlement_id:
                settlement_obj = self.env['wobin.settlements'].browse(res.settlement_id.id)
                settlement_obj.update({'state': 'ready'})

        #Create a new record for Wobin Moves Advances Settlements Lines
        #values = {
        #          'operator_id': res.operator_id.id,
        #          'trip_id': res.trip_id.id,
        #          'advance_id': res.id
        #         }
        #mov_lns_obj = self.env['wobin.moves.adv.set.lines'].create(values) 

        #Set value of id for Wobin Moves Advances Settlements Lines in Advances:
        #res.mov_lns_ad_set_id = mov_lns_obj.id 

        #Create a new record for Wobin Settlements:
        #vals_set = {
        #            'name': self.env['ir.sequence'].next_by_code('self.settlement'),  
        #            'operator_id': res.operator_id.id,
        #            'trip_id': res.trip_id.id,
        #            'state': 'pending'
        #           }
        #self.env['wobin.settlements'].create(vals_set)         

        return res



    name        = fields.Char(string="Advance", readonly=True, required=True, copy=False, default='New')
    operator_id = fields.Many2one('hr.employee',string='Operator', track_visibility='always', ondelete='cascade')
    date        = fields.Date(string='Date', track_visibility='always')
    amount      = fields.Float(string='Amount $', digits=(15,2), track_visibility='always')
    trip_id     = fields.Many2one('wobin.logistica.trips', string='Trip', track_visibility='always', ondelete='cascade')
    expenses_to_check  = fields.Float(string='Pending Expenses to Check', digits=(15,2), compute='set_expenses_to_check', track_visibility='always')
    payment_related_id = fields.Many2one('account.payment', string='Related Payment', compute='set_related_payment', track_visibility='always')
    payment_related_id_aux = fields.Many2one('account.payment', string='Related Payment')
    mov_lns_ad_set_id      = fields.Many2one('wobin.moves.adv.set.lines', ondelete='cascade')
    mov_lns_aux_id         = fields.Many2one('wobin.moves.adv.set.lines', compute='_set_mov_lns_aux')
    settlement_id          = fields.Many2one('wobin.settlements', string='Settlement', ondelete='cascade')
    money_not_consider     = fields.Boolean(string='', default=False)
    company_id = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('your.module'))


    @api.multi
    def write(self, vals):
        #Override write method in order to detect fields changed:
        res = super(WobinAdvances, self).write(vals)  

        #If in fields changed are operator_id and trip_id update 
        #that data in its respective wobin.moves.adv.set.lines rows:
        if vals.get('operator_id', False):

            mov_lns_obj = self.env['wobin.moves.adv.set.lines'].browse(self.mov_lns_aux_id.id)
            
            if mov_lns_obj:
                mov_lns_obj.operator_id = vals['operator_id']

        if vals.get('trip_id', False):

            mov_lns_obj = self.env['wobin.moves.adv.set.lines'].browse(self.mov_lns_aux_id.id)
            
            if mov_lns_obj:
                mov_lns_obj.trip_id = vals['trip_id'] 

                sql_query = """SELECT count(*) 
                               FROM wobin_moves_adv_set_lines
                               WHERE operator_id = %s AND trip_id = %s"""
                self.env.cr.execute(sql_query, (self.operator_id.id, self.trip_id.id,))
                result = self.env.cr.fetchone()

                if result:                   
                    if result[0] > 1:
                        self.env['wobin.moves.adv.set.lines'].browse(self.mov_lns_aux_id.id).unlink()
            
            else:                
                #Considering there is a new trip with new record for operator 
                #then create a new record for Wobin Moves Advances Settlements Lines 
                existing_movs = self.env['wobin.moves.adv.set.lines'].search([('operator_id', '=', self.operator_id.id),
                                                                              ('trip_id', '=', self.trip_id.id)]).ids                                                                       
                if not existing_movs:
                    #Create a new record for Wobin Moves Advances Settlements Lines
                    values = {
                            'operator_id': self.operator_id.id,
                            'trip_id': self.trip_id.id,
                            'advance_id': self.id,
                            }
                    self.env['wobin.moves.adv.set.lines'].create(values)   

        return res                



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
    #@api.depends('name')
    def set_related_payment(self):
        #Retrieve related payment to this advance
        payment_related = self.env['account.payment'].search([('advance_id', '=', self.id), 
                                                              ('state', '!=', 'cancelled')], limit=1).id 

        if payment_related:
            self.payment_related_id = payment_related
            self.write({'payment_related_id_aux': payment_related})



    @api.one
    def _set_mov_lns_aux(self):
        mov_lns_id = self.env['wobin.moves.adv.set.lines'].search([('advance_id', '=', self.id)]).id
        if mov_lns_id: 
            self.mov_lns_aux_id = mov_lns_id 
        else:
            self.mov_lns_aux_id = self.env['wobin.moves.adv.set.lines'].search([('operator_id', '=', self.operator_id.id),
                                                                                ('trip_id', '=', self.trip_id.id)], limit=1).id