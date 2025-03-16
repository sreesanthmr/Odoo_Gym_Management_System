from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = "res.users"

    def create(self,vals):
        user = super(ResUsers, self).create(vals)
        user.partner_id.email = user.login

        return user