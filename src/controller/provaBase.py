import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	model.materia	import Materia
from	model.provaBase		import ProvaBaseType, ProvaBase
from	controller		import auth

def getProvaBases(response, usuario_id, materia_id):
	locals	= eval(response.get_header("locals"))
	try:
		materias	= Usuario.objects.get(id=usuario_id).materias
		data		= []
		if materias:
			data	= json.loads(materias.to_json())
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getProvaBaseById(response, usuario_id, materia_id, provaBase_id):
	locals	= eval(response.get_header("locals"))
	try:
		provaBase		= Usuario.objects.get(id=usuario_id).materias.get(id=materia_id).provas_bases.get(id=provaBase_id)
		data		= []
		if provaBase:
			data	= json.loads(provaBase.to_json())
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newProvaBase(response, usuario_id, materia_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		materia	= Usuario.objects.get(id=usuario_id).materias.get(id=materia_id)
		data.pop("alunos", None)
		data.pop("provas", None)
		provaBase	= ProvaBase(**data)
		materia.provas_bases.append(provaBase)
		materia.save()
		response.status = HTTP_201
		return json.loads(provaBase.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateProvaBase(response, usuario_id, materia_id, provaBase_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		provaBase	= Usuario.objects.get(id=usuario_id).materias.get(id=materia_id).provas_bases.get(id=provaBase_id)
		data.pop("timestamp", None)
		data["timeupdate"]	= datetime.now()
		for key, value in data.items():
			provaBase[key]	= value
		provaBase.save()
		return json.loads(provaBase.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteProvaBase(response, usuario_id, materia_id, provaBase_id):
	locals	= eval(response.get_header("locals"))
	try:
		provaBase	= Usuario.objects.get(id=usuario_id).materias.get(id=materia_id).provas_bases.get(id=provaBase_id)
		provaBase.delete()
		return {}
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
