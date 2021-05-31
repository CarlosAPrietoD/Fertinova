from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    zip = fields.Char('Zip', change_default=True, required=True)
