import	hug

from	library.veryx	import auth
from	controller		import realizacao as controllerRealizacao
from	model			import realizacao as modelRealizacao

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	response
):
	return controllerRealizacao.getRealizacaos(response)

@hug.get('/{id}', requires=auth.basicAccess('usuario'))
def get_byId(
	id: hug.types.number,
	response
):
	return controllerRealizacao.getRealizacaoById(response, id)

@hug.post('/', requires=auth.basicAccess('usuario'))
def post_data(
	realizacao: modelRealizacao.RealizacaoType(),
	response
):
	return controllerRealizacao.newRealizacao(response, realizacao)

@hug.put('/{id}', requires=auth.basicAccess('usuario'))
def put_data(
	id: hug.types.number,
	realizacao: modelRealizacao.RealizacaoType(),
	response
):
	return controllerRealizacao.updateRealizacao(response, id, realizacao)

@hug.delete('/{id}', requires=auth.basicAccess('usuario'))
def delete_data(
	id: hug.types.number,
	response
):
	return controllerRealizacao.deleteRealizacaoById(response, id)
