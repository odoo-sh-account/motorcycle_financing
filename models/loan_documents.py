from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LoanApplicationTag(models.Model):
    _name = 'loan.application.tag'
    _description = 'Loan Application Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')

    # SQL Constraint for unique tag names
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Tag name must be unique!')
    ]


class LoanApplicationDocumentType(models.Model):
    _name = 'loan.application.document.type'
    _description = 'Loan Application Document Type'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True)
    document_number = fields.Integer(string='Required Document Number', required=True, default=1)

    # SQL Constraint for unique document type names
    _sql_constraints = [
        ('name_uniq', 'UNIQUE(name)', 'Document type name must be unique!')
    ]


class LoanApplicationDocument(models.Model):
    _name = 'loan.application.document'
    _description = 'Loan Application Document'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    application_id = fields.Many2one('loan.application', string='Loan Application', required=True)
    attachment = fields.Binary(string='File', required=True)
    type_id = fields.Many2one('loan.application.document.type', string='Document Type', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='new', required=True)

    @api.onchange('attachment')
    def _onchange_attachment(self):
        """
        Reset document state to 'new' when attachment is modified
        """
        if self.attachment:
            self.state = 'new'

    def action_approve(self):
        """
        Approve the document
        - Changes state to 'approved'
        - Validates that all other documents are approved
        """
        for record in self:
            # Validate all documents in the application
            other_docs = record.application_id.document_ids
            unapproved_docs = other_docs.filtered(lambda d: d.state != 'approved' and d.id != record.id)
            
            if unapproved_docs:
                raise ValidationError("All documents must be approved before accepting this document.")
            
            record.write({'state': 'approved'})

    def action_reject(self):
        """
        Reject the document
        """
        self.write({'state': 'rejected'})
