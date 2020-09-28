# -*- coding: utf-8 -*-

from odoo import models, fields, api

class LogisticsQuotations(models.Model):
    _name = 'logistics.quotations'
    _description = 'Logistics Quotations'

    name = fields.Char()