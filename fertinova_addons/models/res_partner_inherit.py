class Partner(models.Model):
    _inherit = 'res.partner'
    
    zip = fields.Char('Zip', change_default=True, required=True)
