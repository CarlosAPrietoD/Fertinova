# -*- coding: utf-8 -*-
from odoo import models, fields, api

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   TICKET 164    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class AccountPayment(models.Model):
    _inherit = 'account.payment'
    
    #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    #             MODEL FIELDS
    #state = fields.Selection(selection_add=[('authorized', 'Autorizado'), ('draft',)])
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('authorized', 'Autorizado'),
        ('posted', 'Posted'),
        ('sent', 'Sent'),
        ('reconciled', 'Reconciled'),
        ('cancelled', 'Cancelled')
        ], string='Status', required=True, readonly=True, copy=False, tracking=True, default='draft')    
    
    bank_account_id = fields.Many2one('res.partner.bank', string='Cuenta Diario Pago', 
                                      compute='_compute_bank_account', readonly=False)
    
    invoices_id     = fields.Many2one('account.invoice', 
                                      string='Factura', readonly=False,
                                      default=lambda self: self.env['account.invoice'].search([('partner_id', '=', self.partner_id.id), 
                                                                                               ('state', 'not in', ['paid', 'cancel'])]))
    
    purchases_id    = fields.Many2one('purchase.order', 
                                      string='Orden de Compra', readonly=False,
                                      default=lambda self: self.env['purchase.order'].search([('partner_id', '=', self.partner_id.id), 
                                                                                               ('state', 'not in', ['done', 'cancel'])]))

    #\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\-\
    #             METHOD FIELDS
    @api.depends('journal_id')
    def _compute_bank_account(self):
        self.bank_account_id = self.env['account.journal'].search([('id', '=', self.journal_id.id)]).bank_account_id.id
    
    def change_state_authorized(self):
        self.state = 'authorized'  
        
    @api.multi
    def post(self):
        """ Create the journal items for the payment and update the payment's state to 'posted'.
            A journal entry is created containing an item in the source liquidity account (selected journal's default_debit or default_credit)
            and another in the destination reconcilable account (see _compute_destination_account_id).
            If invoice_ids is not empty, there will be one reconcilable move line per invoice to reconcile with.
            If the payment is a transfer, a second journal entry is created in the destination journal to receive money from the transfer account.
        """
        for rec in self:

            #if rec.state != 'draft':
            #    raise UserError(_("Only a draft payment can be posted."))

            if any(inv.state != 'open' for inv in rec.invoice_ids):
                raise ValidationError(_("The payment cannot be processed because the invoice is not open!"))

            # keep the name in case of a payment reset to draft
            if not rec.name:
                # Use the right sequence to set the name
                if rec.payment_type == 'transfer':
                    sequence_code = 'account.payment.transfer'
                else:
                    if rec.partner_type == 'customer':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.customer.invoice'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.customer.refund'
                    if rec.partner_type == 'supplier':
                        if rec.payment_type == 'inbound':
                            sequence_code = 'account.payment.supplier.refund'
                        if rec.payment_type == 'outbound':
                            sequence_code = 'account.payment.supplier.invoice'
                rec.name = self.env['ir.sequence'].with_context(ir_sequence_date=rec.payment_date).next_by_code(sequence_code)
                if not rec.name and rec.payment_type != 'transfer':
                    raise UserError(_("You have to define a sequence for %s in your company.") % (sequence_code,))

            # Create the journal entry
            amount = rec.amount * (rec.payment_type in ('outbound', 'transfer') and 1 or -1)
            move = rec._create_payment_entry(amount)
            persist_move_name = move.name

            # In case of a transfer, the first journal entry created debited the source liquidity account and credited
            # the transfer account. Now we debit the transfer account and credit the destination liquidity account.
            if rec.payment_type == 'transfer':
                transfer_credit_aml = move.line_ids.filtered(lambda r: r.account_id == rec.company_id.transfer_account_id)
                transfer_debit_aml = rec._create_transfer_entry(amount)
                (transfer_credit_aml + transfer_debit_aml).reconcile()
                persist_move_name += self._get_move_name_transfer_separator() + transfer_debit_aml.move_id.name

            rec.write({'state': 'posted', 'move_name': persist_move_name})
        return True
