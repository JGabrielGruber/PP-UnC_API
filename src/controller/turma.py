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
		turmas	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas
		data		= []
		if turmas:
			for turma in turmas:
				data.append(json.loads(turma.to_json()))
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
		turma		= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id)
		data		= []
		if turma:
			data	= json.loads(turma.to_json())
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newTurma(response, usuario_id, materia_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		data.pop("alunos", None)
		data.pop("provas", None)
		usuario	= Usuario.objects.get(id=usuario_id)
		turma	= Turma(**data)
		usuario.materias.get(_id=materia_id).turmas.append(turma)
		usuario.save()
		response.status = HTTP_201
		return json.loads(turma.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateTurma(response, usuario_id, materia_id, turma_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		turma	= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id)
		data.pop("timestamp", None)
		data.pop("alunos", None)
		data.pop("provas", None)
		data["timeupdate"]	= datetime.now()
		for key, value in data.items():
			turma[key]	= value
		usuario.save()
		return json.loads(turma.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteTurma(response, usuario_id, materia_id, turma_id):
	locals	= eval(response.get_header("locals"))
	try:
		turma	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id)
		turma.delete()
		return {}
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
