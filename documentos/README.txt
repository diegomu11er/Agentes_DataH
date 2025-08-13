**noticias_publicadas_ultimos_30d.csv**:

	* Contém as matérias que foram criadas no edit nos últimos 30 dias.
	* Já houve um processamento prévio para extrair editoria e subeditoria.
	* Já houve um processamento prévio para extrair apenas um autor (múltiplos autores podem ter contribuído).

**leitura_ultimos_5d_amostra.csv**:

	* Contém dados do sistema de eventos no site e app ZM (Zen Metrics).
	* Foram incluídos apenas eventos que possuem "idMateria", pois, por exemplo, eventos na capa do site não possuem idMateria.
	* Foram incluídos apenas eventos com idMateria existente no dataset de matérias publicadas nos últimos 30 dias, portanto desconsideramos leituras de matérias antigas.
	* O conjunto original possui mais de 6 milhões de registros, então foi extraída uma amostra aleatória de 10 mil registros.