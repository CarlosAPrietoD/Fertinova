# -*- coding: utf-8 -*-
from odoo import api, fields, models
 

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   PRACTICE    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#
class MaintenanceEquipment(models.Model):
    _inherit = "maintenance.equipment"

    #:::::::::::::::::::::::::::::::::::::::
    # MODEL FIELDS
    #:::::::::::::::::::::::::::::::::::::::
    vehicle = fields.Many2one('fleet.vehicle', required=True, store=True)


class MaintenanceRequest(models.Model):
    _inherit = "maintenance.request"

    #:::::::::::::::::::::::::::::::::::::::
    # MODEL FIELDS
    #:::::::::::::::::::::::::::::::::::::::
    vehicle = fields.Many2one('fleet.vehicle', required=True, store=True)         
    
    @api.onchange('equipment_id')
    def _onchange_equipment(self):
        self.vehicle = self.env['maintenance.equipment'].search([('id', '=', self._origin.id)]).vehicle.id
#//////////////////////////////////////////////////////////////////////////////////////////////#
#   PRACTICE    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#