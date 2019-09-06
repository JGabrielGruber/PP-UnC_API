import	hug

from	library.veryx	import auth
from	controller		import aluno as controllerAluno
from	model			import aluno as modelAluno

@hug.get('/', requires=auth.ownerAccess())
def get_index(
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerAluno.getAlunos(response, usuario_id, materia_id, turma_id)

@hug.get('/{aluno_id}', requires=auth.ownerAccess())
def get_byId(
	aluno_id: hug.types.text,
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerAluno.getAlunoById(response, usuario_id, materia_id, turma_id, aluno_id)

@hug.post('/', requires=auth.ownerAccess())
def post_data(
	aluno: modelAluno.AlunoType(),
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerAluno.newAluno(response, usuario_id, materia_id, turma_id, aluno)

@hug.put('/{aluno_id}', requires=auth.ownerAccess())
def put_data(
	aluno_id: hug.types.text,
	turma_id,
	materia_id,
	usuario_id,
	aluno: modelAluno.AlunoType(),
	response
):
	return controllerAluno.updateAluno(response, usuario_id, materia_id, turma_id, aluno_id, aluno)

@hug.delete('/{aluno_id}', requires=auth.ownerAccess())
def delete_data(
	aluno_id: hug.types.text,
	turma_id,
	materia_id,
	usuario_id,
	response
):
	return controllerAluno.deleteAlunoById(response, usuario_id, materia_id, turma_id, aluno_id)
