from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class LoanApplication(models.Model):
    _name = 'loan.application'
    _description = 'Loan Application'

    name = fields.Char(
        string='Application Number',
        required=True
    )
    
    # Related Fields from Sale Order
    sale_order_id = fields.Many2one(
        comodel_name='sale.order', 
        string='Sale Order',
        required=True
    )
    sale_order_total = fields.Monetary(
        string='Sale Order Total', 
        related='sale_order_id.amount_total', 
        readonly=True
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency', 
        related='sale_order_id.currency_id', 
        readonly=True
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner', 
        string='Customer', 
        related='sale_order_id.partner_id', 
        readonly=True
    )
    user_id = fields.Many2one(
        comodel_name='res.users', 
        string='Salesperson', 
        related='sale_order_id.user_id', 
        readonly=True
    )

    # Computed Fields
    loan_amount = fields.Monetary(
        string='Loan Amount',
        currency_field='currency_id',
        compute='_compute_loan_amount',
        store=True,
        readonly=False
    )
    down_payment = fields.Monetary(
        string='Down Payment',
        currency_field='currency_id',
        compute='_compute_loan_amount',
        store=True,
        readonly=False
    )
    
    # Other existing fields
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
    date_sent = fields.Date(
        string='Sent Date', 
        readonly=True, 
        copy=False
    )
    interest_rate = fields.Float(
        string='Interest Rate (%)',
        digits=(5, 2),
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

    # Existing relational fields
    document_ids = fields.One2many(
        'loan.application.document',
        'application_id',
        string='Documents'
    )
    tag_ids = fields.Many2many(
        'loan.application.tag',
        string='Tags'
    )
    product_template_id = fields.Many2one(
        'product.template',
        string='Product'
    )

    # Document Count Fields
    document_count = fields.Integer(
        string='Total Documents', 
        compute='_compute_document_counts',
        store=True
    )
    document_count_approved = fields.Integer(
        string='Approved Documents', 
        compute='_compute_document_counts',
        store=True
    )

    # SQL Constraint for non-negative down payment and loan amount
    _sql_constraints = [
        ('non_negative_down_payment', 'CHECK(down_payment >= 0)', 'Down payment cannot be negative.'),
        ('non_negative_loan_amount', 'CHECK(loan_amount >= 0)', 'Loan amount cannot be negative.')
    ]

    @api.depends('sale_order_total', 'loan_amount', 'down_payment')
    def _compute_loan_amount(self):
        for record in self:
            # If loan_amount is not set, calculate it from sale order total and down payment
            if not record.loan_amount:
                record.loan_amount = record.sale_order_total - record.down_payment
            # If loan_amount is set, calculate down_payment
            elif record.loan_amount:
                record.down_payment = record.sale_order_total - record.loan_amount

    @api.constrains('down_payment')
    def _check_down_payment(self):
        """
        Validate that down payment does not exceed sale order total
        """
        for record in self:
            if record.down_payment > record.sale_order_total:
                raise ValidationError("Down payment cannot exceed the sale order total.")

    @api.depends('document_ids', 'document_ids.state')
    def _compute_document_counts(self):
        for record in self:
            record.document_count = len(record.document_ids)
            record.document_count_approved = len(record.document_ids.filtered(lambda d: d.state == 'approved'))

    # Existing action methods
    def action_send(self):
        """
        Send loan application for approval
        - Requires all documents to be approved
        - Changes state to 'sent'
        - Sets sent date
        """
        for record in self:
            # Check if all documents are approved
            unapproved_docs = record.document_ids.filtered(lambda d: d.state != 'approved')
            if unapproved_docs:
                raise UserError("All documents must be approved before sending the application.")
            
            # Set state and date
            record.write({
                'state': 'sent',
                'date_sent': fields.Date.today()
            })

    def action_review(self):
        self.write({'state': 'review'})

    def action_approve(self):
        """
        Approve loan application
        - Changes state to 'approved'
        - Sets approval date
        """
        for record in self:
            record.write({
                'state': 'approved',
                'date_approval': fields.Date.today()
            })

    def action_reject(self, rejection_reason=False):
        """
        Reject loan application
        - Changes state to 'rejected'
        - Sets rejection date
        - Optionally sets rejection reason
        """
        for record in self:
            record.write({
                'state': 'rejected',
                'date_rejection': fields.Date.today(),
                'rejection_reason': rejection_reason or "No specific reason provided."
            })

    def action_sign(self):
        self.write({
            'state': 'signed',
            'date_signed': fields.Datetime.now(),
        })

    def action_cancel(self):
        self.write({'state': 'cancel'})
