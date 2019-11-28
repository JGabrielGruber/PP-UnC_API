import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime, timedelta

from	model.usuario		import Usuario
from	model.realizacao	import RealizacaoType, Realizacao
from	model.resposta		import Resposta
from	controller			import auth
from	library				import errorHandler

def getRealizacaos(response, usuario_id, materia_id, turma_id, prova_id):
	try:
		realizacoes	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).realizacoes
		data		= []
		if realizacoes:
			for realizacao in realizacoes:
				data.append(json.loads(json.dumps(realizacao.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
		for item in data:
			item.pop('respostas', None)
		return data
	except Exception as e:
		return errorHandler.handleError(response, e)

def getRealizacaoById(response, usuario_id, materia_id, turma_id, prova_id, realizacao_id):
	locals	= eval(response.get_header("locals"))
	try:
		realizacao	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).realizacoes.get(_id=realizacao_id)
		data	= []
		if realizacao:
			data	= json.loads(json.dumps(realizacao.to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
		return data
	except Exception as e:
		return errorHandler.handleError(response, e)

def newRealizacao(response, usuario_id, materia_id, turma_id, prova_id, data):
	try:
		usuario		= Usuario.objects.get(id=usuario_id)
		materia		= usuario.materias.get(_id=materia_id)
		prova		= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
		dataAlunos	= data["alunos"]
		realizacoes	= []
		data["limite"] = datetime.fromtimestamp(data["limite"])
		data.pop("alunos")
		for aluno in dataAlunos:
			aluno	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos.get(_id=aluno)
			realizacao	= Realizacao(aluno=aluno, **data)
			prova.realizacoes.append(realizacao)
			usuario.save()
			auth.sendToken(response, "Link de acesso da prova", {
				"name": "PP-UnC - " + usuario['nome'],
				"client_id": str(usuario['email']).split('@')[0],
				"domain": usuario['email'].split('@')[1],
				"email": usuario['email']
			}, {
				"name": aluno['nome'],
				"client_id": str(aluno['email']).split('@')[0],
				"domain": str(aluno['email']).split('@')[1],
				"email": str(aluno['email']),
				"limit": data['limite'],
				"level": "aluno"
			}, [
				usuario_id,
				materia_id,
				turma_id,
				prova_id,
				str(realizacao["_id"])
			], prova.titulo + " da matéria " + materia.titulo)
			realizacoes.append(json.loads(json.dumps(realizacao.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
		response.status = HTTP_201
		return realizacoes
	except Exception as e:
		return errorHandler.handleError(response, e)

def startRealizacao(response, usuario_id, materia_id, turma_id, prova_id, realizacao_id):
	try:
		usuario		= Usuario.objects.get(id=usuario_id)
		realizacao	= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).realizacoes.get(_id=realizacao_id)
		if not realizacao.iniciada:
			questoes	= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).questoes
			realizacao.timeupdate	= datetime.now()
			realizacao.timestarted	= datetime.now()
			realizacao.iniciada		= True
			for questao in questoes:
				resposta			= Resposta()
				resposta.questao	= str(questao._id)
				realizacao.respostas.append(resposta)
			usuario.save()
		return json.loads(json.dumps(realizacao.to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
	except Exception as e:
		return errorHandler.handleError(response, e)

def updateRealizacao(response, usuario_id, materia_id, turma_id, prova_id, realizacao_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		usuario		= Usuario.objects.get(id=usuario_id)
		prova		= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id)
		realizacao	= prova.realizacoes.get(_id=realizacao_id)
		data.pop("timestamp", None)
		data.pop("aluno", None)
		data["timeupdate"]	= datetime.now()
		if not locals["level"] == "usuario" and not locals["level"] == "admin":
			data.pop("total", None)
			data.pop("timestarted", None)
			data.pop("limite", None)
			data.pop("iniciada", None)
			if realizacao["timestarted"] + timedelta(minutes=prova["duracao"]) < datetime.now():
				return json.loads(json.dumps(realizacao.to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
		if data["respostas"]:
			for resposta in data["respostas"]:
				resposta.pop("correta", None)
				resposta.pop("meioCorreta", None)
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
		return json.loads(json.dumps(realizacao.to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
	except Exception as e:
		return errorHandler.handleError(response, e)

def deleteRealizacaoById(response, usuario_id, materia_id, turma_id, realizacao_id, prova_id):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).provas.get(_id=prova_id).realizacoes.filter(_id=prova_id).delete()
		usuario.save()
		return
	except Exception as e:
		return errorHandler.handleError(response, e)
