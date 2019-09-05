import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	model.prova		import ProvaType, Prova

def getProvas(response, usuario_id, materia_id, turma_id):
	locals	= eval(response.get_header("locals"))
	try:
		provas	= Usuario.objects.get(_id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas
		data	= []
		if provas:
			data	= json.loads(provas.to_json())
		for item in data:
			item.pop('realizacoes', None)
			item.pop('questoes', None)
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getProvaById(response, usuario_id, materia_id, turma_id, prova_id):
	locals	= eval(response.get_header("locals"))
	try:
		prova	= Usuario.objects.get(_id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
		data	= []
		if prova:
			data	= json.loads(prova.to_json())
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newProva(response, usuario_id, materia_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		turma	= Usuario.objects.get(_id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id)
		data.pop("realizacoes", None)
		prova	= Prova(**data)
		turma.provas.append(turma)
		turma.save()
		response.status = HTTP_201
		return json.loads(prova.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateProva(response, usuario_id, materia_id, turma_id, prova_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		prova		= Usuario.objects.get(_id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
		data.pop("timestamp", None)
		data.pop("realizacoes", None)
		data["timeupdate"]	= datetime.now()
		for key, value in data.items():
			prova[key]	= value
		prova.save()
		return json.loads(prova.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteProva(response, usuario_id, materia_id, turma_id, prova_id):
	locals	= eval(response.get_header("locals"))
	try:
		prova		= Usuario.objects.get(_id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
		prova.delete()
		return {}
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
