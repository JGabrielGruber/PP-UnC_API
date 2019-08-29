import	hug

from	library.veryx	import auth
from	controller		import turma as controllerTurma
from	model			import turma as modelTurma
from	route			import aluno, prova

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	response
):
	return controllerTurma.getTurmas(response)

@hug.get('/{id}', requires=auth.basicAccess('usuario'))
def get_byId(
	id: hug.types.number,
	response
):
	return controllerTurma.getTurmaById(response, id)

@hug.post('/', requires=auth.basicAccess('usuario'))
def post_data(
	turma: modelTurma.TurmaType(),
	response
):
	return controllerTurma.newTurma(response, turma)

@hug.put('/{id}', requires=auth.basicAccess('usuario'))
def put_data(
	id: hug.types.number,
	turma: modelTurma.TurmaType(),
	response
):
	return controllerTurma.updateTurma(response, id, turma)

@hug.delete('/{id}', requires=auth.basicAccess('usuario'))
def delete_data(
	id: hug.types.number,
	response
):
	return controllerTurma.deleteTurmaById(response, id)

@hug.extend_api('/{id}/provas')
def prova_api():
	return [prova]

@hug.extend_api('/{id}/alunos')
def aluno_api():
	return [aluno]
