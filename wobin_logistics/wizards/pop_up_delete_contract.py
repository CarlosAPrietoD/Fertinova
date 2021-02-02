from odoo import api, fields, models 

class delete_contract_wizard(models.TransientModel):
    _name = 'wizard.delete.contract'
    _description = 'Delete Contract'
    

    def deletion(self):
        #Get Context:    
        context = self._context
        
        #Get active id from Contract viewed and to be deleted:
        contract_to_delete = context['active_id']
        
        #Deletion:
        self.env['wobin.logistica.contracts'].search([('id', '=', contract_to_delete)]).unlink()
    
        
       