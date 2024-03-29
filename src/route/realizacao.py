import	hug

from	library.veryx	import auth
from	controller		import realizacao as controllerRealizacao
from	model			import realizacao as modelRealizacao

@hug.get('/', requires=auth.ownerAccess())
def get_index(
	prova_id,
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerRealizacao.getRealizacaos(response, usuario_id, materia_id, turma_id, prova_id)

@hug.get('/{realizacao_id}', requires=auth.advancedAccess())
def get_byId(
	realizacao_id: hug.types.text,
	prova_id,
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerRealizacao.getRealizacaoById(response, usuario_id, materia_id, turma_id, prova_id, realizacao_id)

@hug.post('/', requires=auth.ownerAccess())
def post_data(
	realizacao: modelRealizacao.RealizacoesType(),
	prova_id,
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerRealizacao.newRealizacao(response, usuario_id, materia_id, turma_id, prova_id, realizacao)

@hug.put('/{realizacao_id}', requires=auth.advancedAccess())
def put_data(
	realizacao_id: hug.types.text,
	prova_id,
	turma_id,
	materia_id,
	usuario_id,
	realizacao: modelRealizacao.RealizacaoType(),
	response
):
	return controllerRealizacao.updateRealizacao(response, usuario_id, materia_id, turma_id, prova_id, realizacao_id, realizacao)

@hug.put('/{realizacao_id}/iniciar', requires=auth.advancedAccess())
def put_data(
	realizacao_id: hug.types.text,
	prova_id,
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerRealizacao.startRealizacao(response, usuario_id, materia_id, turma_id, prova_id, realizacao_id)

@hug.delete('/{realizacao_id}', requires=auth.ownerAccess())
def delete_data(
	realizacao_id: hug.types.text,
	prova_id,
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerRealizacao.deleteRealizacaoById(response, usuario_id, materia_id, turma_id, prova_id, realizacao_id)
