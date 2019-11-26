import	hug
import	numpy
from	jsonschema		import validate, exceptions
from	mongoengine		import *
from	datetime		import datetime
from	bson.objectid	import ObjectId

schema_resposta	= {
	"type":	"object",
	"properties": {
		"questao": {
			"type": "string"
		},
		"escolhas": {
			"type": "array",
			"items": {
				"type": "string"
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
	},
	"required": [
		"questao"
	]
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
	_id			= ObjectIdField(required=True, default=lambda: ObjectId())
	questao		= ObjectIdField(required=True)
	escolhas	= ListField(StringField())
	resposta	= StringField()
	correta		= BooleanField()
	meioCorreta	= BooleanField()
	timestamp	= DateTimeField(default=datetime.now())
	timeupdate	= DateTimeField(default=datetime.now())
