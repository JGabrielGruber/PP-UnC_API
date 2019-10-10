import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	model.materia	import Materia
from	model.turma		import TurmaType, Turma
from	controller		import auth
from	library			import errorHandler

def getTurmas(response, usuario_id, materia_id):
	try:
		turmas	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas
		data	= []
		if turmas:
			for turma in turmas:
				data.append(json.loads(json.dumps(turma.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
		for item in data:
			item.pop('alunos', None)
			item.pop('provas', None)
		return data
	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def getTurmaById(response, usuario_id, materia_id, turma_id):
	try:
		turma		= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id)
		data		= []
		if turma:
			data	= json.loads(json.dumps(turma.to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
		return dataTurma(data)
	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def newTurma(response, usuario_id, materia_id, data):
	try:
		data.pop("alunos", None)
		data.pop("provas", None)
		usuario	= Usuario.objects.get(id=usuario_id)
		turma	= Turma(**data)
		usuario.materias.get(_id=materia_id).turmas.append(turma)
		usuario.save()
		response.status = HTTP_201
		return dataTurma(json.loads(json.dumps(turma.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def updateTurma(response, usuario_id, materia_id, turma_id, data):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		turma	= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id)
		data.pop("timestamp", None)
		data.pop("alunos", None)
		data.pop("provas", None)
		data.pop("_id", None)
		data["timeupdate"]	= datetime.now()
		for key, value in data.items():
			turma[key]	= value
		usuario.save()
		return dataTurma(json.loads(json.dumps(turma.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def deleteTurmaById(response, usuario_id, materia_id, turma_id):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		usuario.materias.get(_id=materia_id).turmas.filter(_id=turma_id).delete()
		usuario.save()
		return
	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def dataTurma(data):
	for item in data["alunos"]:
		item.pop('email', None)
		item.pop('timestamp', None)
		item.pop('timeupdate', None)
	for item in data["provas"]:
		item.pop('descricao', None)
		item.pop('duracao', None)
		item.pop('questoes', None)
		item.pop('realizacoes', None)
		item.pop('timestamp', None)
		item.pop('timeupdate', None)
	return data
