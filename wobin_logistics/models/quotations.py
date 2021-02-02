# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WobinLogisticaQuotations(models.Model):
    _name = 'wobin.logistica.quotations'
    _description = 'Logistics Quotations'

    name = fields.Char()