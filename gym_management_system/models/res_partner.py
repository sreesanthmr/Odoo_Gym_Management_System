from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    height = fields.Float(string="Height(in cm)", required=True)
    weight = fields.Float(string="Weight(in kg)", required=True)
    bmi = fields.Float(string="BMI", compute="_compute_bmi", store=True)
    is_gym_member = fields.Boolean(string="Is Gym Member?", default=False)
    membership_id = fields.Many2one("gym.membership")
    membership_count = fields.Integer(compute="_compute_membership_count")
    body_measurements_line_ids = fields.One2many("body.measurements","member_id")

    @api.depends("height", "weight")
    def _compute_bmi(self):
        for record in self:
            if record.height > 0 and record.weight > 0:
                height_in_m = record.height / 100
                bmi = record.weight / (height_in_m**2)
                record.bmi = round(bmi, 2)

    def change_is_gym_member(self):
        for rec in self:
            if rec.is_gym_member == True:
                rec.is_gym_member = False

    @api.depends("membership_id")
    def _compute_membership_count(self):
        for rec in self:
            rec.membership_count = self.env["gym.membership"].search_count(
                [("member_id", "=", rec.id)]
            )

    def action_get_membership(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Membership",
            "view_mode": "list,form",
            "res_model": "gym.membership",
            "domain": [("member_id", "=", self.id)],
            "context": "{'create': False}",
        }

    def create_membership_invoice(self, product, amount):
        """ Create Customer Invoice of Membership for partners.
        """
        invoice_vals_list = []
        for partner in self:
            addr = partner.address_get(['invoice'])
            if not addr.get('invoice', False):
                raise UserError(_("Partner doesn't have an address to make the invoice."))

            invoice_vals_list.append({
                'move_type': 'out_invoice',
                'partner_id': partner.id,
                'invoice_line_ids': [
                    (
                        0,
                        None,
                        {
                            'product_id': product,
                            'quantity': 1,
                            'price_unit': amount,
                            # 'tax_ids': [(6, 0, product.taxes_id.filtered_domain(self.env['account.tax']._check_company_domain(self.env.company)).ids)]
                        }
                     )
                ]
            })

        return self.env['account.move'].create(invoice_vals_list)
