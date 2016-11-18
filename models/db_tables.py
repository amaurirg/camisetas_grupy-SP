CG = db.define_table('camisetas',
	Field('horario', notnull=True, label='Indicação de data e hora'),
	Field('nome', notnull=True, label='Nome completo'),
	Field('tipo', notnull=True, label='Tipo de camiseta'),
	Field('tamanho', notnull=True, label='Tamanho'),
	Field('valor', notnull=True, label='Valor'),
	Field('pago', label='Pago', widget=SQLFORM.widgets.radio.widget, 
           requires = IS_IN_SET(['NÃO', 'SIM']), default='NÃO')
	)
