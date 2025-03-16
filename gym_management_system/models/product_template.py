from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_gym_plan = fields.Boolean(string="Is Gym Plan?", default=False, tracking=True)
    duration = fields.Selection(
        [
            ("one_month", "1 Month"),
            ("three_months", "3 Month"),
            ("six_months", "6 Month"),
            ("one_year", "1 Year"),
        ],
        string="Duration",
        default="one_month",
        tracking=True,
    )
    benefits = fields.Text(string="Benefits")
