import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario		import Usuario
from	model.realizacao	import RealizacaoType, Realizacao

def getRealizacaos(response, usuario_id, materia_id, turma_id, prova_id):
	locals	= eval(response.get_header("locals"))
	try:
		realizacoes	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
		data		= []
		if realizacoes:
			data	= json.loads(realizacoes.to_json())
		for item in data:
			item.pop('realizacoes', None)
			item.pop('questoes', None)
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getRealizacaoById(response, usuario_id, materia_id, turma_id, prova_id, realizacao_id):
	locals	= eval(response.get_header("locals"))
	try:
		realizacao	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).realizacoes.get(_id=realizacao_id)
		data	= []
		if prova:
			data	= json.loads(realizacao.to_json())
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newRealizacao(response, usuario_id, materia_id, prova_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		prova		= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
		realizacao	= Realizacao(**data)
		prova.realizacoes.append(realizacao)
		realizacao.save()
		response.status = HTTP_201
		return json.loads(realizacao.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateRealizacao(response, usuario_id, materia_id, turma_id, prova_id, realizacao_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		realizacao		= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).realizacoes.get(_id=realizacao_id)
		data.pop("timestamp", None)
		data["timeupdate"]	= datetime.now()
		for key, value in data.items():
			realizacao[key]	= value
		realizacao.save()
		return json.loads(realizacao.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteRealizacao(response, usuario_id, materia_id, turma_id, realizacao_id, prova_id):
	locals	= eval(response.get_header("locals"))
	try:
		realizacao		= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).realizacoes.get(_id=realizacao_id)
		realizacao.delete()
		return {}
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
