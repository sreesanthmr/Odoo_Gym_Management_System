from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    
    def create(self, vals):
        for rec in self:
            membership = self.env["gym.membership"].search([("member_id", "=", self.partner_id.id)])
            membership.invoice_ids = [(4, rec.id)]

        return super(AccountMove, self).create(vals)

    def write(self,vals):
        for rec in self:
            rec.ensure_one()
            if rec.payment_state == "paid":
                membership = self.env["gym.membership"].search([("member_id", "=", self.partner_id.id)])
                membership.state = "paid"

        return super(AccountMove, self).write(vals)
