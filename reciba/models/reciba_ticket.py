from odoo import models, fields, api

class RecibaTicket(models.Model):
    _name = 'reciba.ticket'
    _description = 'Boletas'

    name = fields.Char(string="Name")