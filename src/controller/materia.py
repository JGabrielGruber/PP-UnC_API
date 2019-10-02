import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	model.materia	import MateriaType, Materia
from	controller		import auth

def getMaterias(response, usuario_id):
	try:
		materias	= Usuario.objects.get(id=usuario_id).materias
		data		= []
		if materias:
			for materia in materias:
				data.append(json.loads(json.dumps(materia.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
		for item in data:
			item.pop('turmas', None)
			item.pop('provasBases', None)
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getMateriaById(response, usuario_id, materia_id):
	try:
		materia		= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id)
		data		= []
		if materia:
			data	= dataMateria(json.loads(json.dumps(materia.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newMateria(response, usuario_id, data):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		data.pop("turmas", None)
		data.pop("provasBases", None)
		materia	= Materia(**data)
		usuario.materias.append(materia)
		usuario.save()
		response.status = HTTP_201
		return dataMateria(json.loads(json.dumps(materia.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateMateria(response, usuario_id, materia_id, data):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		materia	= usuario.materias.get(_id=materia_id)
		data.pop("timestamp", None)
		data.pop("turmas", None)
		data.pop("provas_bases", None)
		data["timeupdate"]	= datetime.now()
		for key, value in data.items():
			materia[key]	= value
		usuario.save()
		return dataMateria(json.loads(json.dumps(materia.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteMateriaById(response, usuario_id, materia_id):
	try:
		Usuario.objects(id=usuario_id).update_one(pull__materias___id=materia_id)
		return
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def dataMateria(data):
	for item in data["turmas"]:
		item.pop('alunos', None)
		item.pop('provas', None)
		item.pop('semestre', None)
		item.pop('descricao', None)
		item.pop('timestamp', None)
		item.pop('timeupdate', None)
	for item in data["provas_bases"]:
		item.pop('questoes', None)
		item.pop('descricao', None)
		item.pop('timestamp', None)
		item.pop('timeupdate', None)
	return data
