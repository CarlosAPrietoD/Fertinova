from odoo import api, fields, models 

class delete_contract_wizard(models.TransientModel):

    _name = 'logistics.contract.delete'
    _description = 'Delete Contract'

    message = fields.Text(string="Are you sure you want to delete this contract?\n\nWhen you delete it, you will have to generate a new one to fill the amount pending delivery", readonly=True, store=True)

    def deletion(self):
        return {'type': 'ir.actions.act_window_close'}