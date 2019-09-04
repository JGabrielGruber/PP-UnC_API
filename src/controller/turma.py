import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	model.materia	import Materia
from	model.turma		import TurmaType, Turma
from	controller		import auth

def getTurmas(response, usuario_id, materia_id):
	locals	= eval(response.get_header("locals"))
	try:
		turmas	= Usuario.objects.get(id=usuario_id).materias.get(id=materia_id).turmas
		data		= []
		if turmas:
			data	= json.loads(turmas.to_json())
		for item in data:
			item.pop('alunos', None)
			item.pop('provas', None)
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getTurmaById(response, usuario_id, materia_id, turma_id):
	locals	= eval(response.get_header("locals"))
	try:
		turma		= Usuario.objects.get(id=usuario_id).materias.get(id=materia_id).turmas.get(id=turma_id)
		data		= []
		if materia:
			data	= json.loads(materia.to_json())
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newTurma(response, usuario_id, materia_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		materia	= Usuario.objects.get(id=usuario_id).materias.get(id=materia_id)
		data.pop("alunos", None)
		data.pop("provas", None)
		turma	= Turma(**data)
		materia.turmas.append(turma)
		materia.save()
		response.status = HTTP_201
		return json.loads(turma.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateTurma(response, usuario_id, materia_id, turma_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		turma		= Usuario.objects.get(id=usuario_id).materias.get(id=materia_id).turmas.get(id=turma_id)
		data.pop("timestamp", None)
		data.pop("alunos", None)
		data.pop("provas", None)
		data["timeupdate"]	= datetime.now()
		for key, value in data.items():
			turma[key]	= value
		turma.save()
		return json.loads(turma.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteTurma(response, usuario_id, materia_id, turma_id):
	locals	= eval(response.get_header("locals"))
	try:
		turma		= Usuario.objects.get(id=usuario_id).materias.get(id=materia_id).turmas.get(id=turma_id)
		turma.delete()
		return {}
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
