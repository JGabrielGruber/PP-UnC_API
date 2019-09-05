import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	model.aluno		import AlunoType, Aluno

def getAlunos(response, usuario_id, materia_id, turma_id):
	locals	= eval(response.get_header("locals"))
	try:
		alunos	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos
		data	= []
		if alunos:
			for aluno in alunos:
				data.append(json.loads(aluno.to_json()))
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getAlunoById(response, usuario_id, materia_id, turma_id, aluno_id):
	locals	= eval(response.get_header("locals"))
	try:
		aluno	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos.get(_id=aluno_id)
		data	= []
		if aluno:
			data	= json.loads(aluno.to_json())
		return data
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def newAluno(response, usuario_id, materia_id, turma_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		aluno	= Aluno(**data)
		usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos.append(aluno)
		usuario.save()
		response.status = HTTP_201
		return json.loads(aluno.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateAluno(response, usuario_id, materia_id, turma_id, aluno_id, data):
	locals	= eval(response.get_header("locals"))
	try:
		usuario	= Usuario.objects.get(id=usuario_id)
		aluno	= usuario.materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos.get(_id=aluno_id)
		data.pop("timestamp", None)
		data["timeupdate"]	= datetime.now()
		for key, value in data.items():
			aluno[key]	= value
		usuario.save()
		return json.loads(aluno.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def deleteAluno(response, usuario_id, materia_id, turma_id, aluno_id):
	locals	= eval(response.get_header("locals"))
	try:
		aluno	= Usuario.objects.get(id=usuario_id).materias.get(_id=materia_id).turmas.get(_id=turma_id).alunos.get(_id=aluno_id)
		aluno.delete()
		return {}
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }
