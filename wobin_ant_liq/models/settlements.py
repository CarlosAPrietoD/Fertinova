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
        """This method intends to create a sequence for a given comprobation"""
        #Change of sequence (if it isn't stored is shown "New" else e.g ANT000005)  
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code(
                'self.settlement') or 'New'
            vals['name'] = sequence                      
        return super(WobinSettlements, self).create(vals)



    name        = fields.Char(string="Advance", readonly=True, required=True, copy=False, default='New')
    operator_id = fields.Many2one('hr.employee',string='Operator', track_visibility='always')
    date        = fields.Date(string='Date', track_visibility='always')
    circuit_id  = fields.Many2one('wobin.circuits', string='Circuit', track_visibility='always')
    attachments  = fields.Many2many('ir.attachment', relation='settlements_attachment', string='Attachments', track_visibility='always')
    adv_set_lines_ids = fields.One2many('wobin.moves.adv.set.lines', 'id', string='Circuit Settlements for operator', compute='_set_adv_set_lines_ids')


    @api.multi
    @api.depends('name')
    def _set_adv_set_lines_ids(self):
        for rec in self:
            rec.adv_set_lines_ids = self.env['wobin.moves.adv.set.lines'].search([('operator_id', '=', rec.operator_id.id),
                                                                                  ('circuit_id','=', rec.circuit_id.id)])