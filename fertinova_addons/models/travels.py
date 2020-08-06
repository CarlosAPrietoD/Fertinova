from odoo import api, models, fields

class FleetTravel(models.Model):
    #=============================================Tabla de viajes===========================================
    _name = "fleet.travel"

    def accordance_change(self):
        self.condition='accordance'

    def adjustment_change(self):
        self.condition='adjustment'
        
    #============Meotodo para asignar automaticamente la etiqueta de viaje=============================
    @api.model
    def create(self, vals):
        travel = super(FleetTravel, self).create(vals)
        #==================Buscamos los viajes asignados anteriormente a ese vehiculo==================
        travels = travel.env['fleet.travel'].search([('vehicle', '=', travel.vehicle.id)])
        n=len(travels)
        tag_string='V: '+str(n)
        #============Si la etiqueta del viaje actual ya está creada solo se asigna, de lo contrario es creada===
        tag = travel.env['account.analytic.tag'].search([('name', '=', tag_string)], limit=1)
        if tag:
            travel.travel_tag=tag
        else:
            vals = {
                    'name': tag_string
                }
            new_tag = self.env['account.analytic.tag'].create(vals)
            travel.travel_tag=new_tag
        
        return travel


    #==============metodo para cambiar el estado del viaje al llenar ciertos campos============== 
    @api.multi
    @api.onchange('vehicle','route_tag','driver_tag','cargo_date','cargo_qty','unload_date','unload_qty')
    def _onchange_state(self):
        if self.vehicle and self.route_tag and self.driver_tag:
            if not self.cargo_date or not self.cargo_qty or not self.unload_date or not self.unload_qty:
                self.state = 'asigned'
        if self.vehicle and self.route_tag and self.driver_tag and self.cargo_date and self.cargo_qty:
            if not self.unload_date or not self.unload_qty:
                self.state = 'route'
        if self.vehicle and self.route_tag and self.driver_tag and self.cargo_date and self.cargo_qty and self.unload_date and self.unload_qty:
            self.state = 'discharged'
        



    customer = fields.Many2one('res.partner', string="Customer", required=True)
    travel_tag = fields.Many2one('account.analytic.tag', string="Travel", readonly=True)
    route_tag = fields.Many2one('account.analytic.tag', string="Route", required=True)
    driver_tag = fields.Many2one('account.analytic.tag', string="Driver", required=True)
    vehicle = fields.Many2one('fleet.vehicle', string="Vehicle", required=True)
    advance = fields.Float(string="Advance")
    travel_init = fields.Date(string="Travel init")
    cargo_date = fields.Date(string="Cargo date")
    cargo_qty = fields.Float(string="Quantity")
    unload_date = fields.Date(string="Unload date")
    unload_qty = fields.Float(string="Unload quantity")
    accordance_payment = fields.Binary(string="Accordance Payment")
    file_name = fields.Char()
    condition = fields.Selection([('accordance', 'Conformidad'), ('adjustment', 'Ajustes'), ('authorized', 'Autorizado')])
    state = fields.Selection([('asigned', 'Asignado'), ('route', 'Ruta'),('discharged','Descargado')])