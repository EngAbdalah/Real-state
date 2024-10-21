from odoo import models,fields



class SaleOrder(models.Model):
    _inherit ='sale.order'
    property_id=fields.Many2one('property')
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()  # super function >>> i must learn about it
        # logic write your on code in this section
        print("in action_confirm method")
        return res



