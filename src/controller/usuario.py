import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	controller		import auth
from	library			import errorHandler

def getUsuarios(response):
	try:
		data	= json.loads(json.dumps(Usuario.objects.to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
		for item in data:
			item.pop('senha', None)
			item.pop('materias', None)
		return data

	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def getUsuarioById(response, id):
	try:
		data	= json.loads(json.dumps(Usuario.objects.get(id=id).to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
		return dataUsuario(data)

	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def getUsuarioByEmail(response, email):
	try:
		data	= json.loads(json.dumps(Usuario.objects.get(email=email).to_mongo().to_dict(), indent=4, sort_keys=True, default=str))
		return data["_id"]

	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def newUsuario(response, data):
	try:
		data["senha"]	= auth.setAuth(
			response,
			{ "email": data["email"], "senha": data["senha"], "level": "usuario" },
			"usuario"
		)
		try:
			if data["senha"]["error"]:
				return data["senha"]
		except Exception as e:
			pass
		usuario	= Usuario(**data)
		usuario["timestamp"]	= datetime.now()
		usuario["timeupdate"]	= datetime.now()
		usuario.save()
		response.status = HTTP_201
		return dataUsuario(json.loads(json.dumps(usuario.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def updateUsuario(response, id, data):
	locals	= eval(response.get_header("locals"))
	try:
		data.pop('materias', None)
		data.pop('timestamp', None)
		data.pop('timeupdate', None)
		data.pop('senha', None)
		data.pop('email', None)
		usuario					= Usuario.objects.get(id=id)
		usuario["timeupdate"]	= datetime.now()
		for key, value in data.items():
			usuario[key]	= value
		usuario.save()
		return dataUsuario(json.loads(json.dumps(usuario.to_mongo().to_dict(), indent=4, sort_keys=True, default=str)))
	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def deleteUsuarioById(response, id):
	locals	= eval(response.get_header("locals"))
	try:
		delete	= auth.removeAuth(response, id)
		if not delete:
			return Usuario.objects.get(id=id).delete()
		else:
			return delete

	except Exception as e:
		return errorHandler.handleError(response, e.__class__.__name__)

def dataUsuario(data):
	data.pop('senha')
	for item in data["materias"]:
		item.pop('turmas', None)
		item.pop('provas_bases', None)
	return data
