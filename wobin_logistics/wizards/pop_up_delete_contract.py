from odoo import api, fields, models 

class delete_contract_wizard(models.TransientModel):
    _name = 'wizard.delete.contract'
    _description = 'Delete Contract'
    

    def deletion(self):
        #Get Context:
        print('\n\n\n context: ',self._context)
        context = self._context
        #Get active id from Contract viewed and to be deleted:
        contract_to_delete = context['active_id']
        print('\n\n\n contract_to_delete: ', contract_to_delete)
        #Deletion:
        self.env['logistics.contracts'].search([('id', '=', contract_to_delete)]).unlink()
    
        
       