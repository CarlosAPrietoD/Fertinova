# -*- coding: utf-8 -*-
import base64
from odoo import models, fields, api

class module_xml_operations(models.Model):
    _name = 'xml.operations'
    _inherit = ['mail.thread', 'mail.activity.mixin']    
    _description = 'Module for reading XMLs'
    

    #::::::::::::::::::::::::::::::::::::::::
    #  Model Fields
    #::::::::::::::::::::::::::::::::::::::::
    name          = fields.Char('Name')
    xml_file      = fields.Binary(string='XML File:', compute='read_xml')
    check_ppd     = fields.Boolean(string='Is it PPD?')
    check_payment = fields.Boolean(string='Has it already uploaded Payment Complement?')
 
    #::::::::::::::::::::::::::::::::::::::::
    #  Model Methods
    #::::::::::::::::::::::::::::::::::::::::
    def read_xml(self):
        x_file = base64.decodestring(self.xml_file).decode("utf-8")
        print(x_file)