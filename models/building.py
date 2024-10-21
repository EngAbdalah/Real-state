from email.policy import default

from odoo import models ,fields, api
# from odoo.exceptions import ValidationError



class Building(models.Model):
    _name='building'
    _description='Property is display name for user'
    _inherit=['mail.thread','mail.activity.mixin']
    # _rec_name='code'
    name=fields.Char()
    no=fields.Integer()
    code=fields.Char()
    description=fields.Text()
    active=fields.Boolean(default=1)



