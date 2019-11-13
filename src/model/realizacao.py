import	hug
import	numpy
from	jsonschema		import validate, exceptions
from	mongoengine		import *
from	datetime		import datetime
from	bson.objectid	import ObjectId

from	.aluno		import schema_aluno, Aluno
from	.resposta	import schema_resposta, Resposta

schema_realizacao	= {
	"type":	"object",
	"properties": {
		"aluno": {
			"type": "string"
		},
		"respostas": {
			"type": "array",
			"items": schema_resposta
		},
		"iniciada": {
			"type": "boolean"
		},
		"finalizada": {
			"type": "boolean"
		},
		"limite": {
			"type": "string"
		},
		"total": {
			"type": "number"
		}
	},
	"required": [
		"aluno"
	]
}

class RealizacaoType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_realizacao)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Realizacao(EmbeddedDocument):
	_id			= ObjectIdField(required=True, default=lambda: ObjectId())
	aluno		= EmbeddedDocumentField(Aluno)
	respostas	= EmbeddedDocumentListField(Resposta)
	iniciada	= BooleanField()
	finalizada	= BooleanField()
	limite		= DateTimeField()
	total		= FloatField()
	timestamp	= DateTimeField(default=datetime.now())
	timeupdate	= DateTimeField(default=datetime.now())
