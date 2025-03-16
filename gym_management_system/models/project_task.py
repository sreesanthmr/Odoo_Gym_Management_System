from odoo import models, fields

class ProjectTask(models.Model):
    _inherit = "project.task"

    member_ids = fields.Many2many(
        "res.partner", string="Assignees", domain=[('is_gym_member', '=', True)]
    )

    is_gym_workout_schedule = fields.Boolean("Is Gym Workout Schedule?", default=False)
    no_of_reps = fields.Char(string="No. of Reps")
