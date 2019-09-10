import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario		import Usuario
from	model.realizacao	import RealizacaoType, Realizacao
from	model.resposta		import Resposta
from	controller			import auth

def getRealizacaos(response, usuario_id, materia_id, turma_id, prova_id):
	try:
		realizacoes	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).realizacoes
		data		= []
		if realizacoes:
			for realizacao in realizacoes:
				data.append(json.loads(realizacao.to_json()))
		for item in data:
			item.pop('respostas', None)
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getRealizacaoById(response, usuario_id, materia_id, turma_id, prova_id, realizacao_id):
	locals	= eval(response.get_header("locals"))
	try:
		realizacao	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).realizacoes.get(_id=realizacao_id)
		data	= []
		if realizacao:
			data	= json.loads(realizacao.to_json())
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newRealizacao(response, usuario_id, materia_id, turma_id, prova_id, data):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		aluno	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos.get(_id=data["aluno"])
		prova	= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
		data.pop("aluno")
		realizacao	= Realizacao(aluno=aluno, **data)
		prova.realizacoes.append(realizacao)
		usuario.save()
		auth.sendToken(response, "Link de acesso da prova", {
			"name": usuario['nome'],
			"client_id": str(usuario['id']),
			"email": usuario['email']
		}, {
			"name": aluno['nome'],
			"client_id": str(aluno['_id']),
			"email": aluno['email'],
			"minutes": prova['duracao'],
			"level": "aluno"
		}, [
			usuario_id,
			materia_id,
			turma_id,
			prova_id,
			str(realizacao["_id"])
		])
		response.status = HTTP_201
		return json.loads(realizacao.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateRealizacao(response, usuario_id, materia_id, turma_id, prova_id, realizacao_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		usuario		= Usuario.objects.get(id=usuario_id)
		realizacao	= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).realizacoes.get(_id=realizacao_id)
		data.pop("timestamp", None)
		data.pop("aluno", None)
		data["timeupdate"]	= datetime.now()
		if not locals["level"] == "usuario" and not locals["level"] == "admin":
			data.pop("total", None)
			for resposta in data["respostas"]:
				resposta.pop("correta", None)
				resposta.pop("meioCorreta", None)
		if data["respostas"]:
			for key, value in enumerate(data["respostas"]):
				if not "_id" in value and not realizacao.respostas.filter(questao=value["questao"]):
					resposta	= Resposta(**value)
					realizacao.respostas.append(resposta)
				else:
					resposta	= realizacao.respostas.filter(questao=value["questao"])[0]
					for k, v in value.items():
						resposta[k]	= v
			data.pop("respostas")
			usuario.save()
			usuario.reload()
		data.pop("_id", None)
		for key, value in data.items():
			realizacao[key]	= value
		usuario.save()
		return json.loads(realizacao.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteRealizacaoById(response, usuario_id, materia_id, turma_id, realizacao_id, prova_id):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).realizacoes.filter(_id=prova_id).delete()
		usuario.save()
		return
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
