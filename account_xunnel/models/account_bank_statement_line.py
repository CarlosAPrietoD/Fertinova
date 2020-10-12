# Copyright 2019, Vauxoo, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


from odoo import fields, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    card_number = fields.Char(
        help="Some banks won't provide this data.")
