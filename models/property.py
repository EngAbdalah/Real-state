from tokenize import group

from odoo import models ,fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class Property(models.Model):
    _name='property'
    _description='Property'#is display name for user
    _inherit=['mail.thread','mail.activity.mixin']
    ref=fields.Char( default='new',readonly=1)
    name=fields.Char(required=1 , default='new', size=12)
    description=fields.Text(tracking=1)
    postcode=fields.Char(required=1 , size=4)
    date_availability=fields.Date(tracking=1)
    expected_selling_date=fields.Date(tracking=1)
    is_late=fields.Boolean()
    expected_price=fields.Float()         #digit=(0,5)
    diff=fields.Float(compute='_compute_diff', store=1, readonly=0 )
    selling_price=fields.Float()
    bedrooms=fields.Integer()
    living_area=fields.Integer()
    facades=fields.Integer()
    garage=fields.Boolean(groups="my_first_app.property_manager_group")
    garden=fields.Boolean()
    garden_area=fields.Integer()
    garden_orantation=fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West'),


    ],default='north')
    # create_time=fields.Datetime(fields.Datetime.now())
    # next_time=fields.Datetime(compute='_compute_next_time')


    owner_id = fields.Many2one('owner')
    tag_ids= fields.Many2many('tag')
    state = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('sold','Sold'),
        ('closed','Closed'),
    ],default ='draft')
    owner_address=fields.Char(related ='owner_id.address',readonly=0)
    owner_phone=fields.Char(related ='owner_id.phone',readonly=0)

    # add validation on 3td teir (database)
    _sql_constraints=[
        ('unique_name', 'unique("name")', 'this name is exist')  #ask eng. mohamed  why is not name become uniqe
        # ('expres name', this function take filed name'unique("name")', the massege for user 'this name is exist')

    ]
    line_ids=fields.One2many('property.line','property_id')
    active=fields.Boolean(default=1)

    # @api.depends('create_time')
    # def _compute_next_time(self):
    #     for rec in self:
    #         if rec.create_time:
    #             rec.next_time = rec.create_time + timedelta(hours=6)
    #         else:
    #             rec.next_time =False

    @api.depends('expected_price','selling_price','owner_id.phone')  # this is depends   method call when any update hapend in this fields
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price


        # this onchange method that take fields as argument
    @api.onchange('expected_price')  #field must be simple field this main that field is in tree view and form view
    def _onchange_expected_price(self):
        for rec in self:
            print("_onchange_expected_price")
            return {
                'warning':{'title':'warning','message':'negative value', 'type':'noification' }
            }

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):

        for rec in self :

            if rec.bedrooms == 0:
                raise ValidationError('please enter the valid number !')

    def action_draft(self):
        for rec in self :
            rec.create_history_record(rec.state,'draft')
            print("inside draft action")
            rec.state='draft'
            # rec.write({'state':'draft'})

    def action_pending(self):
        for rec in self :
            rec.create_history_record(rec.state,'pending')
            rec.state='pending'

    def actino_sold(self):
        for rec in self:
            rec.create_history_record(rec.state, 'sold')
            rec.state='sold'

    def actino_closed(self):
        for rec in self:
            rec.create_history_record(rec.state, 'closed')
            rec.state='closed'



    # crud___operation
    @api.model_create_multi
    def create(self,vals):
        res=super(Property,self).create(vals)     #super function >>> i must learn about it
        # logic write your on code in this section
        print("over write on create operation")
        return res

    #reade function

    @api.model
    def _search(self, domain,offset=0, limit=None, order=None, access_rights_uid=None):
        res = super(Property, self)._search(domain,offset=0 ,limit=None ,order=None,access_rights_uid=None)  # super function >>> i must learn about it
        # logic write your on code in this section
        print("over write on read operation")
        return res

    #update operation >>> write
    def write(self,vals):
        res = super(Property, self).write(vals)  # super function >>> i must learn about it
        # logic write your on code in this section
        print("over write on write operation")
        return res

    # delete  operation >>> unlink()
    def unlink(self):
        res=super(Property,self).unlink()
        print("over write on delete operation")
        return res

    def check_expected_selling_date(self):
        property_ids=self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today() :
                rec.is_late=True

        print("inside expected_selling_date")


    def action(self):
        print(self.env.user)
        print(self.env.user.login)
        print(self.env.user.id)
        print(self.env.company.id)
        print(self.env.company.name)
        print(self.env.company.street)
        print(self.env.context)
        print(self.env.cr)
        print(self.env['owner'].create({'name':'name_one','phone':'01153110580'}))
        print("33333env")

        print(self.env['owner'].search([]))
        print("44444env")

        print(self.env['property'].search(['|',('name','=','p1'),('postcode','=','5555')]))

    @api.model
    def create(self, vals):
        res = super(Property, self).create(vals)  # super function >>> i must learn about it
        # logic write your on code in this section
        if res.ref=='new':
            res.ref=self.env['ir.sequence'].next_by_code('property_seq')
        print("over write on create operation")
        print("**50"*50)
        return res


    def create_history_record(self,old_state,new_state,reason=""):
        for rec in self :
            rec.env['property.history'].create({
                'user_id':rec.env.uid,
                'property_id':rec.id,
                'old_state':old_state,
                'new_state': new_state,
                'reason':reason or '',
                'line_ids':[(0,0,{'description':line.description, 'area':line.area}) for line in rec.line_ids],
            })
        print("**110"*50)


    def actino_open_change_state_wizard(self):
        action=self.env['ir.actions.actions']._for_xml_id('my_first_app.change_state_wizard_action')

        action['context']={'default_property_id':self.id}
        return action


    def property_xlsx_report(self):
        print("in property_xlsx_report")
        return {
            'type':'ir.actions.act_url',
            'url':f'/property/excel/report/{self.env.context.get("active_ids")}',
            'target':'new'
        }











class PropertyLine(models.Model):


    _name='property.line'
    area=fields.Float()
    description=fields.Char()
    property_id=fields.Many2one('property')





