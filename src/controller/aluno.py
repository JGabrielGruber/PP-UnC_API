import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	model.aluno		import AlunoType, Aluno
from	library			import errorHandler

def getAlunos(response, usuario_id, materia_id, turma_id):
	try:
		alunos	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos
		data	= []
		if alunos:
			for aluno in alunos:
				data.append(json.loads(json.dumps(aluno.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
		return data
	except Exception as e:
		return errorHandler.handleError(response, e)

def getAlunoById(response, usuario_id, materia_id, turma_id, aluno_id):
	try:
		aluno	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos.get(_id=aluno_id)
		data	= []
		if aluno:
			data	= json.loads(json.dumps(aluno.to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
		return data
	except Exception as e:
		return errorHandler.handleError(response, e)

def newAluno(response, usuario_id, materia_id, turma_id, data):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		aluno	= Aluno(**data)
		usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos.append(aluno)
		usuario.save()
		response.status = HTTP_201
		return json.loads(json.dumps(aluno.to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
	except Exception as e:
		return errorHandler.handleError(response, e)

def updateAluno(response, usuario_id, materia_id, turma_id, aluno_id, data):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		aluno	= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos.get(_id=aluno_id)
		data.pop("_id", None)
		data.pop("timestamp", None)
		data["timeupdate"]	= datetime.now()
		for key, value in data.items():
			aluno[key]	= value
		usuario.save()
		return json.loads(json.dumps(aluno.to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
	except Exception as e:
		return errorHandler.handleError(response, e)

def deleteAlunoById(response, usuario_id, materia_id, turma_id, aluno_id):
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos.filter(_id=aluno_id).delete()
		usuario.save()
		return
	except Exception as e:
		return errorHandler.handleError(response, e)
