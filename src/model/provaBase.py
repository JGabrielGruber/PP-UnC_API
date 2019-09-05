import	hug
import	numpy
from	jsonschema		import validate, exceptions
from	mongoengine		import *
from	datetime		import datetime
from	bson.objectid	import ObjectId

from	.questao	import schema_questao, Questao

schema_prova_base	= {
	"type":	"object",
	"properties": {
		"titulo": {
			"type": "string"
		},
		"descricao": {
			"type": "string"
		},
		"questoes": {
			"type": "array",
			"items": schema_questao
		}
	},
	"required": [
		"titulo"
	]
}

class ProvaBaseType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_prova)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class ProvaBase(EmbeddedDocument):
	_id			= ObjectIdField(required=True, default=lambda: ObjectId())
	titulo		= StringField(required=True)
	descricao	= StringField(required=True)
	questoes	= ListField(EmbeddedDocumentField(Questao))
	timestamp	= DateTimeField(default=datetime.now())
	timeupdate	= DateTimeField(default=datetime.now())
