from odoo import models, fields, api

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    name = fields.Char(
        string='Application Number',
        required=True
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id.id
    )
    date_application = fields.Date(
        string='Application Date',
        readonly=True,
        copy=False
    )
    date_approval = fields.Date(
        string='Approval Date',
        readonly=True,
        copy=False
    )
    date_rejection = fields.Date(
        string='Rejection Date',
        readonly=True,
        copy=False
    )
    date_signed = fields.Datetime(
        string='Signed On',
        readonly=True,
        copy=False
    )
    down_payment = fields.Monetary(
        string='Down Payment',
        currency_field='currency_id',
        required=True
    )
    interest_rate = fields.Float(
        string='Interest Rate (%)',
        digits=(5, 2),
        required=True
    )
    loan_amount = fields.Monetary(
        string='Loan Amount',
        currency_field='currency_id',
        required=True
    )
    loan_term = fields.Integer(
        string='Term (months)',
        required=True,
        default=36
    )
    rejection_reason = fields.Text(
        string='Rejection Reason',
        copy=False
    )
    notes = fields.Text(
        string='Notes',
        copy=False
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('review', 'Credit Check'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('signed', 'Signed'),
        ('cancel', 'Canceled')
    ], string='Status', default='draft', copy=False, required=True)

    def action_send(self):
        self.write({
            'state': 'sent',
            'date_application': fields.Date.today(),
        })

    def action_review(self):
        self.write({'state': 'review'})

    def action_approve(self):
        self.write({
            'state': 'approved',
            'date_approval': fields.Date.today(),
        })

    def action_reject(self):
        self.write({
            'state': 'rejected',
            'date_rejection': fields.Date.today(),
        })

    def action_sign(self):
        self.write({
            'state': 'signed',
            'date_signed': fields.Datetime.now(),
        })

    def action_cancel(self):
        self.write({'state': 'cancel'})
