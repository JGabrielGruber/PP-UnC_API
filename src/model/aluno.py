import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *
from	datetime	import datetime

schema_aluno	= {
	"type":	"object",
	"properties": {
		"nome": {
			"type": "string"
		},
		"email": {
			"type": "string"
		}
	},
	"required": [
		"nome",
		"email"
	]
}

class AlunoType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_aluno)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Aluno(EmbeddedDocument):
	nome		= StringField(required=True)
	email		= EmailField(required=True)
	timestamp	= DateTimeField(default=datetime.now())
	timeupdate	= DateTimeField(default=datetime.now())
