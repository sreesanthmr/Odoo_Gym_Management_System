from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError
import random


class GymMembership(models.Model):
    _name = "gym.membership"
    _description = "Gym Membership"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "reference"

    reference = fields.Char(
        string="Reference",
        required=True,
        copy=False,
        readonly=True,
        default="New",
    )
    member_id = fields.Many2one(
        "res.partner", string="Member", domain=[("is_gym_member", "=", True)], default=lambda self: self.env.user
    )
    membership_plan_id = fields.Many2one(
        "product.product",
        string="Membership Plan",
        tracking=True,
    )
    training_type = fields.Selection(
        [
            ("common_training", "Common Training"),
            ("personal_training", "Personal Training"),
        ],
        string="Training Type",
        default="common_training",
        tracking=True,
    )
    trainer_id = fields.Many2one(
        "hr.employee",
        string="Trainer",
        tracking=True,
    )
    membership_fees = fields.Float(string="Membership Fees", tracking=True)
    membership_date_from = fields.Date(
        string="Membership Start Date",
        default=date.today(),
        tracking=True,
    )
    membership_date_to = fields.Date(string="Membership End Date", tracking=True)

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirm", "Confirmed"),
            ("payment_pending", "Payment Pending"),
            ("paid", "Paid"),
            ("cancel", "Cancelled"),
            ("expire", "Expired"),
        ],
        string="Status",
        default="draft",
        tracking=True,
    )
    invoice_ids = fields.Many2many("account.move")
    invoice_count = fields.Integer(compute="_compute_invoice_count")

    def action_confirm(self):
        for record in self:
            record.state = "confirm"
            trainers = self.env["hr.employee"].search([("is_gym_trainer", "=", "True")])
            if trainers:
                self.trainer_id = random.choice(trainers).id


    def action_cancel(self):
        for record in self:
            if record.state == "payment_pending":
                invoices = self.env["account.move"].search(
                    [("partner_id", "=", record.member_id.id)]
                )
                invoices.unlink()
            record.state = "cancel"

    def action_draft(self):
        for record in self:
            record.state = "draft"

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

    def membership_invoice(self):
        invoice_list = self.create_membership_invoice(
            self.member_id, self.membership_plan_id, self.membership_fees
        )
        search_view_ref = self.env.ref("account.view_account_invoice_filter", False)
        form_view_ref = self.env.ref("account.view_move_form", False)
        list_view_ref = self.env.ref("account.view_move_tree", False)

        self.state = "payment_pending"

        for rec in self:
            rec.invoice_count = self.env["account.move"].search_count(
                [("partner_id", "=", rec.member_id.id)]
            )

        return {
            "domain": [("id", "in", invoice_list.ids)],
            "name": "Membership Invoices",
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "views": [(list_view_ref.id, "list"), (form_view_ref.id, "form")],
            "search_view_id": search_view_ref and [search_view_ref.id],
        }

    def create_membership_invoice(self, member, membership_plan, membership_fees):
        """Create Customer Invoice of Membership for partners."""
        invoice_vals_list = []
        addr = member.address_get(["invoice"])
        if not addr.get("invoice", False):
            raise UserError(_("Partner doesn't have an address to make the invoice."))

        invoice_vals_list.append(
            {
                "move_type": "out_invoice",
                "partner_id": member.id,
                "invoice_line_ids": [
                    (
                        0,
                        None,
                        {
                            "product_id": membership_plan.id,
                            "quantity": 1,
                            "price_unit": membership_fees,
                        },
                    )
                ],
            }
        )

        return self.env["account.move"].create(invoice_vals_list)

    @api.depends("invoice_ids")
    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = self.env["account.move"].search_count(
                [("partner_id", "=", rec.member_id.id)]
            )

    def view_invoice_list(self):
        list_view_ref = self.env.ref("account.view_move_tree", False)
        form_view_ref = self.env.ref("account.view_move_form", False)
        search_view_ref = self.env.ref("account.view_account_invoice_filter", False)

        return {
            "domain": [("partner_id", "=", self.member_id.id)],
            "name": "Membership Invoices",
            "res_model": "account.move",
            "type": "ir.actions.act_window",
            "views": [(list_view_ref.id, "list"), (form_view_ref.id, "form")],
            "search_view_id": search_view_ref and [search_view_ref.id],
            "context": "{'create': False}",
        }

    ###########  PROPER FUNCTIONALITY ###########
    def membership_expire(self):
        today = date.today()
        template = self.env.ref("gym_management_system.gym_membership_expire_email_template")
        records = self.env["gym.membership"].search([("membership_date_to","=",today)])
        for record in records:
            record.state = "expire"
            template.send_mail(record.id)

    
    ###########  FOR TESTING EMAIL ###########
    # def membership_expire(self):
    #     today = date.today()
    #     template = self.env.ref("gym_management_system.gym_membership_expire_email_template")
    #     records = self.env["gym.membership"].search([("membership_date_from","=",today)])
    #     for record in records:
    #         record.state = "expire"
    #         template.send_mail(record.id)


    def create(self, vals):
        existing_member = self.env["gym.membership"].search(
            [("member_id", "=", vals.get("member_id"))], limit=1
        )
        if existing_member:
            raise ValidationError("This member is already registered in the gym.")

        if vals.get("reference", "New") == "New":
            vals["reference"] = (
                self.env["ir.sequence"].next_by_code("gym.membership") or "New"
            )
        self.member_id.membership_id = self.id
        return super(GymMembership, self).create(vals)


    def write(self, vals):
        if self.state == "paid":
            self.trainer_id.assigned_member_ids = [(4, self.member_id.id)]
        return super(GymMembership, self).write(vals)


    def unlink(self):
        for rec in self:
            if rec.state not in ("cancel", "draft"):
                raise ValidationError(
                    "Only memberships in draft or cancelled state can be deleted"
                )
            trainer = self.env["hr.employee"].search([("id", "=", rec.trainer_id.id)])
            if rec.member_id.id in trainer.assigned_member_ids.ids:
                trainer.write({"assigned_member_ids": [(3, rec.member_id.id)]})
        return super(GymMembership, self).unlink()


    
