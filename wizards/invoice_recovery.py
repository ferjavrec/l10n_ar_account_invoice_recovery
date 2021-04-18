from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DF

class AccountInvoiceRecovery(models.TransientModel):
	_name = 'account.invoice.recovery'
	_description = 'Account Invoice Recovery'
	
	journal_id = fields.Many2one('account.journal', string='Diario',
		required=True, domain="[('type', '=', 'sale'), ('company_id', '=', company_id)]")
	documento_id = fields.Many2one('account.document.type', string='Tipo Comprobante',
		domain="[('localization', '=', 'argentina')]", required=True)
	number = fields.Integer('Numero de Comprobante', required=True)
	company_id = fields.Many2one('res.company', string='Company', change_default=True,
		required=True, readonly=True,
		default=lambda self: self.env['res.company']._company_default_get('account.invoice'))
	


	@api.multi
	def confirm(self):
		ws = self.company_id.get_connection(self.journal_id.afip_ws).connect()
		retorno = ws.CompConsultar(self.documento_id.code, self.journal_id.point_of_sale_number, self.number)
		if retorno == '':
			raise UserError(_('Los datos ingresados no corresponden a una factura autorizada por AFIP'))
			return

		message = 'FechaCbte = ' + ws.FechaCbte + '\n'
		message += 'CbteNro = ' + str(ws.CbteNro) + '\n'
		message += 'PuntoVenta = ' + str(ws.PuntoVenta) + '\n'
		message += 'ImpNETO =' + str(ws.ImpNeto) + '\n'
		message += 'ImpOpEx =' + str(ws.ImpOpEx) + '\n'
		message += 'ImpIVA =' + str(ws.ImpIVA) + '\n'
		message += 'ImpTrib =' + str(ws.ImpTrib) + '\n'
		message += 'ImpTotal =' + str(ws.ImpTotal) + '\n'
		message += 'IVA =' + str(ws.factura['iva']) + '\n'
		message += 'TRIBUTOS =' + str(ws.factura['tributos']) + '\n'
		message += 'CAE = ' + str(ws.CAE) + '\n'
		message += 'Vencimiento = ' + str(ws.Vencimiento) + '\n'

		if ws.AnalizarXml('XmlResponse'):
			if self.journal_id.afip_ws == 'wsfex':
				cuit_cliente = ws.ObtenerTagXml('Cuit_pais_cliente')
				emision_tipo = ws.ObtenerTagXml('Cbte_tipo')
			else:
				cuit_cliente = ws.ObtenerTagXml('DocNro')
				emision_tipo = ws.ObtenerTagXml('CbteTipo')
				
		message += 'CUIT CLIENTE = %s\n' % cuit_cliente
		message += 'Tipo comprobante = %s\n' % emision_tipo

		return self.msgbox(message)
	
	def msgbox (self, message):
	   return {
			'name': 'Message',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'msg.box',
			'target': 'new',
			'context': {'default_message': "{}". format (message)}
	}
