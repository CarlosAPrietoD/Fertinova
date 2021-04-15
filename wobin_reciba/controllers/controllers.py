# -*- coding: utf-8 -*-
from odoo import http

# class WobinReciba(http.Controller):
#     @http.route('/wobin_reciba/wobin_reciba/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/wobin_reciba/wobin_reciba/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('wobin_reciba.listing', {
#             'root': '/wobin_reciba/wobin_reciba',
#             'objects': http.request.env['wobin_reciba.wobin_reciba'].search([]),
#         })

#     @http.route('/wobin_reciba/wobin_reciba/objects/<model("wobin_reciba.wobin_reciba"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('wobin_reciba.object', {
#             'object': obj
#         })