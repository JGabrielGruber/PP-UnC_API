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

@hug.get('/{usuario_id}', requires=auth.basicAccess('usuario'))
def get_byId(
	usuario_id: hug.types.number,
	response
):
	return controllerUsuario.getUsuarioById(response, usuario_id)

@hug.post('/', requires=auth.basicAccess('admin'))
def post_data(
	usuario: modelUsuario.UsuarioType(),
	response
):
	return controllerUsuario.newUsuario(response, usuario)

@hug.put('/{usuario_id}', requires=auth.basicAccess('usuario'))
def put_data(
	usuario_id: hug.types.number,
	usuario: modelUsuario.UsuarioType(),
	response
):
	return controllerUsuario.updateUsuario(response, usuario_id, usuario)

@hug.delete('/{usuario_id}', requires=auth.basicAccess('usuario'))
def delete_data(
	usuario_id: hug.types.number,
	response
):
	return controllerUsuario.deleteUsuarioById(response, usuario_id)

@hug.extend_api('/{usuario_id}/materias')
def materia_api():
	return [materia]
