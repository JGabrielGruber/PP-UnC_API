import	hug

from	library.veryx	import auth
from	controller		import materia as controllerMateria
from	model			import materia as modelMateria
from	route			import turma, provaBase

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	usuario_id,
	response
):
	return controllerMateria.getMaterias(response, usuario_id)

@hug.get('/{materia_id}', requires=auth.basicAccess('usuario'))
def get_byId(
	materia_id: hug.types.number,
	usuario_id,
	response
):
	return controllerMateria.getMateriaById(response, usuario_id, materia_id)

@hug.post('/', requires=auth.basicAccess('admin'))
def post_data(
	materia: modelMateria.MateriaType(),
	usuario_id,
	response
):
	return controllerMateria.newMateria(response, usuario_id, materia)

@hug.put('/{materia_id}', requires=auth.basicAccess('usuario'))
def put_data(
	materia_id: hug.types.number,
	usuario_id,
	materia: modelMateria.MateriaType(),
	response
):
	return controllerMateria.updateMateria(response, usuario_id, materia_id, materia)

@hug.delete('/{materia_id}', requires=auth.basicAccess('usuario'))
def delete_data(
	materia_id: hug.types.number,
	usuario_id,
	response
):
	return controllerMateria.deleteMateriaById(response, usuario_id, materia_id)

@hug.extend_api('/{materia_id}/turmas')
def turma_api():
	return [turma]

@hug.extend_api('/{materia_id}/provas')
def prova_api():
	return [provaBase]
