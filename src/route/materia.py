import	hug

from	library.veryx	import auth
from	controller		import materia as controllerMateria
from	model			import materia as modelMateria
from	route			import turma, provaBase

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	response
):
	return controllerMateria.getMaterias(response)

@hug.get('/{id}', requires=auth.basicAccess('usuario'))
def get_byId(
	id: hug.types.number,
	response
):
	return controllerMateria.getMateriaById(response, id)

@hug.post('/', requires=auth.basicAccess('admin'))
def post_data(
	materia: modelMateria.MateriaType(),
	response
):
	return controllerMateria.newMateria(response, materia)

@hug.put('/{id}', requires=auth.basicAccess('usuario'))
def put_data(
	id: hug.types.number,
	materia: modelMateria.MateriaType(),
	response
):
	return controllerMateria.updateMateria(response, id, materia)

@hug.delete('/{id}', requires=auth.basicAccess('usuario'))
def delete_data(
	id: hug.types.number,
	response
):
	return controllerMateria.deleteMateriaById(response, id)

@hug.extend_api('/{id}/turmas')
def turma_api():
	return [turma]

@hug.extend_api('/{id}/provas')
def prova_api():
	return [provaBase]
