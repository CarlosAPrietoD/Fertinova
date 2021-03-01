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
        #Change of sequence (if it isn't stored is shown "New" else e.g COMP000005)  
        if vals.get('name', 'New') == 'New':
            sequence = self.env['ir.sequence'].next_by_code(
                'self.comprobation') or 'New'
            vals['name'] = sequence    

        res = super(WobinComprobations, self).create(vals)  

        #Intend to link this record with Wobin Moves Advances Settlements Lines:
        operator = res.operator_id.id
        trip     = res.trip_id.id
        advance  = res.advance_id.id
        
        get_id_mvs = self.env['wobin.moves.adv.set.lines'].search([('operator_id', '=', operator),
                                                                   ('trip_id', '=', trip),
                                                                   ('advance_id', '=', advance)], limit=1)
                                                                       
        mov_lns_obj = self.env['wobin.moves.adv.set.lines'].browse(get_id_mvs.id)
        mov_lns_obj.write({'comprobation_id': res.id}) 

        #Set value of id for Wobin Moves Advances Settlements Lines in Advances:
        res.mov_lns_ad_set_id = mov_lns_obj.id                                                                                                   

        return res


    name        = fields.Char(string="Advance", readonly=True, required=True, copy=False, default='New')
    operator_id = fields.Many2one('hr.employee',string='Operator', track_visibility='always', ondelete='cascade')
    date        = fields.Date(string='Date', track_visibility='always')
    amount      = fields.Float(string='Amount $', digits=(15,2), group_operator=False, compute='set_amount', track_visibility='always')
    trip_id     = fields.Many2one('wobin.logistica.trips', string='Trip', track_visibility='always', ondelete='cascade')
    expenses_to_refund = fields.Float(string='Pending Expenses to Refund', digits=(15,2), compute='set_expenses_to_refund', track_visibility='always')
    acc_mov_related_id = fields.Many2one('account.move', string='Related Account Move', compute='set_related_acc_mov', track_visibility='always', ondelete='cascade')
    advance_id         = fields.Many2one('wobin.advances', string='Advance ID', ondelete='cascade')
    mov_lns_ad_set_id  = fields.Many2one('wobin.moves.adv.set.lines', string='Movs Lns Adv Set Id', ondelete='cascade')
    comprobation_lines_ids = fields.One2many('wobin.comprobation.lines', 'comprobation_id', string='Concept Lines')
    


    def create_acc_mov(self):
        #This method intends to display a Form View of Account Move        
        context_modified = False

        # Subprocess:
        #Consult different models in order to fill up by default some fields in 
        #pop up window of account move
        enterprise_id       = self.env['hr.employee'].search([('id', '=', self.operator_id.id)], limit=1).enterprise_id.id
        contact_id          = self.env['hr.employee'].search([('id', '=', self.operator_id.id)], limit=1).contact_id.id
        analytic_account_id = self.env['wobin.logistica.trips'].search([('id', '=', self.trip_id.id)], limit=1).analytic_accnt_id.id
        analytic_tag_ids    = self.env['account.analytic.tag'].search([('name', '=', self.trip_id.name)], limit=1).ids


        #Retrieve related payment of advance in this comprobation:
        payment_related = self.env['account.payment'].search([('advance_id', '=', self.advance_id.id)], limit=1) 
        
        if payment_related:
            #Get journal name from payment consulted and determine if it contains "Contabilidad B"
            journal = self.env['account.journal'].search([('id', '=', payment_related.journal_id.id)], limit=1)

            journal_id = journal.id
            journal_name = journal.name
            
            if journal_name:
                substring = "Contabilidad B"
                
                if substring in journal_name:
                    context_modified = True
                    ctxt = {'default_comprobation_id': self.id,
                            'default_journal_id': journal_id,
                            'default_line_ids': [(0, 0, {'partner_id': enterprise_id, 
                                                 'contact_deb_cred_id': contact_id,
                                                 'analytic_account_id': analytic_account_id,
                                                 'analytic_tag_ids': analytic_tag_ids}
                                                )]
                           }
        
        if context_modified == False:
            ctxt = {'default_comprobation_id': self.id,
                    'default_line_ids': [(0, 0, {'partner_id': enterprise_id, 
                                                 'contact_deb_cred_id': contact_id,
                                                 'analytic_account_id': analytic_account_id,
                                                 'analytic_tag_ids': analytic_tag_ids}
                                         )]
                   }            
         
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
            'context': ctxt
        }  



    @api.one
    def set_amount(self):
        self.amount = sum(line.amount for line in self.comprobation_lines_ids)



    @api.one
    def set_expenses_to_refund(self):
        #Sum amounts from the same trip by operator
        sql_query = """SELECT sum(amount) 
                         FROM wobin_comprobations 
                        WHERE trip_id = %s AND operator_id = %s"""
        self.env.cr.execute(sql_query, (self.trip_id.id, self.operator_id.id,))
        result = self.env.cr.fetchone()

        if result:                    
            self.expenses_to_refund = result[0]        



    @api.one
    def set_related_acc_mov(self):
        acc_mov_related = self.env['account.move'].search([('comprobation_id', '=', self.id)], limit=1).id
        if acc_mov_related:
            self.acc_mov_related_id = acc_mov_related




class WobinComprobationLines(models.Model):
    _name = 'wobin.comprobation.lines'
    _description = 'Wobin Comprobation Lines'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    
    _sql_constraints = [
                        ('concept_line_uniq', 
                         'unique (concept_id)',     
                         'Conceptos Duplicados en Líneas de Comprobación no permitidos')
                       ]

    comprobation_id = fields.Many2one('wobin.comprobations', string='Comprobation Reference', required=True, ondelete='cascade', index=True)
    concept_id = fields.Many2one('wobin.concepts', string='Concept', track_visibility='always')
    amount = fields.Float(string='Amount $', digits=(15,2), track_visibility='always')