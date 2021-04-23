# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


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
                        }
                movs = self.env['wobin.moves.adv.set.lines'].create(values) 
                _logger.info('\n\n\n movs %s\n\n\n', movs) 
                _logger.info('\n\n\n movs.id ID %s\n\n\n', movs.id) 
                res.mov_lns_ad_set_id_aux = movs.id 
                _logger.info('\n\n\nres.mov_lns_ad_set_id_aux%s\n\n\n', res.mov_lns_ad_set_id_aux)



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
    mov_lns_ad_set_id_aux  = fields.Many2one('wobin.moves.adv.set.lines', ondelete='cascade')
    settlement_id          = fields.Many2one('wobin.settlements', string='Settlement', ondelete='cascade')
    money_not_consider     = fields.Boolean(string='', default=False)
    company_id = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('your.module'))



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
        payment_related = self.env['account.payment'].search([('advance_id', '=', self.id)], limit=1).id 

        if payment_related:
            self.payment_related_id = payment_related
            self.write({'payment_related_id_aux': payment_related})



    @api.onchange('operator_id')
    def _onchange_operator_id(self):                       
        _logger.info('\n\n\n UPDATE self.mov_lns_ad_set_id_aux.id %s\n\n\n', self.mov_lns_ad_set_id_aux.id)
        _logger.info('\n\n\n UPDATE origin.mov_lns_ad_set_id_aux.id %s\n\n\n', self._origin.mov_lns_ad_set_id_aux.id)
        movs_obj = self.env['wobin.moves.adv.set.lines'].search([('id', '=', self._origin.mov_lns_ad_set_id_aux.id)])
        _logger.info('\n\n\n movs.id UPDATE ID %s\n\n\n', movs_obj)
        #movs_obj.update({'operator_id': self._origin.operator_id.id})
        if movs_obj:
            movs_obj.operator_id = self.operator_id.id