from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    is_gym_trainer = fields.Boolean(string="Is a Trainer?", default=False)
    assigned_member_ids = fields.Many2many("res.partner", "assigned_trainer_id", string="Assigned Members")
    assigned_member_count = fields.Integer(compute="compute_assigned_member_count")

    @api.depends("assigned_member_ids")
    def compute_assigned_member_count(self):
        self.assigned_member_count = len(self.assigned_member_ids)

    def assigned_members(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": "Assigned Members",
            "res_model": "gym.membership",
            "view_mode": "list",
            "domain": [("member_id", "in", self.assigned_member_ids.ids)],
            "context": "{'create': False}",
        }

    def change_is_gym_trainer(self):
        for rec in self:
            if rec.is_gym_trainer == True:
                rec.is_gym_trainer = False

    
