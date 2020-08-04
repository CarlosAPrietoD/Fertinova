# -*- coding: utf-8 -*-
from odoo import http

# class TransportesAlbaCustoms(http.Controller):
#     @http.route('/transportes_alba_customs/transportes_alba_customs/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/transportes_alba_customs/transportes_alba_customs/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('transportes_alba_customs.listing', {
#             'root': '/transportes_alba_customs/transportes_alba_customs',
#             'objects': http.request.env['transportes_alba_customs.transportes_alba_customs'].search([]),
#         })

#     @http.route('/transportes_alba_customs/transportes_alba_customs/objects/<model("transportes_alba_customs.transportes_alba_customs"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('transportes_alba_customs.object', {
#             'object': obj
#         })