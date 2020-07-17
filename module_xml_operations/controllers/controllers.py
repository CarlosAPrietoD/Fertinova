# -*- coding: utf-8 -*-
from odoo import http

# class ModuleXmlOperations(http.Controller):
#     @http.route('/module_xml_operations/module_xml_operations/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/module_xml_operations/module_xml_operations/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('module_xml_operations.listing', {
#             'root': '/module_xml_operations/module_xml_operations',
#             'objects': http.request.env['module_xml_operations.module_xml_operations'].search([]),
#         })

#     @http.route('/module_xml_operations/module_xml_operations/objects/<model("module_xml_operations.module_xml_operations"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('module_xml_operations.object', {
#             'object': obj
#         })