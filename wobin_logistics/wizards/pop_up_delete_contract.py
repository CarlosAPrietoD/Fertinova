from odoo import api, fields, models 

class delete_contract_wizard(models.TransientModel):
    _name = 'wizard.delete.contract'
    _description = 'Delete Contract'

    message  = fields.Char(string="Are you sure you want to delete this contract?", readonly=True)
    message2 = fields.Char(string="When you delete it, you will have to generate a new one to fill the amount pending delivery", readonly=True)


    def deletion(self):
        #Get Context:
        print('\n\n\n context: ',self._context)
        context = self._context
        #Get active id from Contract viewed and to be deleted:
        contract_to_delete = context['active_id']
        print('\n\n\n contract_to_delete: ', contract_to_delete)
        #Deletion:
        self.env['logistics.contracts'].search([('id', '=', contract_to_delete)]).unlink()
    
        
       