from odoo import models, fields, api

class AccountPayment(models.Model):
    _inherit = 'account.payment'


    @api.onchange('payment_type')
    def get_payment_type(self):
        user = self.env['res.users'].browse(self.env.uid)
        company=user.company_id.name
        
        if company == 'TRANSPORTES DE ALBA SA DE CV':
            
            if self.payment_type == 'transfer':
                
                journal = self.env['account.journal'].search([('name', '=', 'TA. DEPÓSITOS POR ASIGNAR')], limit=1)
                contact = self.env['res.partner'].search([('name', '=', 'DEPÓSITOS POR ASIGNAR')], limit=1)
                
                self.journal_id = journal.id
                self.x_studio_contacto_deudor_acreedor_1 = contact.id
                self.destination_journal_id = journal.id
                print("==============")
            

        