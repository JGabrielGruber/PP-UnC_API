import	hug

from	library.veryx	import auth
from	controller		import curso as controllerCurso
from	model			import curso as modelCurso

@hug.get('/', requires=auth.basicAccess('usuario'))
def get_index(
	response
):
	return controllerCurso.getCursos(response)

@hug.post('/', requires=auth.basicAccess('usuario'))
def post_data(
	curso: modelCurso.CursoType(),
	response
):
	return controllerCurso.newCurso(response, curso)
