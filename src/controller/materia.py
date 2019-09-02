import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	model.materia	import MateriaType, Materia
from	controller		import auth

def getMaterias(response):
	locals	= eval(response.get_header("locals"))
	try:
		materias	= Usuario.objects.get(id=locals["id"]).materias
		data		= []
		if materias:
			data	= json.loads(materias.to_json())
		for item in data:
			item.pop('turmas', None)
			item.pop('provasBases', None)
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getMateriaById(response, id):
	locals	= eval(response.get_header("locals"))
	try:
		materia		= Usuario.objects.get(id=locals["id"]).materias.get(id=id)
		data		= []
		if materia:
			data	= json.loads(materia.to_json())
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newMateria(response, data):
	locals	= eval(response.get_header("locals"))
	try:
		usuario	= Usuario.objects.get(id=locals["id"])
		data.pop("turmas", None)
		data.pop("provasBases", None)
		materia	= Materia(**data)
		usuario.materias.append(materia)
		usuario.save()
		response.status = HTTP_201
		return json.loads(curriculo.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateMateria(response, data):
	locals	= eval(response.get_header("locals"))
	try:
		materia		= Usuario.objects.get(id=locals["id"]).materias.get(id=id)
		data.pop("timestamp", None)
		data.pop("turmas", None)
		data.pop("provasBases", None)
		data["timeupdate"]	= datetime.now()
		for key, value in data.items():
			materia[key]	= value
		materia.save()
		return json.loads(materia.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteMateria(response):
	locals	= eval(response.get_header("locals"))
	try:
		materia		= Usuario.objects.get(id=locals["id"]).materias.get(id=id)
		materia.delete()
		return {}
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
