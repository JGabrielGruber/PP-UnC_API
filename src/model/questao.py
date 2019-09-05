import	hug
import	numpy
from	jsonschema		import validate, exceptions
from	mongoengine		import *
from	datetime		import datetime
from	bson.objectid	import ObjectId

schema_questao	= {
	"type":	"object",
	"properties": {
		"descricao": {
			"type": "string"
		},
		"isAlternativa": {
			"type": "boolean"
		},
		"alternativas": {
			"type": "array",
			"items": {
				"type": "string"
			}
		},
		"isMultipla": {
			"type": "boolean"
		},
		"corretas": {
			"type": "array",
			"items": {
				"type": "number"
			}
		},
		"esperado": {
			"type": "string"
		},
		"peso": {
			"type": "number"
		},
	},
	"required": [
		"descricao",
		"isAlternativa",
		"peso"
	]
}

class QuestaoType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_questao)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Questao(EmbeddedDocument):
	_id				= ObjectIdField(required=True, default=lambda: ObjectId())
	descricao		= StringField(required=True)
	isAlternativa	= BooleanField(required=True)
	alternativas	= ListField(StringField())
	isMultipla		= BooleanField()
	corretas		= ListField(IntField())
	esperado		= StringField()
	peso			= FloatField(max_length=2, required=True)
	timestamp		= DateTimeField(default=datetime.now())
	timeupdate		= DateTimeField(default=datetime.now())
