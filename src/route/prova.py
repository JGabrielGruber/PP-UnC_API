import	hug

from	library.veryx	import auth
from	controller		import prova as controllerProva
from	model			import prova as modelProva
from	route			import realizacao

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerProva.getProvas(response, usuario_id, materia_id, turma_id)

@hug.get('/{prova_id}', requires=auth.basicAccess('usuario'))
def get_byId(
	prova_id: hug.types.number,
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerProva.getProvaById(response, usuario_id, materia_id, turma_id, prova_id)

@hug.post('/', requires=auth.basicAccess('usuario'))
def post_data(
	prova: modelProva.ProvaType(),
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerProva.newProva(response, usuario_id, materia_id, turma_id, prova)

@hug.put('/{prova_id}', requires=auth.basicAccess('usuario'))
def put_data(
	prova_id: hug.types.number,
	turma_id,
	materia_id,
	usuario_id,
	prova: modelProva.ProvaType(),
	response
):
	return controllerProva.updateProva(response, usuario_id, materia_id, turma_id, prova_id, prova)

@hug.delete('/{prova_id}', requires=auth.basicAccess('usuario'))
def delete_data(
	prova_id: hug.types.number,
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerProva.deleteProvaById(response, usuario_id, materia_id, turma_id, prova_id)

@hug.extend_api('/{prova_id}/realizacoes')
def realizacao_api():
	return [realizacao]
