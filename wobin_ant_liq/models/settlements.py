# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class WobinConcepts(models.Model):
    _name = 'wobin.concepts'
    _description = 'Wobin Concepts'
    _inherit = ['mail.thread', 'mail.activity.mixin'] 

    name = fields.Char(string='Concept', track_visibility='always')
    account_account_id = fields.Many2one('account.account', string='Accounting Account', track_visibility='always', ondelete='cascade')
    credit_flag = fields.Boolean(string='Concept Set Like Credit')
    company_id = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('wobin.concepts'))



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



    name        = fields.Char(string="Settlement", readonly=True, required=True, copy=False, default='New')
    operator_id = fields.Many2one('hr.employee',string='Operator', track_visibility='always', ondelete='cascade')
    date        = fields.Date(string='Date', track_visibility='always')
    #trip_id     = fields.Many2one('wobin.logistica.trips', string='Trip', track_visibility='always', ondelete='cascade')
    attachments = fields.Many2many('ir.attachment', relation='settlements_attachment', string='Attachments', track_visibility='always')
    possible_adv_set_lines_ids = fields.One2many('wobin.moves.adv.set.lines', 'settlement_id', string='Possible Moves for operator')
    settled_adv_set_lines_ids  = fields.One2many('wobin.moves.adv.set.lines', 'settlement_aux_id', string='Settled Moves for operator')
    total_selected   = fields.Float(string='Total of Selected Rows $', digits=(15,2))
    total_settlement = fields.Float(string='Total of Settlement $', digits=(15,2))
    amount_to_settle = fields.Float(string='Amount to Settle $', digits=(15,2))
    state            = fields.Selection(selection = [('pending', 'Pending'),
                                                     ('ready', 'Ready to settle'),
                                                     ('settled', 'Settled'),
                                                ], string='State', required=True, readonly=True, copy=False, tracking=True, default='pending', track_visibility='always')    
    # Fields for analysis:
    advance_sum_amnt      = fields.Float(string='Advances', digits=(15,2))#, compute='set_advance_sum_amnt')
    comprobation_sum_amnt = fields.Float(string='Comprobations', digits=(15,2))#, compute='set_comprobation_sum_amnt')
    #amount_to_settle      = fields.Float(string='Amount to Settle $', digits=(15,2), compute='set_amount_to_settle')
    btn_crt_payment    = fields.Boolean(compute="set_flag_btn_crt_payment", default=False)
    btn_mark_settle    = fields.Boolean(compute="set_flag_btn_mark_settle", default=False)
    btn_debtor_new_adv = fields.Boolean(compute="set_flag_btn_debtor_new_a", default=False)
    label_process      = fields.Text(string='')
    payment_related_id = fields.Many2one('account.payment', string='Related Payment', compute='set_related_payment', ondelete='cascade')    
    #acc_mov_related_id = fields.Many2one('account.move', string='Related Account Move', compute='set_related_acc_mov', ondelete='cascade')    
    advance_related_id = fields.Many2one('wobin.advances', string='Related Advance', compute='set_related_advance', ondelete='cascade')    
    trips_related_ids  = fields.Many2many('wobin.logistica.trips')
    mov_lns_ad_set_id  = fields.Many2one('wobin.moves.adv.set.lines', ondelete='cascade')
    company_id = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('wobin.settlements'))


    @api.onchange('operator_id')
    def onchange_adv_set_lines_ids(self):
        #Fill up one2many field with data for current operator and a given trip:
        ids_gotten = self.env['wobin.moves.adv.set.lines'].search([('operator_id', '=', self.operator_id.id), ('settled', '=', False)]).ids
        self.possible_adv_set_lines_ids = [(6, 0, ids_gotten)]                   



    @api.onchange('possible_adv_set_lines_ids')
    def _onchange_comprobation_lines_ids(self):        
        # Only sum up lines which are selected by user:
        sum_amount = sum(line.amount_to_settle for line in self.possible_adv_set_lines_ids if line.check_selection == True)
        # Assign to total selected:
        self.total_selected = sum_amount  
        self.total_settlement = sum_amount
        self.amount_to_settle = sum_amount

        sum_advances = sum(line.advance_sum_amnt for line in self.possible_adv_set_lines_ids if line.check_selection == True)
        self.advance_sum_amnt = sum_advances

        sum_comprobations = sum(line.comprobation_sum_amnt for line in self.possible_adv_set_lines_ids if line.check_selection == True)
        self.comprobation_sum_amnt = sum_comprobations

        list_ids = []
        for line in self.possible_adv_set_lines_ids:
            if line.check_selection == True:
                list_ids.append(line.id)     
        self.settled_adv_set_lines_ids = [(6, 0, list_ids)] 


        list_trips = []
        for ln in self.possible_adv_set_lines_ids:
            if ln.check_selection == True:
                list_trips.append(ln.trip_id.id)
                print('\n\n\n list_trips ',list_trips)          
        self.trips_related_ids = [(6, 0, list_trips)] 
        self.update({'trips_related_ids': [(6, 0, list_trips)]})
        
        print('\n\n\n self.trips_id ', self.trips_related_ids)      
                         

    '''
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
    '''


    @api.one
    def set_flag_btn_crt_payment(self):
        #When "amount to settle" is greater or lesser than 0 just display button for payments
        #through its respectice flag and to aid in xml definition:
        if self.total_selected > 0:
            self.btn_crt_payment = True


    @api.one
    def set_flag_btn_mark_settle(self):
        #When "amount to settle" is equal to 0 (and validating that
        # at least user has some rows selected) just display button to settle
        #through its respectice flag and to aid in xml definition:
        flag = False
        
        for line in self.possible_adv_set_lines_ids:
            if line.check_selection == True:
                flag = True

        if self.total_selected == 0 and flag ==True:           
            self.btn_mark_settle = True


    @api.one
    def set_flag_btn_debtor_new_a(self):  
        #When "amount to settle" is lesser than 0 just display button for acc. move or advances
        #through its respectice flag and to aid in xml definition:        
        if self.total_selected < 0:
            self.btn_debtor_new_adv = True    



    @api.onchange('total_selected')
    def reaction_to_selected_total(self):
        flag = False

        #When "amount to settle" is greater or lesser than 0 just display button for payments
        #through its respectice flag and to aid in xml definition:
        if self.total_selected > 0:
            self.btn_crt_payment = True   

        #When "amount to settle" is equal to 0 (and validating that
        # at least user has some rows selected) just display button to settle
        #through its respectice flag and to aid in xml definition:             
        for line in self.possible_adv_set_lines_ids:
            if line.check_selection == True:
                flag = True

        if self.total_selected == 0 and flag ==True:           
            self.btn_mark_settle = True  

        #When "amount to settle" is lesser than 0 just display button for acc. move or advances
        #through its respectice flag and to aid in xml definition:        
        if self.total_selected < 0:
            self.btn_debtor_new_adv = True  
                                     



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
            'context': {'default_settlement_id': self.id}
        } 

    @api.one
    def set_related_payment(self):
        #Retrieve related payment to this settlement:
        settlement_related = self.env['account.payment'].search([('settlement_id', '=', self.id)], limit=1).id 
        if settlement_related:
            self.payment_related_id = settlement_related 




    @api.one
    def mark_settled(self):
        #Change state of this settlement:
        self.state = 'settled'
        
        #Display into label this settlement was finished: 
        self.label_process = 'Esta Liquidación ha sido saldada' 

        for line in self.possible_adv_set_lines_ids:
            if line.check_selection == True:        
                line.update({'settled': True})         



    
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
            'context': {'default_settlement_id': self.id, 'default_money_not_consider': True}
        } 

    @api.one
    def set_related_advance(self):
        #Retrieve related payment to this settlement:
        settlement_related = self.env['wobin.advances'].search([('settlement_id', '=', self.id)], limit=1).id 
        if settlement_related:            
            self.advance_related_id = settlement_related 
              


    def settle_operation(self):
        #Change state of this settlement if proccess is set up 
        #because already exists a payment, acc. move or advance related with this settlement:
        self.state = 'settled' 

        if self.payment_related_id:
            #Display into label this settlement was finished by a payment: 
            self.label_process = 'Esta Liquidación ha sido saldada por Pago ' + self.payment_related_id.name                                                    

        #if self.acc_mov_related_id:
            #Display into label this settlement was finished by an account move: 
            #self.label_process = 'Esta Liquidación ha sido saldada por Movimiento Contable ' + self.acc_mov_related_id.name                              

        if self.advance_related_id:
            #Display into label this settlement was finished by an advance: 
            self.label_process = 'Esta Liquidación ha sido saldada por Anticipo ' + self.advance_related_id.name 
        
        for line in self.settled_adv_set_lines_ids:
            if line.check_selection == True:
                line.settled = True         
        
        for line in self.possible_adv_set_lines_ids:
            if line.check_selection == True:
                line.update({'settled': True})    
                line.write({'settled': True})

        self.amount_to_settle = None                             





# *******************************************************************
#  Some inheritances made to Account Models
# *******************************************************************

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    advance_id    = fields.Many2one('wobin.advances', string='Advance')     
    settlement_id = fields.Many2one('wobin.settlements', string='Settlement')

    @api.model
    def create(self, vals):
        #Try to modify flow in order to upate state in possible settlement related:
        res = super(AccountPayment, self).create(vals)

        #If a new record was created successfully and settlement related exists
        #update that settlement in order to change its state to 'settled':
        if res.settlement_id:
            settlement_obj = self.env['wobin.settlements'].browse(res.settlement_id.id)
            settlement_obj.update({'state': 'ready'})                   
        return res    




class AccountMove(models.Model):
    _inherit = 'account.move'

    settlement_id   = fields.Many2one('wobin.settlements', string='Settlement')
    comprobation_id = fields.Many2one('wobin.comprobations', string='Comprobation')    

    @api.model
    def create(self, vals):
        #Try to modify flow in order to upate state in possible settlement related:
        res = super(AccountMove, self).create(vals)

        #If a new record was created successfully and settlement related exists
        #update that settlement in order to change its state to 'settled':
        if res.settlement_id:
            settlement_obj = self.env['wobin.settlements'].browse(res.settlement_id.id)
            settlement_obj.update({'state': 'ready'})        
        return res
    




class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    contact_deb_cred_id = fields.Many2one('res.partner', string='Contact Debtor/Creditor')
    




class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    contact_id = fields.Many2one('res.partner', string='Contact')
    enterprise_id = fields.Many2one('res.partner', string='Enterprise')
    flag_employee_active  = fields.Boolean(string='Flag') 