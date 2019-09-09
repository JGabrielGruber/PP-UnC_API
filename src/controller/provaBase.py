import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	model.provaBase	import ProvaBaseType, ProvaBase
from	model.questao	import Questao
from	controller		import auth

def getProvaBases(response, usuario_id, materia_id):
	try:
		provasBases	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).provas_bases
		data		= []
		if provasBases:
			for provaBase in provasBases:
				data.append(json.loads(provaBase.to_json()))
		for item in data:
			item.pop('questoes', None)
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getProvaBaseById(response, usuario_id, materia_id, provaBase_id):
	try:
		provaBase	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).provas_bases.get(_id=provaBase_id)
		data		= []
		if provaBase:
			data	= json.loads(provaBase.to_json())
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newProvaBase(response, usuario_id, materia_id, data):
	try:
		usuario		= Usuario.objects.get(id=usuario_id)
		provaBase	= ProvaBase(**data)
		usuario.materias.get(_id=materia_id).provas_bases.append(provaBase)
		usuario.save()
		response.status = HTTP_201
		return json.loads(provaBase.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateProvaBase(response, usuario_id, materia_id, provaBase_id, data):
	try:
		usuario		= Usuario.objects.get(id=usuario_id)
		provaBase	= usuario.materias.get(_id=materia_id).provas_bases.get(_id=provaBase_id)
		ids			= []

		data.pop("timestamp", None)
		data["timeupdate"]	= datetime.now()
		if data["questoes"]:
			for key, value in enumerate(data["questoes"]):
				if not "_id" in value:
					questao	= Questao(**value)
					provaBase.questoes.append(questao)
					ids.append(questao["_id"])
					value	= json.loads(questao.to_json())
				else:
					questao	= provaBase.questoes.get(_id=value["_id"])
					ids.append(questao["_id"])
					for k, v in value.items():
						questao[k]	= v
			data.pop("questoes")
			usuario.save()
			usuario.reload()
			provaBase	= usuario.materias.get(_id=materia_id).provas_bases.get(_id=provaBase_id)
			questoes	= provaBase.questoes
			for questao in questoes:
				if questao["_id"] in ids:
					ids.pop(ids.index(questao["_id"]))
				else:
					ids.append(questao["_id"])
			for id in ids:
				provaBase.questoes.filter(_id=id).delete()
			usuario.save()
			usuario.reload()
			provaBase	= usuario.materias.get(_id=materia_id).provas_bases.get(_id=provaBase_id)
		for key, value in data.items():
			provaBase[key]	= value
		usuario.save()
		return json.loads(provaBase.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteProvaBaseById(response, usuario_id, materia_id, provaBase_id):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		usuario.materias.get(_id=materia_id).provas_bases.filter(_id=provaBase_id).delete()
		usuario.save()
		return
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
