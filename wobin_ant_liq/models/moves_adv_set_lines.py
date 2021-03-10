# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class WobinMovesAdvSetLines(models.Model):
    _name = 'wobin.moves.adv.set.lines'
    _description = 'Wobin Moves Advances Settlements Lines'   



    settlement_id     = fields.Many2one('wobin.settlements', ondelete='cascade')
    settlement_aux_id = fields.Many2one('wobin.settlements', ondelete='cascade')
    check_selection = fields.Boolean(string=' ')
    operator_id     = fields.Many2one('hr.employee',string='Operator', ondelete='cascade')
    trip_id         = fields.Many2one('wobin.logistica.trips', string='Trip', ondelete='cascade')
    advance_ids     = fields.One2many('wobin.advances', 'mov_lns_ad_set_id', string='Related Advances', ondelete='cascade', compute='set_advances')
    comprobation_ids      = fields.One2many('wobin.comprobations', 'mov_lns_ad_set_id', string='Related Comprobations', ondelete='cascade', compute='set_comprobations')
    advance_sum_amnt      = fields.Float(string='Advances', digits=(15,2), compute='set_advance_sum_amnt')
    comprobation_sum_amnt = fields.Float(string='Comprobations', digits=(15,2), compute='set_comprobation_sum_amnt')
    amount_to_settle      = fields.Float(string='Amount to Settle', digits=(15,2), compute='set_amount_to_settle')
    settled               = fields.Boolean(string='Move Settled')
    #flag_pending_process  = fields.Boolean(string='Pending Process', compute='set_flag_pending_process')


    """
    @api.one
    def set_operator(self):
        self.operator_id = self.env['wobin.advances'].search([('mov_lns_ad_set_id', '=', self.id)], limit=1).operator_id.id


    @api.one
    def set_trip(self):
        self.trip_id = self.env['wobin.advances'].search([('mov_lns_ad_set_id', '=', self.id)], limit=1).trip_id.id    
    """

    @api.one
    @api.depends('operator_id')
    def set_advances(self):
        list_advances = self.env['wobin.advances'].search([('operator_id', '=', self.operator_id.id),
                                                           ('trip_id', '=', self.trip_id.id)]).ids                                                                   
        self.advance_ids = [(6, 0, list_advances)]
        
    

    @api.one
    @api.depends('operator_id')
    def set_comprobations(self):
        #self.comprobation_ids = [(6, 0, self.env['wobin.comprobations'].search([('mov_lns_ad_set_id', '=', self.id)]).ids)]
        list_comprobations = self.env['wobin.comprobations'].search([('operator_id', '=', self.operator_id.id),
                                                                     ('trip_id', '=', self.trip_id.id)]).ids                                                                   
        self.comprobation_ids = [(6, 0, list_comprobations)]        


    @api.one
    def set_advance_sum_amnt(self):
        #self.advance_sum_amnt = self.env['wobin.advances'].search([('mov_lns_ad_set_id', '=', self.id)], limit=1).amount        
        #Sum amounts from various advances linked to a given operator and trip:
        sql_query = """SELECT sum(amount) 
                         FROM wobin_advances 
                        WHERE operator_id = %s AND trip_id = %s"""
        self.env.cr.execute(sql_query, (self.operator_id.id, self.trip_id.id,))
        result = self.env.cr.fetchone()
        
        if result:
            self.advance_sum_amnt = result[0]        


    @api.one 
    def set_comprobation_sum_amnt(self):
        #Sum amounts from various comprobations linked to an advance:
        sql_query = """SELECT sum(amount) 
                         FROM wobin_comprobations 
                        WHERE operator_id = %s AND trip_id = %s"""
        self.env.cr.execute(sql_query, (self.operator_id.id, self.trip_id.id,))
        result = self.env.cr.fetchone()
        if result:                    
            self.comprobation_sum_amnt = result[0]        


    @api.one  
    def set_amount_to_settle(self):
        self.amount_to_settle = self.comprobation_sum_amnt - self.advance_sum_amnt 


    """
    @api.one        
    def set_flag_pending_process(self):
        flag_advances = False; flag_comprobations = False
        #Determine if comprobations have an assigened account move:
        possible_comprobations = self.env['wobin.comprobations'].search([('advance_id', '=', self.advance_id.id)])        
        for comp in possible_comprobations:
            if comp.acc_mov_related_id:
                flag_comprobations = True
            else:
                flag_comprobations = False

        

        #Determine if advance has an assigened payment:
        if self.advance_id.payment_related_id:
            flag_advances = True
        print('\n\n self.advance_id.payment_related_id', self.advance_id.payment_related_id)

        #Assign final determination only when both flags are True
        if flag_advances and flag_comprobations:
            self.flag_pending_process = True
    """




class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    flag_employee_active  = fields.Boolean(string='Flag')
    advance_sum_amnt      = fields.Float(string='Advances', digits=(15,2), compute='set_advance_sum_amnt')
    comprobation_sum_amnt = fields.Float(string='Comprobations', digits=(15,2), compute='set_comprobation_sum_amnt')
    amount_to_settle      = fields.Float(string='Amount to Settle', digits=(15,2), compute='set_amount_to_settle')

    @api.one
    def set_advance_sum_amnt(self):
        #Sum all amounts from the same operator
        advances_gotten = self.env['wobin.advances'].search([('operator_id', '=', self.id), ('money_not_consider', '=', False)])
        
        if advances_gotten:
            self.advance_sum_amnt = sum(line.amount for line in advances_gotten)
        '''
        sql_query = """SELECT sum(amount) 
                         FROM wobin_advances 
                        WHERE operator_id = %s"""
        self.env.cr.execute(sql_query, (self.id,))
        result = self.env.cr.fetchone()

        if result:                    
            self.advance_sum_amnt = result[0]
        '''
    


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