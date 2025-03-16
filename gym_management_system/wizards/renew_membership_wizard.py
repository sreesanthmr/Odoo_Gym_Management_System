from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class RenewMembershipWizard(models.TransientModel):
    _name = "renew.membership.wizard"
    _description = "Renew Membership Wizard"

    membership_id = fields.Many2one(
        "gym.membership", default=lambda self: self.env.context.get("active_id")
    )
    membership_plan_id = fields.Many2one("product.product", string="Membership Plan", required=True)
    membership_date_from = fields.Date(
        string="Membership Start Date", default=date.today()
    )
    membership_date_to = fields.Date(string="Membership End Date")
    membership_fees = fields.Float(string="Membership Fees")

    def submit_membership(self):
        for record in self:
            record.membership_id.membership_plan_id = record.membership_plan_id
            record.membership_id.membership_date_from = record.membership_date_from
            record.membership_id.membership_date_to = record.membership_date_to
            record.membership_id.membership_fees = record.membership_fees
            record.membership_id.state = "confirm"

    @api.onchange("membership_plan_id")
    def onchange_membership_plan(self):
        price_dict = self.membership_plan_id._price_compute("list_price")
        self.membership_fees = price_dict.get(self.membership_plan_id.id) or False

        duration = self.membership_plan_id.duration
        if duration == "one_month":
            self.membership_date_to = date.today() + relativedelta(days=30)
        elif duration == "three_months":
            self.membership_date_to = date.today() + relativedelta(months=3)
        elif duration == "six_months":
            self.membership_date_to = date.today() + relativedelta(months=6)
        elif duration == "one_year":
            self.membership_date_to = date.today() + relativedelta(years=1)
