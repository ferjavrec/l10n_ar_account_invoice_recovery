from odoo import fields, models

class MsgBox(models.Model):
	_name = 'msg.box'
	_description = 'Message Box'

	message = fields.Text(string = "Mensaje")