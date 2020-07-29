# -*- coding: utf-8 -*-
from odoo import api, fields, models
 

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   PRACTICE    DEVELOPED BY SEBASTIAN MENDEZ    --     START
#//////////////////////////////////////////////////////////////////////////////////////////////#


#IT'S POSSIBLE THIS ONE SHALL NOT APPEAR
class MaintenanceTeam(models.Model):
    _inherit = "maintenance.team"

    #:::::::::::::::::::::::::::::::::::::::
    # MODEL FIELDS
    #:::::::::::::::::::::::::::::::::::::::
    vehicle_selector = fields.Many2one('fleet.vehicle', required=True, store=True)


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
        

#//////////////////////////////////////////////////////////////////////////////////////////////#
#   PRACTICE    DEVELOPED BY SEBASTIAN MENDEZ    --     END
#//////////////////////////////////////////////////////////////////////////////////////////////#