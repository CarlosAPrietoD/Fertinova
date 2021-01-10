from odoo import api, fields, models 

class delete_contract_wizard(models.TransientModel):

    _name = 'logistics.contract.delete'
    _description = 'Delete Contract'

    message = fields.Text(string="TEST about this pop up", readonly=True, store=True)