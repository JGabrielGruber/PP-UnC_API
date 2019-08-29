import	hug

from	library.veryx	import auth
from	controller		import prova as controllerProva
from	model			import prova as modelProva
from	route			import realizacao

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	response
):
	return controllerProva.getProvas(response)

@hug.get('/{id}', requires=auth.basicAccess('usuario'))
def get_byId(
	id: hug.types.number,
	response
):
	return controllerProva.getProvaById(response, id)

@hug.post('/', requires=auth.basicAccess('usuario'))
def post_data(
	prova: modelProva.ProvaType(),
	response
):
	return controllerProva.newProva(response, prova)

@hug.put('/{id}', requires=auth.basicAccess('usuario'))
def put_data(
	id: hug.types.number,
	prova: modelProva.ProvaType(),
	response
):
	return controllerProva.updateProva(response, id, prova)

@hug.delete('/{id}', requires=auth.basicAccess('usuario'))
def delete_data(
	id: hug.types.number,
	response
):
	return controllerProva.deleteProvaById(response, id)

@hug.extend_api('/{id}/realizacoes')
def realizacao_api():
	return [realizacao]
