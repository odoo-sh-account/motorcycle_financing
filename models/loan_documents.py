from odoo import models, fields, api

class LoanApplicationTag(models.Model):
    _name = 'loan.application.tag'
    _description = 'Loan Application Tag'

    name = fields.Char(string='Name', required=True)
    color = fields.Integer(string='Color')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Tag name must be unique!')
    ]


class LoanApplicationDocumentType(models.Model):
    _name = 'loan.application.document.type'
    _description = 'Loan Application Document Type'

    name = fields.Char(string='Name', required=True)
    active = fields.Boolean(default=True)
    document_number = fields.Integer(string='Required Document Number', required=True, default=1)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Document type name must be unique!')
    ]


class LoanApplicationDocument(models.Model):
    _name = 'loan.application.document'
    _description = 'Loan Application Document'

    name = fields.Char(string='Name', required=True)
    application_id = fields.Many2one('loan.application', string='Loan Application', required=True)
    attachment = fields.Binary(string='File', required=True)
    type_id = fields.Many2one('loan.application.document.type', string='Document Type', required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status', default='new', required=True)
