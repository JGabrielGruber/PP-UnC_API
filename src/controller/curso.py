import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	controller		import auth

def getCursos(response):
	try:
		data	= json.loads(Curso.objects.to_json())
		return data

	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newCurso(response, data):
	locals	= eval(response.get_header("locals"))
	try:
		curso	= Curso(**data)
		usuario.save()
		response.status = HTTP_201
		return json.loads(curso.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
