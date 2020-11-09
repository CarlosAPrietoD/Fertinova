# -*- coding: utf-8 -*-
from odoo import http

# class Reciba(http.Controller):
#     @http.route('/reciba/reciba/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/reciba/reciba/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('reciba.listing', {
#             'root': '/reciba/reciba',
#             'objects': http.request.env['reciba.reciba'].search([]),
#         })

#     @http.route('/reciba/reciba/objects/<model("reciba.reciba"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('reciba.object', {
#             'object': obj
#         })