# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class WobinSettlements(models.Model):
    _name = 'wobin.settlements'
    _description = 'Wobin Settlements'
    _inherit = ['mail.thread', 'mail.activity.mixin']     


    @api.model
    def create(self, vals):  
        """This method intends to create a sequence for a given settlement"""
        #Change of sequence (if it isn't stored is shown "New" else e.g LIQ000005)  
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code(
                'self.settlement') or 'New'
            vals['name'] = sequence                      
        return super(WobinSettlements, self).create(vals)



    name        = fields.Char(string="Advance", readonly=True, required=True, copy=False, default='New')
    operator_id = fields.Many2one('hr.employee',string='Operator', track_visibility='always')
    date        = fields.Date(string='Date', track_visibility='always')
    trip_id     = fields.Many2one('wobin.logistica.trips', string='Trip', track_visibility='always', ondelete='cascade')
    attachments = fields.Many2many('ir.attachment', relation='settlements_attachment', string='Attachments', track_visibility='always')
    adv_set_lines_ids = fields.One2many('wobin.moves.adv.set.lines', 'id', string='Circuit Settlements for operator', compute='_set_adv_set_lines_ids')
    state             = fields.Selection(selection=[('pending', 'Pending'),
                                                    ('settled', 'Settled'),
                                                   ], string='State', required=True, readonly=True, copy=False, tracking=True, default='pending', track_visibility='always')    
    # Fields for analysis:
    advance_sum_amnt      = fields.Float(string='Advances', digits=dp.get_precision('Product Unit of Measure'), compute='set_advance_sum_amnt')
    comprobation_sum_amnt = fields.Float(string='Comprobations', digits=dp.get_precision('Product Unit of Measure'), compute='set_comprobation_sum_amnt')
    amount_to_settle      = fields.Float(string='Amount to Settle', digits=dp.get_precision('Product Unit of Measure'), compute='set_amount_to_settle')
    btn_crt_payment    = fields.Boolean(compute="set_flag_btn_crt_payment", default=False)
    btn_mark_settle    = fields.Boolean(compute="set_flag_btn_mark_settle", default=False)
    btn_debtor_new_adv = fields.Boolean(compute="set_flag_btn_debtor_new_a", default=False)
    label_process      = fields.Text(string='')
    payment_related_id = fields.Many2one('account.payment', string='Related Payment', compute='set_related_payment', ondelete='cascade')    
    acc_mov_related_id = fields.Many2one('account.move', string='Related Account Move', compute='set_related_acc_mov', ondelete='cascade')    
    advance_related_id = fields.Many2one('wobin.advances', string='Related Advance', compute='set_related_advance', ondelete='cascade')    



    @api.one
    @api.depends('trip_id')
    def _set_adv_set_lines_ids(self):
        #Fill up one2many field with data for current operator and a given trip:
        self.adv_set_lines_ids = self.env['wobin.moves.adv.set.lines'].search([('operator_id', '=', self.operator_id.id),
                                                                               ('trip_id','=', self.trip_id.id)]).ids


    @api.one
    def set_advance_sum_amnt(self):
        #Sum all amounts from the same operator whitin a given trip
        sql_query = """SELECT sum(amount) 
                         FROM wobin_advances 
                        WHERE trip_id = %s AND operator_id = %s"""
        self.env.cr.execute(sql_query, (self.trip_id.id, self.operator_id.id,))
        result = self.env.cr.fetchone()

        if result:                    
            self.advance_sum_amnt = result[0]
    


    @api.one   
    def set_comprobation_sum_amnt(self):
        #Sum all amounts from the same operator whitin a given trip
        sql_query = """SELECT sum(amount) 
                         FROM wobin_comprobations 
                        WHERE trip_id = %s AND operator_id = %s"""
        self.env.cr.execute(sql_query, (self.trip_id.id, self.operator_id.id,))
        result = self.env.cr.fetchone()

        if result:                    
            self.comprobation_sum_amnt = result[0]



    @api.one  
    def set_amount_to_settle(self):
        #Determine 'amount to settle' by doing subtraction comprobation - advance
        self.amount_to_settle = self.comprobation_sum_amnt - self.advance_sum_amnt


    @api.one
    def set_flag_btn_crt_payment(self):
        if self.amount_to_settle > 0:
            print('\n\nself.amount_to_settle', self.amount_to_settle)
            self.btn_crt_payment = True
            print('\n\nself.flag_btn_crt_payment', self.btn_crt_payment)


    @api.one
    def set_flag_btn_mark_settle(self):
        if self.amount_to_settle == 0:
            print('\n\nself.amount_to_settle', self.amount_to_settle)            
            self.btn_mark_settle = True
            print('\n\nself.btn_mark_settle', self.btn_mark_settle)


    @api.one
    def set_flag_btn_debtor_new_a(self):  
        if self.amount_to_settle < 0:
            print('\n\nself.amount_to_settle', self.amount_to_settle)
            self.btn_debtor_new_adv = True  
            print('\n\nself.flag_btn_debtor_new_a', self.btn_debtor_new_adv)  



    def create_payment(self):
        #This method intends to display a Form View of Payments:
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
    def set_related_payment(self):
        #Retrieve related payment to this settlement:
        settlement_related = self.env['account.payment'].search([('settlement_id', '=', self.id)], limit=1).id 
        if settlement_related:
            self.payment_related_id = settlement_related            

            #Display into label this settlement was finished by a payment: 
            self.label_process = 'Esta Liquidación ha sido saldada por Pago ', self.payment_related_id.name       




    @api.one
    def mark_settled(self):
        #Change state of this settlement:
        self.state = 'settled'
        
        #Display into label this settlement was finished: 
        self.label_process = 'Esta Liquidación ha sido saldada' 



    
    def send_debtor(self):
        #This method intends to display a Form View of Account Moves:
        return {
            #'name':_(""),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'account.move',
            #'res_id': p_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {'default_settlement_id': self.id}
        } 

    @api.one
    def set_related_acc_mov(self):
        #Retrieve related payment to this settlement:
        settlement_related = self.env['account.move'].search([('settlement_id', '=', self.id)], limit=1).id 
        if settlement_related:
            self.acc_mov_related_id = settlement_related            

            #Display into label this settlement was finished by a payment: 
            self.label_process = 'Esta Liquidación ha sido saldada por Movimiento Contable ', self.acc_mov_related_id.name




    def create_advance(self):
        #This method intends to display a Form View of Advances:
        return {
            #'name':_(""),
            'view_mode': 'form',
            'view_id': False,
            'view_type': 'form',
            'res_model': 'wobin.advances',
            #'res_id': p_id,
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'new',
            'domain': '[]',
            'context': {'default_settlement_id': self.id}
        } 

    @api.one
    def set_related_advance(self):
        #Retrieve related payment to this settlement:
        settlement_related = self.env['wobin.advances'].search([('settlement_id', '=', self.id)], limit=1).id 
        if settlement_related:
            self.acc_mov_related_id = settlement_related            

            #Display into label this settlement was finished by a payment: 
            self.label_process = 'Esta Liquidación ha sido saldada por Anticipo ', self.advance_related_id.name    




class AccountMove(models.Model):
    _inherit = 'account.move'

    settlement_id   = fields.Many2one('wobin.settlements', string='Settlement')