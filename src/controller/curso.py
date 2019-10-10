import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	controller		import auth
from	library			import errorHandler

def getCursos(response):
	try:
		data	= json.loads(json.dumps(Curso.objects.to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
		return data

	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def newCurso(response, data):
	locals	= eval(response.get_header("locals"))
	try:
		curso	= Curso(**data)
		usuario.save()
		response.status = HTTP_201
		return json.loads(json.dumps(curso.to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)
