from odoo import models,fields



class Tag(models.Model):
    _name = 'tag'
    name = fields.Char()
    # phone = fields.Char()
    # address = fields.Char()
    # property_ids = fields.One2many('property','owner_id')

