import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *
from	datetime	import datetime

from	.materia	import schema_materia, Materia

schema_usuario	= {
	"type": "object",
	"properties": {
		"nome": {
			"type": "string"
		},
		"email": {
			"type": "string"
		},
		"senha": {
			"type": "string"
		},
		"materias": schema_materia
	},
	"required": [
		"nome",
		"email",
		"senha",
	]
}

class UsuarioType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_usuario)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Usuario(DynamicDocument):
	nome			= StringField(max_length=254, required=True)
	senha			= StringField(required=True)
	email			= StringField(max_length=254, required=True)
	materias		= EmbeddedDocumentListField(Materia)
	timestamp		= DateTimeField(default=datetime.now())
	timeupdate		= DateTimeField(default=datetime.now())
