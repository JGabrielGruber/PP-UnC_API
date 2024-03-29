import	hug
import	numpy
from	jsonschema		import validate, exceptions
from	mongoengine		import *
from	datetime		import datetime
from	bson.objectid	import ObjectId

from	.turma		import schema_turma, Turma
from	.provaBase	import schema_prova_base, ProvaBase

schema_materia	= {
	"type":	"object",
	"properties": {
		"titulo": {
			"type": "string"
		},
		"descricao": {
			"type": "string"
		},
		"turmas": {
			"type": "array",
			"items": schema_turma
		},
		"provas_bases": {
			"type": "array",
			"items": schema_prova_base
		},
	},
	"required": [
		"titulo"
	]
}

class MateriaType(hug.types.Type):
	__slots__ = ()

	def __call__(self, value):
		try:
			validate(value, schema_materia)
			return value
		except exceptions.ValidationError as e:
			raise ValueError({
				"invalid":		numpy.array(e.relative_path),
				"required":		e.validator_value
			})

class Materia(EmbeddedDocument):
	_id				= ObjectIdField(required=True, default=lambda: ObjectId())
	titulo			= StringField(required=True)
	descricao		= StringField()
	turmas			= EmbeddedDocumentListField(Turma)
	provas_bases	= EmbeddedDocumentListField(ProvaBase)
	timestamp		= DateTimeField(default=datetime.now())
	timeupdate		= DateTimeField(default=datetime.now())
