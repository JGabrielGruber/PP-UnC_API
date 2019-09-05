import	hug

from	library.veryx	import auth
from	controller		import provaBase as controllerProvaBase
from	model			import provaBase as modelProvaBase

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	materia_id,
	usuario_id,
	response
):
	return controllerProvaBase.getProvaBases(response, usuario_id, materia_id)

@hug.get('/{provaBase_id}', requires=auth.basicAccess('usuario'))
def get_byId(
	provaBase_id: hug.types.text,
	materia_id,
	usuario_id,
	response
):
	return controllerProvaBase.getProvaBaseById(response, usuario_id, materia_id, provaBase_id)

@hug.post('/', requires=auth.basicAccess('usuario'))
def post_data(
	provaBase: modelProvaBase.ProvaBaseType(),
	materia_id,
	usuario_id,
	response
):
	return controllerProvaBase.newProvaBase(response, usuario_id, materia_id, provaBase)

@hug.put('/{provaBase_id}', requires=auth.basicAccess('usuario'))
def put_data(
	provaBase_id: hug.types.text,
	materia_id,
	usuario_id,
	provaBase: modelProvaBase.ProvaBaseType(),
	response
):
	return controllerProvaBase.updateProvaBase(response, usuario_id, materia_id, provaBase_id, provaBase)

@hug.delete('/{provaBase_id}', requires=auth.basicAccess('usuario'))
def delete_data(
	provaBase_id: hug.types.text,
	materia_id,
	usuario_id,
	response
):
	return controllerProvaBase.deleteProvaBaseById(response, usuario_id, materia_id, provaBase_id)
