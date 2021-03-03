# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class WobinMovesAdvSetLines(models.Model):
    _name = 'wobin.moves.adv.set.lines'
    _description = 'Wobin Moves Advances Settlements Lines'   


    operator_id = fields.Many2one('hr.employee',string='Operator', ondelete='cascade', compute='set_operator', store=True)
    trip_id     = fields.Many2one('wobin.logistica.trips', string='Trip', ondelete='cascade', compute='set_trip', store=True)
    advance_id  = fields.Many2one('wobin.advances', string='Advance ID', ondelete='cascade', compute='set_advance', store=True)
    comprobation_ids = fields.Many2many('wobin.comprobations', string='Comprobation ID', ondelete='cascade', compute='set_comprobations', store=True)
    advance_sum_amnt      = fields.Float(string='Advances', digits=(15,2), compute='set_advance_sum_amnt')
    comprobation_sum_amnt = fields.Float(string='Comprobations', digits=(15,2), compute='set_comprobation_sum_amnt')
    amount_to_settle      = fields.Float(string='Amount to Settle', digits=(15,2), compute='set_amount_to_settle')
    flag_pending_process  = fields.Boolean(string='Pending Process', compute='set_flag_pending_process')



    @api.one
    def set_operator(self):
        self.operator_id = self.env['wobin.advances'].search([('mov_lns_ad_set_id', '=', self.id)], limit=1).operator_id.id


    @api.one
    def set_trip(self):
        self.trip_id = self.env['wobin.advances'].search([('mov_lns_ad_set_id', '=', self.id)], limit=1).trip_id.id    


    @api.one
    def set_advance(self):
        self.advance_id = self.env['wobin.advances'].search([('mov_lns_ad_set_id', '=', self.id)], limit=1).id


    @api.one
    def set_comprobations(self):
        self.comprobation_ids = [(6, 0, self.env['wobin.comprobations'].search([('mov_lns_ad_set_id', '=', self.id)]).ids)]


    @api.one
    def set_advance_sum_amnt(self):
        self.advance_sum_amnt = self.env['wobin.advances'].search([('mov_lns_ad_set_id', '=', self.id)], limit=1).amount


    @api.one 
    def set_comprobation_sum_amnt(self):
        #Sum amounts from various comprobations linked to an advance:
        sql_query = """SELECT sum(amount) 
                         FROM wobin_comprobations 
                        WHERE mov_lns_ad_set_id = %s"""
        self.env.cr.execute(sql_query, (self.id,))
        result = self.env.cr.fetchone()

        if result:                    
            self.comprobation_sum_amnt = result[0]        
        #self.comprobation_sum_amnt = self.env['wobin.comprobations'].search([('mov_lns_ad_set_id', '=', self.id)], limit=1).amount  


    @api.one  
    def set_amount_to_settle(self):
        self.amount_to_settle = self.comprobation_sum_amnt - self.advance_sum_amnt 


    
    @api.one        
    def set_flag_pending_process(self):
        flag_advances = False; flag_comprobations = False

        #Iterate multiple possible comprobations and determine if all comprobations are settled:
        for comp in self.comprobation_ids:
            if comp.acc_mov_related_id:
                flag_comprobations = True
            else:
                flag_comprobations = False

        #Determine if advance is settled:
        if self.advance_id.payment_related_id:
            flag_advances = True

        #Assign final determination only when both flags are True
        if flag_advances and flag_comprobations:
            self.flag_pending_process = True




class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    flag_employee_active  = fields.Boolean(string='Flag')
    advance_sum_amnt      = fields.Float(string='Advances', digits=(15,2), compute='set_advance_sum_amnt')
    comprobation_sum_amnt = fields.Float(string='Comprobations', digits=(15,2), compute='set_comprobation_sum_amnt')
    amount_to_settle      = fields.Float(string='Amount to Settle', digits=(15,2), compute='set_amount_to_settle')

    @api.one
    def set_advance_sum_amnt(self):
        #Sum all amounts from the same operator
        sql_query = """SELECT sum(amount) 
                         FROM wobin_advances 
                        WHERE operator_id = %s"""
        self.env.cr.execute(sql_query, (self.id,))
        result = self.env.cr.fetchone()

        if result:                    
            self.advance_sum_amnt = result[0]
    


    @api.one   
    def set_comprobation_sum_amnt(self):
        #Sum all amounts from the same operator
        sql_query = """SELECT sum(amount) 
                         FROM wobin_comprobations 
                        WHERE operator_id = %s"""
        self.env.cr.execute(sql_query, (self.id,))
        result = self.env.cr.fetchone()

        if result:                    
            self.comprobation_sum_amnt = result[0]


    @api.one  
    def set_amount_to_settle(self):
        #Determine 'amount to settle' by doing subtraction comprobation - advance        
        self.amount_to_settle = self.comprobation_sum_amnt - self.advance_sum_amnt  