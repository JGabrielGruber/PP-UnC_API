import	hug

from	route	import auth, curso, usuario

@hug.get('/')
def get_index():
	return ""

@hug.extend_api('/usuarios')
def usuario_api():
	return [usuario]

@hug.extend_api('/cursos')
def curso_api():
	return [curso]

@hug.extend_api('/oauth')
def auth_api():
	return [auth]
