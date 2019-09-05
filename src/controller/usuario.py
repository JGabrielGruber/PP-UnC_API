import	json
from	falcon		import HTTP_201, HTTP_400, HTTP_403, HTTP_502
from	datetime	import datetime

from	model.usuario	import Usuario
from	controller		import auth

def getUsuarios(response):
	try:
		data	= json.loads(Usuario.objects.to_json())
		for item in data:
			item.pop('senha', None)
			item.pop('materias', None)
		return data

	except Exception as e:
		print(e)
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def getUsuarioById(response, id):
	try:
		data	= json.loads(Usuario.objects.get(id=id).to_json())
		data.pop('senha')
		data.pop('materias.turmas', None)
		data.pop('materias.provasBases', None)
		return data

	except Exception as e:
		print(e)
		response.status = HTTP_502
		return { "error": "bad_gateway" }

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
			e=e
		usuario	= Usuario(**data)
		usuario["timestamp"]	= datetime.now()
		usuario["timeupdate"]	= datetime.now()
		usuario.save()
		response.status = HTTP_201
		return json.loads(usuario.to_json())
	except Exception as e:
		response.status = HTTP_502
		return { "error": "bad_gateway" }

def updateUsuario(response, id, data):
	locals	= eval(response.get_header("locals"))
	if locals["client_id"] == id:
		try:
			item.pop('senha')
			data.pop('materias', None)
			usuario					= Usuario.objects.get(id)
			usuario["timeupdate"]	= datetime.now()
			for key, value in data.items():
				usuario[key]	= value
			usuario.save()
			return json.loads(usuario.to_json())
		except Exception as e:
			response.status = HTTP_502
			return { "error": "bad_gateway" }
	else:
		response.status = HTTP_403
		return { "error" : "access_denied" }

def deleteUsuarioById(response, id):
	locals	= eval(response.get_header("locals"))
	if locals["client_id"] == id:
		try:
			delete	= auth.removeAuth(response, id)
			if not delete:
				return Usuario.objects.get(id=id).delete()
			else:
				return delete

		except Exception as e:
			response.status = HTTP_502
			return { "error": "bad_gateway" }
	else:
		response.status = HTTP_403
		return { "error" : "access_denied" }
