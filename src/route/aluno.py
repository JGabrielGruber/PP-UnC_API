import	hug

from	library.veryx	import auth
from	controller		import aluno as controllerAluno
from	model			import aluno as modelAluno

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	response
):
	return controllerAluno.getAlunos(response)

@hug.get('/{id}', requires=auth.basicAccess('usuario'))
def get_byId(
	id: hug.types.number,
	response
):
	return controllerAluno.getAlunoById(response, id)

@hug.post('/', requires=auth.basicAccess('usuario'))
def post_data(
	aluno: modelAluno.AlunoType(),
	response
):
	return controllerAluno.newAluno(response, aluno)

@hug.put('/{id}', requires=auth.basicAccess('usuario'))
def put_data(
	id: hug.types.number,
	aluno: modelAluno.AlunoType(),
	response
):
	return controllerAluno.updateAluno(response, id, aluno)

@hug.delete('/{id}', requires=auth.basicAccess('usuario'))
def delete_data(
	id: hug.types.number,
	response
):
	return controllerAluno.deleteAlunoById(response, id)
