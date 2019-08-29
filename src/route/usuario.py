import	hug

from	library.veryx	import auth
from	controller		import usuario as controllerUsuario
from	model			import usuario as modelUsuario
from	route			import materia

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	response
):
	return controllerUsuario.getUsuarios(response)

@hug.get('/{id}', requires=auth.basicAccess('usuario'))
def get_byId(
	id: hug.types.number,
	response
):
	return controllerUsuario.getUsuarioById(response, id)

@hug.post('/', requires=auth.basicAccess('admin'))
def post_data(
	usuario: modelUsuario.UsuarioType(),
	response
):
	return controllerUsuario.newUsuario(response, usuario)

@hug.put('/{id}', requires=auth.basicAccess('usuario'))
def put_data(
	id: hug.types.number,
	usuario: modelUsuario.UsuarioType(),
	response
):
	return controllerUsuario.updateUsuario(response, id, usuario)

@hug.delete('/{id}', requires=auth.basicAccess('usuario'))
def delete_data(
	id: hug.types.number,
	response
):
	return controllerUsuario.deleteUsuarioById(response, id)

@hug.extend_api('/{id}/materias')
def materia_api():
	return [materia]
