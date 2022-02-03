from datetime import date, datetime
from odoo import api,fields,models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError

class property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"

    price = fields.Float()
    status = fields.Selection(selection=[("accepted","Accepted"),("refused","Refused")],copy=False)
    validity=fields.Integer(string="Validity(Days)",default=7)

    property_id = fields.Many2one ('estate.property')
    partner_id = fields.Many2one ('res.partner')
  
    date_deadline=fields.Date(string="Deadline",compute="_compute_deadline", inverse="_compute_inverse_deadline")

    _sql_constraints = [
        ('check_price', 'check(price>0)', "Offer price must be strictly Positive."),
    ]

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date+relativedelta(days=(record.validity))
            else:
                record.date_deadline = datetime.now()+relativedelta(days=(record.validity))

    def _compute_inverse_deadline(self):
        for record in self:
            if record.create_date:
                diff = datetime.strptime(record.date_deadline.strftime('%Y-%m-%d'), '%Y-%m-%d') - record.create_date
                record.validity = diff.days + 1
            else:
                record.validity = datetime.strptime(record.date_deadline.strftime('%Y-%m-%d'), '%Y-%m-%d') - datetime.todays

    def accepted(self):
        for record in self:
            if record.status == 'accepted':
                return True

    def refused(self):
        for record in self:
            if record.status == 'refused':
                return True
           