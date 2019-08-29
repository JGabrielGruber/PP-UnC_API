import	hug
import	numpy
from	jsonschema	import validate, exceptions
from	mongoengine	import *
from	datetime	import datetime

schema_resposta	= {
	"type":	"object",
	"properties": {
		"escolhas": {
			"type": "array",
			"items": {
				"type": "number"
			}
		},
		"resposta": {
			"type": "string"
		},
		"correta": {
			"type": "boolean"
		},
		"meioCorreta": {
			"type": "boolean"
		}
	}
}

class RespostaType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_resposta)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Resposta(EmbeddedDocument):
	escolhas		= ListField(IntField())
	resposta		= StringField()
	correta			= BooleanField()
	meioCorreta		= BooleanField()
	timestamp		= DateTimeField(default=datetime.now())
	timeupdate		= DateTimeField(default=datetime.now())
