import	hug

from	library.veryx	import auth
from	controller		import turma as controllerTurma
from	model			import turma as modelTurma
from	route			import aluno, prova

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	materia_id,
	usuario_id,
	response
):
	return controllerTurma.getTurmas(response, usuario_id, materia_id)

@hug.get('/{turma_id}', requires=auth.basicAccess('usuario'))
def get_byId(
	turma_id: hug.types.number,
	materia_id,
	usuario_id,
	response
):
	return controllerTurma.getTurmaById(response, usuario_id, materia_id, turma_id)

@hug.post('/', requires=auth.basicAccess('usuario'))
def post_data(
	turma: modelTurma.TurmaType(),
	materia_id,
	usuario_id,
	response
):
	return controllerTurma.newTurma(response, usuario_id, materia_id, turma)

@hug.put('/{turma_id}', requires=auth.basicAccess('usuario'))
def put_data(
	turma_id: hug.types.number,
	materia_id,
	usuario_id,
	turma: modelTurma.TurmaType(),
	response
):
	return controllerTurma.updateTurma(response, usuario_id, materia_id, turma_id, turma)

@hug.delete('/{turma_id}', requires=auth.basicAccess('usuario'))
def delete_data(
	turma_id: hug.types.number,
	materia_id,
	usuario_id,
	response
):
	return controllerTurma.deleteTurmaById(response, usuario_id, materia_id, turma_id)

@hug.extend_api('/{turma_id}/provas')
def prova_api():
	return [prova]

@hug.extend_api('/{turma_id}/alunos')
def aluno_api():
	return [aluno]
