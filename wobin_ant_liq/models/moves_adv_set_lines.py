# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class WobinMovesAdvSetLines(models.Model):
    _name = 'wobin.moves.adv.set.lines'
    _description = 'Wobin Moves Advances Settlements Lines'   


    operator_id = fields.Many2one('hr.employee',string='Operator')
    circuit_id  = fields.Many2one('wobin.circuits', string='Circuit')
    trip_id     = fields.Many2one('wobin.logistica.trips', string='Trip')
    advance_id  = fields.Many2one('wobin.advances', string='Advance', ondelete='set null')
    advance_sum_amnt      = fields.Float(string='Advances', digits=dp.get_precision('Product Unit of Measure'), compute='set_advance_sum_amnt')
    comprobation_sum_amnt = fields.Float(string='Comprobations', digits=dp.get_precision('Product Unit of Measure'), compute='set_comprobation_sum_amnt')
    amount_to_settle      = fields.Float(string='Amount to Settle', digits=dp.get_precision('Product Unit of Measure'), compute='set_amount_to_settle')


    @api.one
    @api.depends('trip_id')
    def set_advance_sum_amnt(self):
        self.advance_sum_amnt = self.env['wobin.advances'].search([('trip_id', '=', self.trip_id.id)], limit=1).amount


    @api.one
    @api.depends('trip_id')    
    def set_comprobation_sum_amnt(self):
        self.comprobation_sum_amnt = self.env['wobin.comprobations'].search([('trip_id', '=', self.trip_id.id)], limit=1).amount   


    @api.one
    @api.depends('trip_id')    
    def set_amount_to_settle(self):
        self.amount_to_settle = self.comprobation_sum_amnt - self.advance_sum_amnt 




class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    flag_employee_active  = fields.Boolean(string='Flag')
    advance_sum_amnt      = fields.Float(string='Advances', digits=dp.get_precision('Product Unit of Measure'), compute='set_advance_sum_amnt')
    comprobation_sum_amnt = fields.Float(string='Comprobations', digits=dp.get_precision('Product Unit of Measure'), compute='set_comprobation_sum_amnt')
    amount_to_settle      = fields.Float(string='Amount to Settle', digits=dp.get_precision('Product Unit of Measure'), compute='set_amount_to_settle')

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
        self.amount_to_settle = self.comprobation_sum_amnt - self.advance_sum_amnt  