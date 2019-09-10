import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	model.prova		import ProvaType, Prova
from	model.questao	import Questao

def getProvas(response, usuario_id, materia_id, turma_id):
	try:
		provas	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas
		data	= []
		if provas:
			for prova in provas:
				data.append(json.loads(prova.to_json()))
		for item in data:
			item.pop('realizacoes', None)
			item.pop('questoes', None)
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getProvaById(response, usuario_id, materia_id, turma_id, prova_id):
	try:
		prova	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
		data	= []
		if prova:
			data	= dataProva(json.loads(prova.to_json()))
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newProva(response, usuario_id, materia_id, turma_id, data):
	try:
		data.pop("realizacoes", None)
		data.pop("questoes", None)
		usuario	= Usuario.objects.get(id=usuario_id)
		prova	= Prova(**data)
		usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.append(prova)
		usuario.save()
		response.status = HTTP_201
		return dataProva(json.loads(prova.to_json()))
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateProva(response, usuario_id, materia_id, turma_id, prova_id, data):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		prova	= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
		ids			= []

		data.pop("timestamp", None)
		data.pop("realizacoes", None)
		data.pop("_id", None)
		data["timeupdate"]	= datetime.now()
		if data["questoes"]:
			for key, value in enumerate(data["questoes"]):
				if not "_id" in value:
					questao	= Questao(**value)
					prova.questoes.append(questao)
					ids.append(questao["_id"])
					value	= json.loads(questao.to_json())
				else:
					questao	= prova.questoes.get(_id=value["_id"])
					ids.append(questao["_id"])
					for k, v in value.items():
						questao[k]	= v
			data.pop("questoes")
			usuario.save()
			usuario.reload()
			prova		= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
			questoes	= prova.questoes
			for questao in questoes:
				if questao["_id"] in ids:
					ids.pop(ids.index(questao["_id"]))
				else:
					ids.append(questao["_id"])
			for id in ids:
				prova.questoes.filter(_id=id).delete()
			usuario.save()
			usuario.reload()
			prova		= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
		for key, value in data.items():
			prova[key]	= value
		usuario.save()
		return json.loads(prova.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteProvaById(response, usuario_id, materia_id, turma_id, prova_id):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).filter(_id=provaBase_id).delete()
		usuario.save()
		return
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def dataProva(data):
	for item in data["realizacoes"]:
		item.pop('respostas', None)
		item.pop('nota', None)
		item.pop('timestamp', None)
		item.pop('timeupdate', None)
	return data
