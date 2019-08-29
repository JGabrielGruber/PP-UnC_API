import	hug

from	library.veryx	import auth
from	controller		import provaBase as controllerProvaBase
from	model			import provaBase as modelProvaBase

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	response
):
	return controllerProvaBase.getProvaBases(response)

@hug.get('/{id}', requires=auth.basicAccess('usuario'))
def get_byId(
	id: hug.types.number,
	response
):
	return controllerProvaBase.getProvaBaseById(response, id)

@hug.post('/', requires=auth.basicAccess('usuario'))
def post_data(
	provaBase: modelProvaBase.ProvaBaseType(),
	response
):
	return controllerProvaBase.newProvaBase(response, provaBase)

@hug.put('/{id}', requires=auth.basicAccess('usuario'))
def put_data(
	id: hug.types.number,
	provaBase: modelProvaBase.ProvaBaseType(),
	response
):
	return controllerProvaBase.updateProvaBase(response, id, provaBase)

@hug.delete('/{id}', requires=auth.basicAccess('usuario'))
def delete_data(
	id: hug.types.number,
	response
):
	return controllerProvaBase.deleteProvaBaseById(response, id)
