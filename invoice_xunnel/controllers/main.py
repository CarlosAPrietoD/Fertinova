
from odoo import http
from odoo.addons.web.controllers.main import Binary


class BinaryInherit(Binary):

    @http.route()
    def content_common(self, *args, **kw):
        response = super().content_common(*args, **kw)
        if response.status_code == 200 and kw.get('raw_html'):
            result = response.response
            if isinstance(result, list):
                result = result[0]
            if isinstance(result, bytes):
                result = result.decode()
            return result
        return response
