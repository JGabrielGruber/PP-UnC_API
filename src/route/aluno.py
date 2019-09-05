import	hug

from	library.veryx	import auth
from	controller		import aluno as controllerAluno
from	model			import aluno as modelAluno

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	response
):
	return controllerAluno.getAlunos(response)

@hug.get('/{aluno_id}', requires=auth.basicAccess('usuario'))
def get_byId(
	aluno_id: hug.types.text,
	response
):
	return controllerAluno.getAlunoById(response, aluno_id)

@hug.post('/', requires=auth.basicAccess('usuario'))
def post_data(
	aluno: modelAluno.AlunoType(),
	response
):
	return controllerAluno.newAluno(response, aluno)

@hug.put('/{aluno_id}', requires=auth.basicAccess('usuario'))
def put_data(
	aluno_id: hug.types.text,
	aluno: modelAluno.AlunoType(),
	response
):
	return controllerAluno.updateAluno(response, aluno_id, aluno)

@hug.delete('/{aluno_id}', requires=auth.basicAccess('usuario'))
def delete_data(
	aluno_id: hug.types.text,
	response
):
	return controllerAluno.deleteAlunoById(response, aluno_id)
