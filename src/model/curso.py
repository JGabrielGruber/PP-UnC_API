import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *

schema_curso	= {
	"type":	"object",
	"properties": {
		"titulo": {
			"type": "string"
		}
	},
	"required": [
		"titulo"
	]
}

class CursoType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_curso)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Curso(EmbeddedDocument):
	titulo	= StringField(required=True)
